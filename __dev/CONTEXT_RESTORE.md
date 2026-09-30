# CONTEXT_RESTORE (__dev) — возобновление работы НАД ProjectStarter

> Это для НАШЕЙ разработки шаблона (не путать с продуктовым `CONTEXT_RESTORE.md` в корне — тот для
> downstream-проектов). Восстанавливаемся отсюда, снизу вверх, дёшево.

## NEXT STEP (2026-09-30, before app restart)

codebase-memory-mcp (DeusData v0.11.0, call-graph MCP server) installed: exe
`Y:\Tools\codebase-memory-mcp\codebase-memory-mcp.exe` (SHA-256 matches the release, owner checked
VirusTotal), registered in `Y:\SRC\.mcp.json` (index cache `Y:\Tools\codebase-memory-mcp\cache`).
After the restart (owner approves the server): index `y:\SRC\llama.cpp_mix` with its
`index_repository`, then test on the mix task (see memory: MoE expert parallelism, target
`qwen4exp`): (1) who calls `build_moe_ffn`; (2) what `ggml_backend_sched_split_graph` calls;
(3) where expert tensors (`ffn_*_exps`) get their buffer / device. Watch calls through backend
function tables (`iface.graph_compute`) — likely blind spot; our cards mark them as `vtable` seams.
Then decide how it sits next to our tools (cards = meaning, get_codeblock = reading, it = call chains).

## START — Plan09 closed; next = owner's call (card prose by Grok on the 1.3.0 form?)

**Where we are (2026-09-30).** Plan08 (C/C++ stamp) closed except step 9 (clangd — needs a Ninja
build of the mix). Plan09 closed (Vision10 executed): scan cache `tools/_cache/<root>-<hash>/`
(zone restamp 31 -> 8 s); C/C++ header card = "API: in source" + family table + `### What each
family is for` (CARD_FORMAT 1.3.0; llama `ggml.h.md` 2637 -> 169 lines); `graph_from_cards --file`
shows files WITHOUT cards from the include tree (`(no card)`, folded by folder; `--cards-only`).
Registry hooks added: `import_line`, `api_families`, `source_edges` (`stamp_langs/CONTRACT.md` amendments 2–4).
Then (same day): get_codeblock fixed for C headers (`#ifdef` frames, bodyless typedefs), `--name`
(`get_codeblock/name_resolver.py`), C/C++ macros cut before parsing (`get_codeblock/cpp_source.py`).
Then: `--all --stale`, Why folded by folder, cards WITHOUT line numbers (anchors = names readable
with `get_codeblock --name`; a line shift no longer rewrites a card). **Next: nothing queued** —
card prose by Grok on the new form is the owner's call. Bump get_codeblock VERSION at session end.

**Read, in order:** tail of `__HQ/tools/__dev/TRACKER.md` → `__HQ/tools/__dev/vision/Vision10__cards-links-and-meaning.md`
→ `__HQ/tools/__dev/plans/Plan09__cards-links-and-meaning.md` → `__dev/DECISIONS.md` (last 4) →
if touching C/C++ code: `__HQ/tools/make_interface_card__TLDR.md` § C/C++ and Plan08 "Итог".
Code via `get_codeblock` (outline → block), never whole files.

**Owner's rules (standing):** tool plans/visions live in the TOOLS repo `__HQ/tools/__dev/`;
a language plugs in as a registry entry (`stamp_langs/`, find_code_usage registries), never an
`if lang ==`; no code before an explicit "поехали"; subagents only with consent.

**Repos (3 gits):** template `t:\AgentsWork\ProjectStarter` · tools `…\__HQ\tools` (nested) ·
`y:\SRC\llama.cpp_mix` (upstream `7fee17846`, branch `mix`; owner's stable build `y:\SRC\llama.cpp`
at `2b129ccfa` is 66 commits older on the same line — don't touch it). llama's `__HQ/` has its own
git (hidden by `.git/info/exclude`), config has `LANGUAGE=["cpp","python"]` + `CPP_*` keys, `__map`
holds 37 C/C++ cards (zone: ggml/include, backend layer, ggml-vulkan, ggml-cuda core). Sync tools:
`py __dev/deploy_hq.py --target y:\SRC\llama.cpp_mix --apply` — commit the tools repo FIRST, or the
deploy sees an unknown version as CONFLICT (then `--force <glob>` after checking the diff).
Restamp the zone: `python llama.cpp_mix/__HQ/tools/make_interface_card.py --all --path ggml/include
--path ggml/src/ggml-backend.cpp,ggml/src/ggml-backend-impl.h,ggml/src/ggml-backend-reg.cpp,ggml/src/ggml-backend-dl.cpp,ggml/src/ggml-backend-dl.h
--path ggml/src/ggml-vulkan --path ggml/src/ggml-cuda/ggml-cuda.cu,ggml/src/ggml-cuda/common.cuh` (from `y:\SRC`).

**Gotchas:**
- Regression: `test/check.py` 121/0, `test_cardstamp.py` 155/0, `test_cpp.py` 140/0,
  `test_name_resolver.py` 32/0, `golden_check.py` 13/13, `sweep_invariants.py` (CRASH=71 = cp1252 fixture, old),
  `run_restamp_fixtures.py` 21/0, `test_split_monster.py` ok, `test__replace_in_files.py` 15/21
  (OLD) — it DELETES fixtures when failing: `git -C __HQ/tools checkout -- test/test__replace_in_files/fixtures`.
- Bash heredocs EAT backslashes (`\n`, `\b` turned into control chars this session). Any edit with
  backslashes: write a .py to the scratchpad with Write, then run it.
- `tree_sitter_cpp` installed (required for C++ declarations); `tree_sitter_python`/`_c` are not.
- Session cwd `Y:\SRC`; don't touch memohood/hermes-filetools.

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
