# __HQ/tools/ — инструменты над карточками (`__map/`)

Тонкий детерминированный слой над карточками кода. Все тулы читают/пишут по **контракту формата**
`card_format.py` — правишь формат ТАМ, тулы не трогаешь. Рецепт написания карточки — `../guides/Guide__MakeCard.md`.

## Общие правила
- **Пути по умолчанию:** карточки — `<project>/__map/`, корень проекта — родитель `__map/` (скрипт лежит
  в `__HQ/tools/`). Переопределяются `--cards-dir` / `--project-root`.
- **UTF-8:** все CLI-тулы форсируют UTF-8 stdout (карточки/коммиты бывают кириллические; иначе Windows-
  консоль cp1251 падает).
- **Зависимость:** `rebuild_graph`/`bundle`/`validate_cards` импортят `card_format.py` (единый источник
  токенов). `__pycache__/` — в `.gitignore`.

---

## Контракт (не CLI)
### `card_format.py`
Единственный источник истины о формате карточки. Константы: `MODULE_SECTIONS` / `PACKAGE_SECTIONS`
(обязательные H2 по типу карточки), `API_SUBSECTIONS`, `DEPS_COLUMNS`, `EDGE_COLUMN` (= `File Path`,
откуда рёбра графа), `EMPTY` (= `(none)`), `ALIASES` (RU/легаси → канон). Хелперы: `canon(token)`,
`is_empty(text)`, `is_package(filename)`, `sections_for(filename)`. Импортится другими тулами.

## Создание и проверка карточек (сторона CodeMap / Guide__MakeCard)
### `py_api.py <file.py>`
ast-подсказка писателю карточки: публичные функции/классы/методы с сигнатурами + импорты
(эвристика внутренние/внешние) + 1-я строка docstring. Только Python, ничего не пишет, не гейт.
```
python __HQ/tools/py_api.py capture.py
```
### `validate_cards.py [--cards-dir P] [--project-root P]`
Проверка карточек по контракту: H1 == имя файла, сводка не пуста, все секции по типу, deps-таблица
или `(none)`, каждый `File Path` резолвится в карточку, приватные `_x` в Public API (подсказка),
сироты (с `--project-root`). Скупой вывод, коучит создателя; exit 1 при проблемах.
```
python __HQ/tools/validate_cards.py --project-root .
```
### `check_freshness.py [--cards-dir P] [--project-root P]`
Какие карточки устарели относительно исходника (режим **git**: последний коммит исходника новее
карточки / незакоммиченная правка; фоллбэк **mtime**) и какие «сироты». Для устаревших в git-режиме
показывает коммиты, тронувшие исходник после карточки. exit 1 при устаревших/сиротах.
```
python __HQ/tools/check_freshness.py
```

## Потребление карты (сторона агента-исполнителя)
### `rebuild_graph.py [--cards-dir P] [--json]`
«Вторая компиляция»: плоская топология из карточек — модули + сводки + `depends_on`, точки входа
(самые востребованные), листья, нерезолвнутые рефы. Грузишь один раз, дальше impact/chain/layers —
в уме. `--json` — граф как JSON.
```
python __HQ/tools/rebuild_graph.py
```
### `bundle.py <file> [--cards-dir P] [--depth N]`
Экономия ВЫЗОВОВ: полная карточка цели + **только Public API** её зависимостей — одним блоком.
`--depth` разворачивает транзитивно (по умолчанию 1).
```
python __HQ/tools/bundle.py capture.py --depth 1
```

## Обслуживание / миграция
### `mask_replace.py <folder> <mask> [-r FIND WITH | -m EXPR FIND WITH] [-R]`
Батч find-and-replace в файлах по маске. `-r` — простая подстрока; `-m EXPR FIND WITH` — замена только
на строках, где Python-`EXPR` (доступны `line`, `re`) истинно (гард против прозы); правила применяются
в порядке CLI. `-R` — рекурсивно по подпапкам. В `FIND`/`WITH` декодируются escape `\n \t \r \\`.
```
python __HQ/tools/mask_replace.py __map "*.md" -R -m 'line.strip()=="## Публичный API"' "## Публичный API" "## Public API"
```

---

## Кто чем пользуется
- **Создатель карточек** (роль CodeMap по `Guide__MakeCard`): `py_api` (подсказка) → пишет карточку →
  `validate_cards` (само-проверка) → `check_freshness` (что переделать).
- **Потребитель** (агент-исполнитель/планировщик): `rebuild_graph` (карта), `bundle` (контекст под файл).
- **Оператор / миграции**: `mask_replace`.
