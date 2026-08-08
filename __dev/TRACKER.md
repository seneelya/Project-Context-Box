# TRACKER — хвост-лог разработки шаблона ProjectStarter

> Прогресс работы над **самим скелетом**. Читать только ХВОСТ (последние строки). Дописывать в конец.
> Это НЕ шаблонный `__HQ/TRACKER.md` (тот — пустой скаффолд для downstream-проектов).

---
<!-- прогресс — дописывать ниже, новое снизу -->

- ✅ Заведены вижены ProjectStarter: `__dev/vision/Vision01__project-starter.md` (зачем скелет +
  инварианты) и `Vision02__cards-layer.md` (слой карточек: NOW-scope + гейтованные FUTURE).
- ✅ Введена папка `__dev/` для разработки шаблона (decisions/tracker/plans/vision); вижены перенесены
  из `__HQ/vision/` (продукт остаётся чистым). Решение записано в `__dev/DECISIONS.md`.
- ✅ `design-open-questions.md` переехал в `__dev/` (dev-документ, не протух); «Meta-aim» поднят в
  Vision01 как инвариант (атомарное правило на любое действие), в open-questions оставлена ссылка.
- ✅ Прояснили таксономию HowTo↔Guide (HowTo = сервисные действия проекта, копятся и линкуются в START;
  Guide = рецепты артефактов схемы); удалён пустой `__HQ/HowTo__Write.md`, расширен START, обобщён скил
  `file-size-and-splits` (убрана memohood-специфика).
- ✅ Большой рефактор именования (D1–D6 в DECISIONS): `__`-маркер меты → `__HQ`/`__map`/`__dev`;
  `__HQ`=мозг (управление+`Guide`-скилы+`__HQ/tools/`), `__map`=плоские данные карт (без `cards/`);
  упразднён тип `Skill`→`Guide`; `helpers/`→`tools/`; правило идентичности путей залочено. Скилы
  мапинга → `__HQ/guides/Guide__MakeCard|AuditCards|BatchCards`; тулы (`check_freshness`, `py_api`,
  `mask_replace`) → `__HQ/tools/`; `file-size-and-splits`→`Guide__SplitLargeFiles`. Все рефы
  переписаны (perl-свип, verify чисто); `check_freshness` дефолты поправлены и проверены на новом
  дереве (карты=`__map`, exit 0). Нейминг подтверждён вслепую на 3 холодных ЛЛМ.
- ✅ Инструменты Vision02 NOW (в `__HQ/tools/`, проверены на живых 83 карточках memohood):
  `check_freshness` — токен-опт (убраны рамки/эмодзи → cp1251-краш ушёл; отставание числом;
  +коммиты, тронувшие исходник после карточки); `rebuild_graph` — плоская топология (модули+сводки+
  deps, точки входа, листья, unresolved-рефы; `--json`); `bundle` — полная карточка цели + Public API
  зависимостей (`--depth`). Все тулы форсируют UTF-8 stdout. Фикстуры в `__HQ/tools/test/graph_cards/`.
- ⚑ Всплыло: 16 не-канонических «From file» в карточках memohood (дотточная нотация `._engine`,
  проза) → часть хабов (напр. `provider.py`) показалась листьями. Долг карточек, не тулов — чинится
  нормализацией по правилу идентичности.
- ✅ Контракт формата карточки залочен: `__HQ/tools/card_format.py` (единый источник) — H1=имя,
  сводка строкой 2; обязательные секции + `(none)`; deps-колонки `Import|File Path|Symbols|Why|Kind`
  (ребро = File Path); **тип карточки** module vs package/node (`## Package layout`); `Re-exports`;
  ALIASES (RU/легаси → канон). `Guide__MakeCard` переписан под контракт. `mask_replace` научен
  escape `\n \t \r \\`.
- ✅ `validate_cards.py` — проверка по контракту (H1==файл · сводка · все секции по типу ·
  deps-таблица/`(none)` · File Path резолвится · private=подсказка · сироты). Чисто на фикстурах
  (module+package); на memohood — worklist: 83/83, unresolved 18, private 27, non-canon 155, ...
- ✅ Майнинг «непрошедших» memohood → 4 находки внесены в контракт: package/node тип + `Package
  layout` (подмодули со ссылками) · re-exports-by-origin · ссылки между карточками · «consumed
  surface» вместо «public surface».
- → next: (d) **механическая миграция карточек memohood** (гардированный `mask_replace`: заголовки/
  колонки RU→канон на якорных строках · H1-split · From-file→File Path). Правит РЕПО memohood массово
  → нужен рекурсивный glob в `mask_replace`; после — ре-валидация, остаток на ручной разбор. Затем
  свод ⚠️ discrepancies + причёсывалка git.
- ✅ Фикс тула: `check_freshness` читает git-вывод как UTF-8 (вскрыто кириллицей коммитов memohood).
- ✅ ВЕХА: memohood переведён на новый скелет (`__HQ`/`__map` + новый тулинг), коммит memohood
  `f60b3f6`; тулы валидированы на живом репо (freshness 83 fresh; rebuild_graph db.py 7, ...). Формат
  карточек memohood ещё легаси (validate: 83/83) → миграция ФОРМАТА = отдельный шаг.
- ✅ memohood: механический проход миграции ФОРМАТА карточек (коммит memohood `7ffec8d`) — H1-split +
  канон общих H2 (legacy-H1 83→0, non-canon 155→1). Остаток НЕ механический = пере-генерация карточек
  под контракт (Role__CodeMap заново по `Guide__MakeCard`) + майнинг — детали в `__dev/CONTEXT_RESTORE.md` Next#1.
- → next (решено, след. сессия): rebuild_graph — развести два вывода: `--json` под визуализатор
  структуры для оператора (дополнить entry-points/leaves/in-degree — сейчас беднее текста, НЕ удалять),
  плоский текст — дотюнить под ЛЛМ. Детали — `__dev/CONTEXT_RESTORE.md` Next#4.
