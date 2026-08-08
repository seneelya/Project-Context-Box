# CONTEXT_RESTORE (__dev) — возобновление работы НАД ProjectStarter

> Это для НАШЕЙ разработки шаблона (не путать с продуктовым `CONTEXT_RESTORE.md` в корне — тот для
> downstream-проектов). Восстанавливаемся отсюда, снизу вверх, дёшево.

## Как восстановиться (по порядку)
1. Хвост `__dev/TRACKER.md` — где остановились и что next.
2. `__dev/DECISIONS.md` — залоченные решения (НЕ релитигировать).
3. Бегло `__dev/vision/Vision01__project-starter.md` (зачем скелет + инварианты) и
   `Vision02__cards-layer.md` (слой карточек: NOW/FUTURE, гейты).
4. `__dev/design-open-questions.md` — открытые вопросы схемы.

## Что построено (суть)
Скелет переведён на **`__`-маркер меты**: `__HQ` (мозг: roles/guides/tools/plans/vision/docs),
`__map` (плоские данные карт), `__dev` (наша разработка). Над карточками — «вторая компиляция»:
- **Контракт формата** — `__HQ/tools/card_format.py` (ЕДИНЫЙ источник): H1 = имя файла, сводка
  строкой 2; обязательные секции + `(none)`; deps-колонки `Import|File Path|Symbols|Why|Kind`
  (ребро = **File Path**, root-relative); **тип карточки** module vs package/node (`## Package layout`);
  `### Re-exports` (там `_`-имена ок); `ALIASES` (RU/легаси → канон); `canon()`, `is_empty()`,
  `sections_for()`.
- **Рецепт** — `__HQ/guides/Guide__MakeCard.md` (+ `Guide__AuditCards/BatchCards/SplitLargeFiles`).
- **Тулы `__HQ/tools/`:** `rebuild_graph.py` (плоская топология + `--json`), `bundle.py`
  (карточка цели + Public API её deps, `--depth`), `validate_cards.py` (проверка по контракту),
  `check_freshness.py` (актуальность, git/mtime, UTF-8), `mask_replace.py` (find/replace: `-r` простое,
  `-m EXPR` гард, `-R` рекурсия, escape `\n \t \r \\`), `py_api.py`. Все форсируют UTF-8 stdout.
  Фикстуры — `__HQ/tools/test/{graph_cards,valid_cards}/`.

## Состояние memohood (полигон)
Переведён на новый скелет — коммит memohood **`f60b3f6`**: layout (`__HQ`/`__map` flatten) + новый
тулинг + пути. Тулы работают на нём (дефолт или `--cards-dir/--project-root`). **НО формат карточек
ещё ЛЕГАСИ** (`validate_cards`: 83/83 с проблемами) — миграция ФОРМАТА = следующий шаг.

## Next (приоритет)
1. **Миграция формата карточек memohood** (`__map`) гардированным `mask_replace -R`:
   RU-заголовки/колонки → канон (по `ALIASES`, только на якорных строках-заголовках, НЕ в прозе);
   H1-split (`# name — summary` → строка-имя + строка-сводка); `From file` (дотточное `._engine`,
   проза) → root-relative путь файла. Потом `validate_cards` → остаток (private-in-API, реально
   unresolved) на ручной разбор/**майнинг** (искать удачные emergent-форматы, вносить в контракт).
2. Vision02 NOW остаток: свод `Discrepancies` со всех карточек; **причёсывалка вывода `git`** (шум↓).
3. FUTURE за гейтами (Vision02): структурный слайсер строка→объект (раньше векторов), вектора-по-
   докстрингам, зонирование графа `subgraph(point,depth)`, нарезка больших файлов, диаграмма оператору.

## Операционные грабли
- Рабочая директория на СТАРТЕ хода сбрасывается на **memohood** (primary) — `cd` в нужный репо ЯВНО.
- ProjectStarter и memohood — РАЗНЫЕ репо; не путать при git.
- Свипы путей — гард `(?<!_)` (perl), чтобы `__` не стало `___`; исходник `_engine/_core/_lab` НЕ трогать.
- Тулы читают git-вывод как UTF-8 (memohood-коммиты кириллические); Windows-консоль cp1251 иначе давится.
- `__pycache__` в `.gitignore` (тулы импортят друг друга — `bundle`/`validate` тянут `rebuild_graph`/`card_format`).
