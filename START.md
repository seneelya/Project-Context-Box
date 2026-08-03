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
3. Open the role file (`Role__*.md`, in the root) and follow it strictly — it holds both the method
   and how to restore context for exactly that role.

## Roles

| Role file (root) | When you take it — the user says… |
| --- | --- |
| **`Role__Plan.md`** | "let's plan", "write the vision", "make a plan", "how should this work" |
| **`Role__Exec.md`** | "do the task", "continue", "your task was …", "implement …" |
| **`Role__CodeMap.md`** | "let's understand the project", "build the map / cards", "what's this code" |
| **`Role__CodeMapLocal.md`** | you are a **local agent** and we are building the project map |
| **`Role__EnvSetup.md`** | "set up the environment", "how to run / test this", taking a new/foreign project |

**Restoring** ("we stopped at …", "continue") → first open **`CONTEXT_RESTORE.md`**.

## Universal rules (language-independent)

- Edit a source file (`*.py`, `*.cpp`, `*.ts`, `*.go`, …) → in the SAME pass update its card in
  `_map/cards/` (cards are a cheap map of the code instead of reading the source).
- Record progress by **appending to the TAIL** of `_hq/TRACKER.md` (`✅ done … → next …`); when
  reading, look only at the **TAIL** (last lines = where we are).

## Naming system (universal)

A file name encodes **address + human-readable name**:

```
<Tag><N>[-<Tag><N> …]__<name>.md
```
Examples: `Plan01__lab.md` (Plan 01) · `Plan01-Task07__extract.md` (Task 07 of Plan 01, topic "extract").

Tags: **`Plan`** · **`Task`** (a plan's step) · **`Context`** (what to read for a task) ·
**`Vision`** (intent/design) · **`Role`** · **`HowTo`** (how to run/test) · **`Guide`** (authoring recipe).
Full addressing rules — in your role file.

## Where things live (map — don't load extra)

- **Code map** → `_map/cards/` — compact per-file cards (descriptive headers). **Read these INSTEAD
  of the source** to understand code cheaply. Missing a card? → the **CodeMap** role builds it.
- **Plans and tasks** → `_hq/plans/` (active); closed → `done/` / `superseded/`; deferred → `deferred/` (all under `_hq/plans/`).
- **Context restore** → `CONTEXT_RESTORE.md` + the TAIL of `_hq/TRACKER.md`.
- **Intent / design** → `_hq/vision/` — needed by the **Plan** role; NOT by a task executor.
- **How to run / test** → `_hq/HowTo__Run.md`, `_hq/HowTo__Test.md`, … (written by `Role__EnvSetup`,
  read by the others).
- **Authoring recipes** → `_hq/guides/` — how to shape a Plan / Task / Context (used by the Plan role).

---

Bootstrap (copying this skeleton into an empty/foreign folder) is a **manual action by the owner**, not a role.
