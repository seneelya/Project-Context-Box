# START — entry point: name your role → read its file

> You just entered a project on the **ProjectStarter** skeleton and you are nearly empty — you have
> no context yet. Your **ROLE is set by the USER** (by what you are doing together). Find your role
> in the list below, open its file, then act by it.
>
> ⚠️ **Don't know your task/role? — ASK the user** ("what is my task?"), get the answer, and come
> back to this file.

## How to use (step by step)

1. From the user's words, pick the role from the table (look at "when you take it" — meaning-aliases).
2. None fits / unclear → **ask the user**, return to step 1.
3. Open the role file (`_HQ/Role__*.md`) and follow it strictly — it holds both the method
   and how to restore context for exactly that role.

## Roles

| Role file (in `_HQ/`) | When you take it — the user says… |
| --- | --- |
| **`_HQ/Role__Plan.md`** | "let's plan", "write the vision", "make a plan", "how should this work" |
| **`_HQ/Role__Exec.md`** | "do the task", "continue", "your task was …", "implement …" |
| **`_HQ/Role__CodeMap.md`** | "let's understand the project", "build the map / cards", "what's this code" |
| **`_HQ/Role__CodeMapLocal.md`** | you are a **local agent** and we are building the project map |
| **`_HQ/Role__EnvSetup.md`** | "set up the environment", "how to run / test this", taking a new/foreign project |
| **`_HQ/Role__Doc.md`** | "the plan is done, update the docs", "reconcile the as-built docs", "document what changed" |

**Restoring** ("we stopped at …", "continue") → first open **`CONTEXT_RESTORE.md`**.

## Universal rules (language-independent)

- Edit a source file (`*.py`, `*.cpp`, `*.ts`, `*.go`, …) → in the SAME pass update its card in
  `_map/cards/` (cards are a cheap map of the code instead of reading the source).
- Record progress by **appending to the TAIL** of `_HQ/TRACKER.md` (`✅ done … → next …`); when
  reading, look only at the **TAIL** (last lines = where we are).

## Naming system (universal)

A file name encodes **address + human-readable name**:

```
<Tag><N>[-<Tag><N> …]__<name>.md
```
Examples: `Plan01__lab.md` (Plan 01) · `Plan01-Task07__extract.md` (Task 07 of Plan 01, topic "extract").

Tags: **`Plan`** · **`Task`** (a plan's step) · **`Context`** (what to read for a task) ·
**`Vision`** (intent/design) · **`Doc`** (how the system works NOW / as-built) · **`Role`** ·
**`HowTo`** (how to run/test) · **`Guide`** (authoring recipe).
Full addressing rules — in your role file.

## Where things live (map — don't load extra)

- **Code map** → `_map/cards/` — compact per-file cards (descriptive headers). **Read these INSTEAD
  of the source** to understand code cheaply. Missing a card? → the **CodeMap** role builds it.
- **Plans and tasks** → `_HQ/plans/` (active); closed → `done/` / `superseded/`; deferred → `deferred/` (all under `_HQ/plans/`).
- **Plan index** → `_HQ/plans/INDEX.md` — catalog of all plans, one line each (+ rough status). What plans exist at a glance; maintained by the **Plan** role.
- **Settled decisions** → `_HQ/DECISIONS.md` — locked calls + one-line why; **read before (re)designing, don't relitigate**. Owned by the **Plan** role.
- **Lessons from closed plans** → grep `^## CARRY` in `_HQ/plans/done/` (deviations · smells · next-gen TODO — jump to the line, don't read whole plans). **Open contract-drift** → grep `KICKBACK` in `_HQ/` (Exec kicked a wrong contract back to Plan).
- **Context restore** → `CONTEXT_RESTORE.md` + the TAIL of `_HQ/TRACKER.md`.
- **How the whole scheme works** (roles, flow, naming — the big picture) → `_HQ/WORKFLOW.md`. Read this to understand how the project is organised.
- **Intent / design (product)** → `_HQ/vision/` — WHY this *product* should work as it does; needed by the **Plan** role; NOT by a task executor.
- **As-built docs** → `_HQ/docs/` — how the system works **NOW** (where things live, example configs, the real flow). A landed plan's lasting consequence, reconciled by the **Doc** role.
- **How to run / test** → `_HQ/HowTo__Run.md`, `_HQ/HowTo__Test.md`, … (written by `Role__EnvSetup`,
  read by the others).
- **Authoring recipes** → `_HQ/guides/` — how to shape a Plan / Task / Context (used by the Plan role).

---

Bootstrap (copying this skeleton into an empty/foreign folder) is a **manual action by the owner**, not a role.
