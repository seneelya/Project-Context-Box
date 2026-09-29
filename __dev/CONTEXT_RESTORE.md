# CONTEXT_RESTORE (__dev) — возобновление работы НАД ProjectStarter

> Это для НАШЕЙ разработки шаблона (не путать с продуктовым `CONTEXT_RESTORE.md` в корне — тот для
> downstream-проектов). Восстанавливаемся отсюда, снизу вверх, дёшево.

## START 2026-09-30 — next: C/C++ stamp (read this block first)

**Where we are.** Plan07 closed (`__dev/plans/done/Plan07__hq-anchor-paths.md`, `## CARRY` inside):
HQ is the path anchor, everything of ours lives inside `__HQ/` (entry files, `__HQ/__map`), tools take
`PROJECT_ROOT`/`MAP_DIR` from config and run from any cwd. Next work = **C/C++ stamp + graph** —
intent in `__HQ/tools/__dev/vision/Vision09__cpp-stamp.md` (tool plans/visions live in the TOOLS repo `__dev/`) (read it whole; no plan yet → Plan08 is the first step).

**Read, in order:** tail of `__dev/TRACKER.md` → `__dev/DECISIONS.md` (last 2 entries = Vision08
calls) → `Vision09__cpp-stamp.md` → `Vision08__hq-as-anchor.md` §3 (path rules, only if touching
paths). Tool code via `get_codeblock` (outline → block), never whole files.

**Repos (3 separate gits):**
- `t:\AgentsWork\ProjectStarter` — template (`__HQ/` docs, `__dev/`, `__dev/deploy_hq.py`).
- `t:\AgentsWork\ProjectStarter\__HQ\tools` — nested tools repo (the code we change).
- `y:\SRC\llama.cpp_mix` — clone of ggml-org/llama.cpp, branch `mix`, upstream HEAD `7fee17846`;
  its `__HQ/` has its OWN git, hidden via `.git/info/exclude`. Test card there:
  `__HQ/__map/convert_hf_to_gguf.py.md`. Sync tools into it by `deploy_hq.py --target y:\SRC\llama.cpp_mix --apply`
  (CONFIG__TOOLS.py there is project-owned: `PROJECT_ROOT=r'y:\SRC\llama.cpp_mix'`, schema 2).

**Plan08 first steps (proposal, agree with owner):** build fixture `__HQ/tools/test/cppSRC/`
(real folder structure, files listed in Vision09 §9, frozen at `7fee17846`, + LICENSE) →
`#include` extraction + resolution via `CPP_INCLUDE_DIRS` + condition tagging from tree-sitter preproc
nodes → header Public API (`CPP_STRIP_MACROS`) → `.h`↔`.cpp` pairing → seam hints → optional
`compile_commands.json`. Prose for cards is written by **Grok**, not by us.

**Gotchas:**
- Session cwd starts at `Y:\SRC`; tools must work from there (that is the point).
- Regression: `test/check.py` 116/0, `test_cardstamp.py` 144/0, `run_restamp_fixtures.py` 21/0,
  `test_split_monster.py` ok, `test__replace_in_files.py` 15/21 (OLD failures) — and it DELETES
  committed fixtures when failing: after a run `git -C __HQ/tools checkout -- test/test__replace_in_files/fixtures`.
- `tree_sitter_cpp` installed; `tree_sitter_python`/`tree_sitter_c` are NOT (python uses `ast` fallback).
- Big edits: python scripts with exact `str.replace` + count asserts; files are LF in index.
- Don't touch memohood/hermes-filetools (migration of our own projects is out of scope for now).
- Subagents only with the owner's consent.

---

## История (2026-08) — ниже старое состояние, для справки

## Как восстановиться (по порядку)
1. Хвост `__dev/TRACKER.md` — где остановились и что next.
2. `__dev/DECISIONS.md` — залоченные решения (НЕ релитигировать).
3. Бегло `__dev/vision/Vision01__project-starter.md` (зачем скелет + инварианты) и
   `Vision02__cards-layer.md` (слой карточек: NOW/FUTURE, гейты).
4. `__dev/design-open-questions.md` — открытые вопросы схемы.

## Что построено (суть)
Скелет переведён на **`__`-маркер меты**: `__HQ` (мозг: roles/guides/tools/plans/vision/docs),
`__map` (плоские данные карт), `__dev` (наша разработка). Над карточками — «вторая компиляция»:
- **Контракт формата** — `__HQ/tools/CARD_FORMAT.py` (ЕДИНЫЙ источник): H1 = имя файла, сводка
  строкой 2; обязательные секции + `(none)`; deps-колонки `Import|File Path|Symbols|Why|Kind`
  (ребро = **File Path**, root-relative); **тип карточки** module vs package/node (`## Package layout`);
  `### Re-exports` (там `_`-имена ок); `ALIASES` (RU/легаси → канон); `canon()`, `is_empty()`,
  `sections_for()`.
- **Рецепт** — `__HQ/guides/Guide__MakeCard.md` (+ `Guide__AuditCards/BatchCards/SplitLargeFiles`).
- **Тулы `__HQ/tools/`:** `graph_from_cards.py` (плоская топология + `--json`), `collect_card_bundle.py`
  (карточка цели + Public API её deps, `--depth`), `validate_cards.py` (проверка по контракту),
  `check_cards_freshness.py` (актуальность, git/mtime, UTF-8), `replace_in_files.py` (find/replace: `-r` простое,
  `-m EXPR` гард, `-R` рекурсия, escape `\n \t \r \\`), `show_pyfile_api.py`. Все форсируют UTF-8 stdout.
  Фикстуры — `__HQ/tools/test/{graph_cards,valid_cards}/`.

## Состояние memohood (полигон)
1) **Layout** — коммит memohood **`f60b3f6`**: `__HQ`/`__map` flatten + новый тулинг + пути.
2) **Формат карточек, МЕХАНИЧЕСКИЙ проход** — коммит **`7ffec8d`**: H1-split (`# name — summary` →
   имя + сводка) + канон общих H2-заголовков (`replace_in_files -R`, гард по точной строке-заголовку).
   Результат: legacy-H1 83→0, non-canonical-header 155→1.
Тулы работают (дефолт / `--cards-dir`). НО карточки ещё НЕ валидны (`validate_cards`: 83/83) — остаток
**не механический** (см. Next #1).

## Next (приоритет)
1. **Пере-генерация карточек memohood под контракт** — это НЕ find/replace, а работа **Role__CodeMap**
   (заново прогнать `Guide__MakeCard` по каждому файлу `__map`). Остаток после мех-прохода (validate):
   добавить `## Doc links` / `## Discrepancies` / колонку `Kind`; нормализовать `From file` → реальный
   root-relative путь (**18 unresolved**, дотточное `._engine` семантически); consumed-surface review
   приватных в Public API (**27**); заголовок Discrepancies с эмодзи (`## ⚠️ Расхождения…`) + one-off/
   мислевел заголовки (`## Внутреннее`, `## Классы` как H2, суффиксные `## Публичный API (…)`).
   ← ЗДЕСЬ ЖЕ **майнинг** emergent-форматов (читать «непрошедшие», годное → в контракт).
2. Vision02 NOW остаток: свод `Discrepancies` со всех карточек; **причёсывалка вывода `git`** (шум↓).
3. FUTURE за гейтами (Vision02): структурный слайсер строка→объект (раньше векторов), вектора-по-
   докстрингам, зонирование графа `subgraph(point,depth)`, нарезка больших файлов, диаграмма оператору.
4. **graph_from_cards — развести два вывода под ДВЕ аудитории** (решено, делаем в след. сессию):
   - `--json` = цель под **визуализатор структуры для оператора** (программа рисует красиво; связано с
     Vision02 FUTURE «диаграмма оператору»). Сейчас беднее текста → **дополнить** entry-points/leaves/
     in-degree. НЕ удалять `--json` — он переназначен под визуализатор.
   - **плоский текст** = для ЛЛМ → отладить/дотюнить полезность вывода.

## Операционные грабли
- Рабочая директория на СТАРТЕ хода сбрасывается на **memohood** (primary) — `cd` в нужный репо ЯВНО.
- ProjectStarter и memohood — РАЗНЫЕ репо; не путать при git.
- Свипы путей — гард `(?<!_)` (perl), чтобы `__` не стало `___`; исходник `_engine/_core/_lab` НЕ трогать.
- Тулы читают git-вывод как UTF-8 (memohood-коммиты кириллические); Windows-консоль cp1251 иначе давится.
- `__pycache__` в `.gitignore` (тулы импортят друг друга — `collect_card_bundle`/`validate` тянут `graph_from_cards`/`CARD_FORMAT`).
