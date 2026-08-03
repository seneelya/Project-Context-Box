# Guide: Task — how to shape a task (recommendations, not a rigid template)

Tasks differ; what is constant is the **action schema**. A task file
(`PlanNN-TaskMM__<slug>.md`, written by the Plan role) carries: a short **goal**, a pointer to its
**Context**, and steps that follow this schema. The executor (`Role__Exec`) then walks it:

1. **Gather context** — read the task's `Context` (the reading manifest). Nothing more.
2. **Log start** — append to `_hq/TRACKER.md`: `◐ <address>`.
3. **Solve** the task.
4. **Test** — run tests / write tests (see `_hq/HowTo__Test.md`).
5. **Log done** — append `✅ <address> done → next <address>`, noting what was verified: self-tested,
   and user-tested if that was needed.

Keep a task narrow enough to do WITHOUT holding the whole plan in mind. This is a recipe of
**actions**, not a fill-in form — the content is yours.
