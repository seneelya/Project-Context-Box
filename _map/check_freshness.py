#!/usr/bin/env python3
"""Проверка актуальности .py.md карточек.

Два режима определения устаревших карточек:

- **git** (если корень проекта — git-репозиторий): карточка считается устаревшей,
  если её исходник изменён без соответствующего обновления карточки — либо в
  рабочем дереве (незакоммиченные правки исходника при чистой карточке), либо по
  истории коммитов (последний коммит, тронувший исходник, новее последнего
  коммита, тронувшего карточку).
- **mtime** (фоллбэк для догитовых проектов или если git недоступен): сравнивает
  mtime карточки и исходника; карточка старше исходника — устарела.

Использование:
    python check_freshness.py [--cards-dir PATH] [--project-root PATH]

По умолчанию ищет карточки в _map/cards/ рядом со скриптом,
а исходники — в родительской директории проекта.
"""

import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def get_mtime(filepath: Path) -> datetime:
    """Возвращает mtime файла как datetime."""
    stat = filepath.stat()
    return datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)


def format_ts(dt: datetime) -> str:
    """Форматирование datetime в читаемый вид."""
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")


# --------------------------------------------------------------------------- #
# git-режим
# --------------------------------------------------------------------------- #

def _git(project_root: Path, *args: str) -> tuple[int, str]:
    """Запускает git в корне проекта. Возвращает (returncode, stdout)."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(project_root), *args],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return proc.returncode, proc.stdout
    except (OSError, subprocess.SubprocessError):
        return 1, ""


def is_git_repo(project_root: Path) -> bool:
    """Проект под git и git доступен как команда."""
    if not (project_root / ".git").exists():
        return False
    code, out = _git(project_root, "rev-parse", "--is-inside-work-tree")
    return code == 0 and out.strip() == "true"


def _git_dirty_paths(project_root: Path) -> set[str]:
    """Пути с незакоммиченными изменениями (относительно корня, posix-слэши)."""
    code, out = _git(project_root, "status", "--porcelain")
    if code != 0:
        return set()
    dirty: set[str] = set()
    for line in out.splitlines():
        if len(line) < 4:
            continue
        path = line[3:].strip()
        # переименование "old -> new"
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        path = path.strip('"')
        dirty.add(path)
    return dirty


def _git_last_commit_ts(project_root: Path, rel_path: str) -> int | None:
    """Unix-время последнего коммита, тронувшего файл. None если файл не в истории."""
    code, out = _git(
        project_root, "log", "-1", "--format=%ct", "--", rel_path
    )
    out = out.strip()
    if code != 0 or not out:
        return None
    try:
        return int(out)
    except ValueError:
        return None


def _rel(path: Path, project_root: Path) -> str:
    return path.relative_to(project_root).as_posix()


def check_freshness_git(cards_dir: Path, project_root: Path) -> dict:
    """git-режим: устаревание по рабочему дереву + истории коммитов."""
    cards = sorted(cards_dir.rglob("*.py.md"))
    if not cards:
        print(f"⚠️ Карточек не найдено в {cards_dir}")
        return {"fresh": [], "outdated": [], "orphan": []}

    dirty = _git_dirty_paths(project_root)

    fresh = []
    outdated = []
    orphan = []

    for card in cards:
        rel_card = card.relative_to(cards_dir)
        rel_source = str(rel_card).replace(".md", "")
        source_path = project_root / rel_source

        if not source_path.exists():
            orphan.append(card)
            continue

        source_rel_git = _rel(source_path, project_root)
        card_rel_git = _rel(card, project_root)

        source_dirty = source_rel_git in dirty
        card_dirty = card_rel_git in dirty

        # Исходник изменён в рабочем дереве, а карточку не тронули → устарела.
        if source_dirty and not card_dirty:
            src_mt = get_mtime(source_path)
            card_mt = get_mtime(card)
            outdated.append((card, card_mt, src_mt))
            continue

        # Если оба (или только карточка) грязные — считаем, что карточку правят
        # вместе с кодом; доверяем.
        if source_dirty or card_dirty:
            fresh.append(card)
            continue

        # Чистое рабочее дерево — сравниваем историю коммитов.
        src_ct = _git_last_commit_ts(project_root, source_rel_git)
        card_ct = _git_last_commit_ts(project_root, card_rel_git)

        if src_ct is None:
            # Исходник не закоммичен и не грязный — нечего сравнивать, считаем свежим.
            fresh.append(card)
            continue

        if card_ct is None or src_ct > card_ct:
            src_mt = datetime.fromtimestamp(src_ct, tz=timezone.utc)
            card_mt = (
                datetime.fromtimestamp(card_ct, tz=timezone.utc)
                if card_ct is not None
                else get_mtime(card)
            )
            outdated.append((card, card_mt, src_mt))
        else:
            fresh.append(card)

    return {"fresh": fresh, "outdated": outdated, "orphan": orphan}


# --------------------------------------------------------------------------- #
# mtime-режим (фоллбэк)
# --------------------------------------------------------------------------- #

def check_freshness_mtime(cards_dir: Path, project_root: Path) -> dict:
    """Проверяет все карточки по mtime и возвращает отчёт."""
    cards = sorted(cards_dir.rglob("*.py.md"))
    if not cards:
        print(f"⚠️ Карточек не найдено в {cards_dir}")
        return {"fresh": [], "outdated": [], "orphan": []}

    fresh = []
    outdated = []
    orphan = []

    for card in cards:
        rel_card = card.relative_to(cards_dir)
        rel_source = str(rel_card).replace(".md", "")
        source_path = project_root / rel_source

        if not source_path.exists():
            orphan.append(card)
            continue

        card_mtime = get_mtime(card)
        source_mtime = get_mtime(source_path)

        if card_mtime >= source_mtime:
            fresh.append(card)
        else:
            outdated.append((card, card_mtime, source_mtime))

    return {"fresh": fresh, "outdated": outdated, "orphan": orphan}


def main():
    parser = argparse.ArgumentParser(description="Проверка актуальности .py.md карточек")
    parser.add_argument(
        "--cards-dir",
        type=Path,
        default=None,
        help="Путь к папке с карточками (по умолчанию: _map/cards/ рядом со скриптом)",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Корень проекта (по умолчанию: родительская директория cards-dir)",
    )
    args = parser.parse_args()

    if args.cards_dir:
        cards_dir = args.cards_dir.resolve()
    else:
        # Скрипт лежит в _map/, карточки в _map/cards/
        cards_dir = Path(__file__).parent / "cards"

    if args.project_root:
        project_root = args.project_root.resolve()
    else:
        # _map/cards/ → _map/ → проект
        project_root = cards_dir.parent.parent

    use_git = is_git_repo(project_root)
    mode = "git" if use_git else "mtime"

    print(f"📂 Карточки: {cards_dir}")
    print(f"📂 Проект:   {project_root}")
    print(f"🔎 Режим:    {mode}")
    print()

    if use_git:
        result = check_freshness_git(cards_dir, project_root)
    else:
        result = check_freshness_mtime(cards_dir, project_root)

    print("=" * 60)
    print("📊 ОТЧЁТ ОБ АКТУАЛЬНОСТИ КАРТОЧЕК")
    print("=" * 60)
    print()

    total = len(result["fresh"]) + len(result["outdated"]) + len(result["orphan"])
    print(f"Всего карточек: {total}")
    print(f"✅ Актуальных:   {len(result['fresh'])}")
    print(f"❌ Устаревших:   {len(result['outdated'])}")
    print(f"⚠️ Без исходника: {len(result['orphan'])}")
    print()

    if result["outdated"]:
        print("-" * 60)
        print("❌ УСТАРЕВШИЕ КАРТОЧКИ (нужен перезапуск Pass 1):")
        print("-" * 60)
        for card, card_mtime, source_mtime in sorted(result["outdated"]):
            rel_card = str(card.relative_to(cards_dir))
            rel_source = str(card.relative_to(cards_dir)).replace(".md", "")
            print(f"\n  📄 {rel_card}")
            print(f"     Исходник: {rel_source}")
            print(f"     Карточка: {format_ts(card_mtime)}")
            print(f"     Исходник: {format_ts(source_mtime)}")
            age_diff = source_mtime - card_mtime
            hours = age_diff.total_seconds() / 3600
            if hours < 1:
                print(f"     Разница: {age_diff.total_seconds():.0f} сек.")
            else:
                print(f"     Разница: {hours:.1f} ч.")
        print()

    if result["orphan"]:
        print("-" * 60)
        print("⚠️ КАРТОЧКИ БЕЗ ИСХОДНИКА:")
        print("-" * 60)
        for card in result["orphan"]:
            rel_card = str(card.relative_to(cards_dir))
            print(f"  📄 {rel_card}")
        print()

    if result["fresh"] and len(result["fresh"]) <= 5:
        print("-" * 60)
        print("✅ АКТУАЛЬНЫЕ КАРТОЧКИ:")
        print("-" * 60)
        for card in result["fresh"]:
            rel_card = str(card.relative_to(cards_dir))
            print(f"  📄 {rel_card}")
        print()

    print("=" * 60)
    if result["outdated"]:
        print(f"⚠️  НАЙДЕНО {len(result['outdated'])} УСТАРЕВШИХ КАРТОЧЕК")
        print("   Запустите Pass 1 для обновления.")
        sys.exit(1)
    elif result["orphan"]:
        print(f"⚠️  НАЙДЕНО {len(result['orphan'])} КАРТОЧЕК БЕЗ ИСХОДНИКА")
        sys.exit(1)
    else:
        print("✅ ВСЕ КАРТОЧКИ АКТУАЛЬНЫ!")
        sys.exit(0)


if __name__ == "__main__":
    main()
