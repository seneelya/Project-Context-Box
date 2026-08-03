# Guide: Task — the action schema every task follows

A task file (`PlanNN-TaskMM__<slug>.md`, written by the Plan role) is NOT a fill-in form — tasks
differ in content. What every task shares is the **action schema** below. The Plan role shapes the
task around it; the executor (`Role__Exec`) walks it.

**Assume the executor did NOT read the plan.** A task must be self-sufficient — put **direct links**
to everything it needs right inside the task:
- how to assemble context for task agent → `read _hq/guides/Guide__Context.md` + the task's own `Context` file;
- how to test / run (when relevant) → `read _hq/HowTo__Test.md` / `read _hq/HowTo__Run.md`;
- any other file or instruction the task needs that is not already in those.

If the executor needs the parent plan, add a **link to the plan** — do NOT copy the plan into the task.

## Action schema

1. **Gather context** — read the task's `Context` (the reading manifest). Nothing more.
2. **Log start** — append to `_hq/TRACKER.md`: `◐ <address>`.
3. **Solve** the task.
4. **Test** — run / write tests per the task's linked `HowTo__Test`.
5. **Log done** — append `✅ <address> done → next <address>`, noting what was verified: self-tested,
   and user-tested if that was needed.

Keep a task narrow enough to do WITHOUT holding the whole plan in mind.
