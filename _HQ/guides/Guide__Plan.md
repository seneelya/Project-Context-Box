# Guide: Plan — how to shape a plan (recommendations)

A plan is **detailed** — it is the instruction of what to do for a whole app or an important part of it.

It contains: **goal · scope · in→out contracts** (treat an unsolved hard part as a BLACK BOX with a
contract, fill it later) · **acceptance criteria** · a **cross-check** against existing plans
(`_HQ/plans/*__*.md`) so you don't overlap or conflict.

When you **decompose into tasks**: for each task, write its **context-assembly instruction** into the
`Context` file the task will reference (`PlanNN-Context__<slug>.md`), **or a section of the plan** for a
small/shared context — `read _HQ/guides/Guide__Context.md`.
That is where "what to read to do this" lives, so the executor never blind-searches.

**Tracking:** in the plan (and in each task) add a short pointer to `_HQ/guides/Guide__Tracker.md`,
so progress is logged to the tracker as work proceeds.

**Generations:** a genuine rework → a new plan `PlanNN.K` with its own tasks (`supersedes:`); the old
family moves to `_HQ/plans/superseded/`. Addresses are immortal; a small edit is just git.

Frontmatter (only when superseding — a fresh plan needs none):

```markdown
---
supersedes: Plan01        # the NEW plan names what it replaces
superseded_by: Plan01.2   # the OLD plan names its replacement (added when it moves to superseded/)
---
```

**Deferring:** postpone a plan/task out of the active flow → move its family to `_HQ/plans/deferred/`
(not a tracker `⏸` pause). Promote back to active when picked up.
