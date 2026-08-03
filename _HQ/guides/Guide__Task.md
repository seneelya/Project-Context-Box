# Guide: Task — the action schema every task follows

A task file (`PlanNN-TaskMM__<slug>.md`, written by the Plan role) is NOT a fill-in form — tasks
differ in content. What every task shares is the **action schema** below. The Plan role shapes the
task around it; the executor (`Role__Exec`) walks it.

> **Language:** keep the structural / action parts in English (like these guides); write the task's
> **creative substance** — the goal, the what & why — in the working language (Russian works better
> there for the model).

**Assume the executor did NOT read the plan.** A task must be self-sufficient — inside the task, put
**direct links to every file the executor must read** to do the work:
- the task's own **`Context`** file (the reading manifest — what to read for this task);
- **`HowTo`** files when relevant → e.g. `read _HQ/HowTo__Test.md`, `read _HQ/HowTo__Run.md`;
- **how to record progress** → `read _HQ/guides/Guide__Tracker.md` (log to the tracker as you go);
- **the parent plan** — if doing this task requires knowing the whole plan, put a **link to the plan
  file** into the read-list. This happens often. Link it — do NOT copy the plan into the task.
- any other file or instruction the task needs that is not already in those.

> Not for the task: `Guide__Context` is the **Plan role's** own instruction on HOW to author a
> `Context` file — it is NOT linked into the task. (Plan role: `read _HQ/guides/Guide__Context.md`.)

## What is `<address>`

`<address>` = the node's coordinate, taken from its file name (the part before `__`).
Example: file `Plan01-Task07__extract.md` → address **`Plan01-Task07`** (Task 07 of Plan 01).
Full addressing rules → naming section in `START.md` and `Role__Exec.md`.

## Action schema

1. **Gather context** — read the task's `Context` (the reading manifest). Nothing more.
2. **Log start** — append to `_HQ/TRACKER.md`: `◐ <address>`.
3. **Solve** the task.
4. **Test** — run / write tests per the task's linked `HowTo__Test`.
5. **Log done** — append `✅ <address> done → next <address>`, noting what was verified: self-tested,
   and user-tested if that was needed.

Keep a task narrow enough to do WITHOUT holding the whole plan in mind.

## Context improves over time

If, after finishing, you realize you needed files that were NOT in your read-list — **append** links
to them at the END of the plan file you read (or the task's `Context` file if you did not read the
plan). This is the improve-over-time loop from `Guide__Context`: the next run reads better.
Just append — do not rewrite.
