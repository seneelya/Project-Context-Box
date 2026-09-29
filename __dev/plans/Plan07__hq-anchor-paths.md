# Plan07 — `__HQ` как точка отсчёта: `MAP_DIR`/`LOG_DIR` от штаба, явное > конфиг, свежесть по двум git

> Замысел и правила — `__dev/vision/Vision08__hq-as-anchor.md` (читать первым, §3 — правила, §5 —
> что пересматриваем в tools-`Vision01__path-and-flag-conventions.md`). Номер сквозной с
> `__HQ/tools/__dev/plans/` (там до Plan06). Трекинг — хвост `__dev/TRACKER.md`
> (`__HQ/guides/Guide__Tracker.md`).

## Цель

Штаб (`__HQ`) может лежать вне исходников, агент может стартовать где угодно — тулы работают
одинаково правильно. Проверено вживую на `y:\SRC\llama.cpp_mix\` (форк llama.cpp, штаб со своим git,
скрыт от git llama.cpp), с запуском из `y:\SRC\`.

## Scope

- **Этап A — код тулов** (репо `__HQ/tools`): A1–A7 ниже.
- **Этап B — раскладка, доки, деплой** (репо ProjectStarter): только после того, как A проверен
  вживую. Детализируется отдельно по итогам A.
- Вне scope: C/C++ в штемпеле, правило выборочного картирования (Vision08 §7).

## Контракты (in → out)

- `HQ` = `Path(__file__).resolve().parent.parent` для тула в `<HQ>/tools/` — вычисляется, не
  конфигурируется.
- Конфиг (`<HQ>/tools/CONFIG__TOOLS.py`), `CONFIG_SCHEMA_VERSION = 2`:
  - `PROJECT_ROOT` — абсолютный, строка `r'...'`;
  - `MAP_DIR` — относительно `HQ` или абсолютный; нет ключа → легаси `PROJECT_ROOT/__map`;
  - `LOG_DIR` — при схеме ≥ 2 относительно `HQ`; при схеме < 2 — как было, от `PROJECT_ROOT`.
- Резолв каталога карточек (card-тулы), по порядку:
  1. `--cards-dir X` → `X`;
  2. `--project-root` задан явно (путь) → `<root>/__map` (MAP_DIR конфига не применяется);
  3. иначе (корень из конфига) → `MAP_DIR` конфига от `HQ`, или легаси `PROJECT_ROOT/__map`.
  `--project-root @` = «явно взять из конфига» → ведёт себя как п.3 (это тот же корень).
- Неявный корень: конфига нет / `PROJECT_ROOT` пуст / папки нет → exit 2 с понятным сообщением.
  Проверка «корень — предок тула» удаляется.

## Задачи (исполнитель — сильная модель; одна сессия)

- **A1. Резолвер в `graph_from_cards.py`.** `hq_root()`, `resolve_cards_dir(cards_dir_arg,
  project_root_arg, project_root)`; `resolve_project_root` — без ancestor-check, с проверкой
  существования; без конфига в неявной ветке — отказ. Новый модуль НЕ заводить (Vision08 §5).
- **A2. Подключить пять card-тулов:** `graph_from_cards`, `validate_cards`, `check_cards_freshness`,
  `collect_card_bundle` (у него своя копия `_resolve_project_root` → перевести на общий),
  `make_interface_card` (`_card_path` + `--all` + новый флаг `--cards-dir`; своя копия резолва корня
  → на общий).
- **A3. Конфиг своего штаба.** Неявная ветка — конфиг из `hq_root()/tools/`; явный чужой корень —
  как сейчас `load_config_at(root)` (легаси `root/__HQ/tools/`), иначе умолчания.
- **A4. `LOG_DIR` от `HQ`** при схеме ≥ 2 (логирование в `make_interface_card` и `get_codeblock`).
- **A5. `check_cards_freshness` — попарный git.** `git -C <dir файла>` для исходника и для карточки
  отдельно; dirty-набор — по каждому репо; сторона без git → mtime. Вывод `mode=` — показать
  раскладку (напр. `src=git cards=git(другой)`), без шума.
- **A6. Шаблонный `CONFIG__TOOLS.py`** в tools-репо: ключи `MAP_DIR`, `LOG_DIR` с комментарием про
  якорь `HQ`, схема 2. `__TLDR.md` затронутых тулов + `TOOLS.md` — флаг `--cards-dir` у штемпеля,
  правило «явное > конфиг».
- **A8. Generic-тулы: относительный `--file` сначала от `PROJECT_ROOT`** (`get_codeblock`,
  `find_code_usage`, `show_pyfile_api`) — Vision08 §5, третий пересмотр: корень → cwd, двойное
  совпадение → предупреждение, не-cwd → полный путь в `#File:`. Каждый тул у себя (generic-тулы в
  `graph_from_cards` не лезут).
- **A7. Проверка.**
  - Регресс tools (`check.py`, `test_cardstamp.py`, `run_restamp_fixtures.py`) — перед коммитом.
  - Легаси: прогон card-тулов на memohood без `MAP_DIR` — поведение прежнее (только чтение).
  - Живьём, cwd = `y:\SRC\`: `llama.cpp_mix` (клон llama.cpp + `git init` в `__HQ`, `__HQ` в
    `.git/info/exclude`) — штемпель python-файла llama.cpp (напр. `convert_hf_to_gguf.py`) без флагов
    → карточка в `__HQ/__map/`; граф/валидатор/бандл её видят; freshness: `fresh`, после правки
    исходника — `outdated`, после коммита карточки в git штаба — снова `fresh`.
  - Явный чужой корень (`--project-root <memohood> --cards-dir <scratch>`) — пишет туда, куда сказано.

## Критерии приёмки

- Все пункты A7 проходят; регресс не хуже базы (известные старые падения — отдельно названы).
- Ни одного `root / "__map"` в card-тулах мимо резолвера (grep).
- Легаси-проект без `MAP_DIR` работает без изменений.

## Context (что читать исполнителю)

- `__dev/vision/Vision08__hq-as-anchor.md` — целиком.
- `__HQ/tools/__dev/vision/Vision01__path-and-flag-conventions.md` §2 — действующая конвенция.
- Код (через `get_codeblock`, не целиком): `graph_from_cards.py` — `resolve_project_root` (≈49),
  `load_config_at` (≈92), `main` (≈884); `make_interface_card.py` — `_card_path` (≈872),
  резолв корня (≈947), `_stamp_all` (≈1061), `main` (≈1118), логирование (≈50–95);
  `check_cards_freshness.py` — `_git`/`is_git_repo`/`_dirty_paths`/`_last_commit_ts` (≈35–80),
  `check_git` (≈106), `main` (≈160); `validate_cards.py` `main` (≈199);
  `collect_card_bundle.py` `_resolve_project_root` (≈35), `main` (≈99); `get_codeblock` — место
  логирования (найти по `LOG_DIR`).
- Перед правкой: в tools-репо висят незакоммиченные `CONFIG__TOOLS.py` (M) и `CONFIG__TOOLS.py.bak`
  — посмотреть, что это, спросить владельца, не затирать.

— Опус5.5 (Claude Opus 5.5), 2026-09-29, по обсуждению с Натальей
