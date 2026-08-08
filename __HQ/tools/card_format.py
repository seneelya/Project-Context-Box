"""Контракт формата карточки — ЕДИНЫЙ источник истины.

Правь ФОРМАТ здесь; `validate_cards.py` / `rebuild_graph.py` / `bundle.py`
импортят эти переменные, код тулов не трогаем.

Скелет карточки:
    # <name><ext>            <- H1: ТОЛЬКО имя файла (== имени исходника)
    <one-line summary>       <- 2-я непустая строка: короткая сводка (не пустая!)

    ## <section>             <- все секции из SECTIONS, по порядку, присутствие
    ...                         обязательно; если пусто — ровно EMPTY.
"""

# H1 больше НЕ содержит разделитель " — ": строка 1 = имя, строка 2 = сводка.

# Обязательные секции H2 (в этом порядке). Пусто -> EMPTY.
SECTIONS = [
    "Public API",
    "Dependencies Internal",
    "Dependencies External",
    "How it works",
    "Doc links",
    "Discrepancies",
]

# Подсекции Public API (H3) — РЕКОМЕНДУЕМЫЕ примеры, НЕ закрытый список: локальная
# модель группирует экспорт по виду и добавляет уместные для языка (Enums, Interfaces,
# Macros, ...). Включаются только те, что реально есть. Порядок — важное первым.
API_SUBSECTIONS = ["Functions", "Classes", "Constants", "Types", "Objects", "Re-exports"]

# Ре-экспорты/алиасы: имена, выставленные наружу, но живущие в другом файле (напр.
# back-compat `_setup = register_cli`). Здесь `_`-имена ДОПУСТИМЫ — это намеренный
# интерфейс, поэтому validator НЕ считает их "private in Public API".
REEXPORT_SUBSECTION = "Re-exports"

# Таблица "Dependencies Internal" — колонки в фиксированном порядке.
DEPS_COLUMNS = ["Import", "File Path", "Symbols", "Why", "Kind"]
EDGE_COLUMN = "File Path"     # из какой колонки берём рёбра графа (root-relative путь к файлу)
IMPORT_KINDS = ["normal", "lazy", "conditional", "type"]

# Маркер пустой секции/ячейки. Парсер принимает и вариант в бэктиках: `(none)`.
EMPTY = "(none)"

# Синонимы старых/иноязычных токенов -> канон (для миграции и терпимого чтения).
ALIASES = {
    # секции
    "Публичный API": "Public API",
    "Зависимости (внутренние)": "Dependencies Internal",
    "Internal dependencies": "Dependencies Internal",
    "Внешние зависимости": "Dependencies External",
    "External dependencies": "Dependencies External",
    "Принцип работы": "How it works",
    "Расхождения docstring ↔ код": "Discrepancies",
    "Docstring ↔ code discrepancies": "Discrepancies",
    # подсекции
    "Функции": "Functions",
    "Классы": "Classes",
    # колонки
    "Импортирует": "Import",
    "Из файла": "File Path",
    "From file": "File Path",
    "Объекты": "Symbols",
    "Objects": "Symbols",
    "Зачем": "Why",
    "Как": "Kind",
}


def canon(token):
    """Канонизирует заголовок/колонку через ALIASES (иначе возвращает как есть)."""
    return ALIASES.get(token.strip(), token.strip())


def is_empty(text):
    """True, если тело секции/ячейка — маркер пустоты (с бэктиками или без)."""
    return text.strip().strip("`").strip() == EMPTY
