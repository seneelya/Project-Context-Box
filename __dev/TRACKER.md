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
- → next: токен-опт вывода `check_freshness` (эмодзи `📂`/полосы `===` → cp1251-краш + шум для ЛЛМ);
  затем инструменты Vision02 NOW — `rebuild_graph` (плоская топология) и `bundle`.
