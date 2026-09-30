# CONTEXT_RESTORE (__dev) — возобновление работы НАД ProjectStarter

> Это для НАШЕЙ разработки шаблона (не путать с продуктовым `CONTEXT_RESTORE.md` в корне — тот для
> downstream-проектов). Восстанавливаемся отсюда, снизу вверх, дёшево.

## START 2026-09-30 (evening) — C/C++ stamp DONE; next: card prose + wider zone

**Where we are.** Plan07 closed (HQ anchor). **Plan08 closed except step 9** — C/C++/CUDA in the
stamp, links and graph. Tool plans/visions now live in the TOOLS repo: `__HQ/tools/__dev/`
(`vision/Vision09__cpp-stamp.md`, `plans/Plan08__cpp-stamp.md` — its "Итог" section = what was
built and why it deviates). Owner's rules: language = registry entry, never an `if`; tool plans in
the tools `__dev`.

**Read, in order:** tail of `__HQ/tools/__dev/TRACKER.md` → Plan08 "Итог" → `__dev/DECISIONS.md`
(last 4 entries) → `__HQ/tools/make_interface_card__TLDR.md` § C/C++. Code via `get_codeblock`.

**Repos (3 gits):** template `t:\AgentsWork\ProjectStarter` · tools `…\__HQ\tools` (nested) ·
`y:\SRC\llama.cpp_mix` (upstream `7fee17846`, branch `mix`) whose `__HQ/` has its own git (hidden
by `.git/info/exclude`). Sync tools there: `py __dev/deploy_hq.py --target y:\SRC\llama.cpp_mix --apply`.
llama config (project-owned) has `LANGUAGE=["cpp","python"]`, `CPP_INCLUDE_DIRS`, `CPP_STRIP_MACROS`,
`CPP_WRAPPER_MACROS`. Its `__HQ/__map` has 37 C/C++ cards (ggml/include, backend layer, vulkan, cuda core).

**Next (proposal):** card prose is written by **Grok** per `Guide__MakeCard` (§ C/C++); widen the
zone as the mix work needs it (`tools/server`, model loading in `src/`); step 9 (compile_commands →
live/dead) once a Ninja build of the mix exists.

**Gotchas:**
- Regression: `test/check.py` 121/0, `test_cardstamp.py` 155/0, `test_cpp.py` 82/0,
  `run_restamp_fixtures.py` 21/0, `test_split_monster.py` ok, `test__replace_in_files.py` 15/21
  (OLD) — it DELETES fixtures when failing: `git -C __HQ/tools checkout -- test/test__replace_in_files/fixtures`.
- Bash heredocs EAT backslashes (twice this session: `\n`, `\b` became control chars). Edits with
  backslashes: write a .py to the scratchpad with Write, then run it.
- `tree_sitter_cpp` installed (required for C++ declarations); `tree_sitter_python`/`_c` are not.
- Session cwd `Y:\SRC`; don't touch memohood/hermes-filetools; subagents only with owner's consent.

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
