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
3. Open the role file (`__HQ/Role__*.md`) and follow it strictly — it holds both the method
   and how to restore context for exactly that role.

## Roles

| Role file (in `__HQ/`) | When you take it — the user says… |
| --- | --- |
| **`__HQ/Role__Plan.md`** | "let's plan", "write the vision", "make a plan", "how should this work" |
| **`__HQ/Role__Exec.md`** | "do the task", "continue", "your task was …", "implement …" |
| **`__HQ/Role__CodeMap.md`** | "let's understand the project", "build the map / cards", "what's this code" |
| **`__HQ/Role__CodeMapLocal.md`** | you are a **local agent** and we are building the project map |
| **`__HQ/Role__EnvSetup.md`** | "set up the environment", "how to run / test this", taking a new/foreign project |
| **`__HQ/Role__Doc.md`** | "the plan is done, update the docs", "reconcile the as-built docs", "document what changed" |
| **`__HQ/Role__Recon.md`** | "investigate/map how [the foreign system] does X", "research the target system", "how does <host app> handle …" |

**Restoring** ("we stopped at …", "continue") → first open **`CONTEXT_RESTORE.md`**. If you were in
the **Recon** role, its own journal `__HQ/recon/CONTEXT_RESTORE_RECON.md` is the more specific entry
point — that role accumulates state outside the tracker.

## Universal rules (language-independent)

- Edit a source file (`*.py`, `*.cpp`, `*.ts`, `*.go`, …) → in the SAME pass update its card in
  `__map/` (cards are a cheap map of the code instead of reading the source).
- Record progress by **appending to the TAIL** of `__HQ/TRACKER.md` (`✅ done … → next …`); when
  reading, look only at the **TAIL** (last lines = where we are).

## Naming system (universal)

A file name encodes **address + human-readable name**:

```
<Tag><N>[-<Tag><N> …]__<name>.md
```
Examples: `Plan01__lab.md` (Plan 01) · `Plan01-Task07__extract.md` (Task 07 of Plan 01, topic "extract").

Tags: **`Plan`** · **`Task`** (a plan's step) · **`Context`** (what to read for a task) ·
**`Vision`** (intent/design) · **`Doc`** (how the system works NOW / as-built) · **`Role`** ·
**`HowTo`** (how to do a recurring project action — run/test/build, or how to write the project's own kind of program) · **`Guide`** (authoring recipe).
Full addressing rules — in your role file.

## Where things live (map — don't load extra)

- **Code map** → `__map/` — compact per-file cards (descriptive headers). **Read these INSTEAD
  of the source** to understand code cheaply. Missing a card? → the **CodeMap** role builds it.
- **Dev tools (your hands)** → `__HQ/tools/` — small CLIs (reverse usage index, code blocks, the
  card stamp, …). Catalog + how to run → **`__HQ/tools/TOOLS.md`** (router: pick a tool by task,
  then read its `<name>__TLDR.md`). Prefer them over reading whole files.
- **Plans and tasks** → `__HQ/plans/` (active); closed → `done/` / `superseded/`; deferred → `deferred/` (all under `__HQ/plans/`).
- **Plan index** → `__HQ/plans/INDEX.md` — catalog of all plans, one line each (+ rough status). What plans exist at a glance; maintained by the **Plan** role.
- **Settled decisions** → `__HQ/DECISIONS.md` — locked calls + one-line why; **read before (re)designing, don't relitigate**. Owned by the **Plan** role.
- **Lessons from closed plans** → grep `^## CARRY` in `__HQ/plans/done/` (deviations · smells · next-gen TODO — jump to the line, don't read whole plans). **Open contract-drift** → grep `KICKBACK` in `__HQ/` (Exec kicked a wrong contract back to Plan).
- **Context restore** → `CONTEXT_RESTORE.md` + the TAIL of `__HQ/TRACKER.md`.
- **How the whole scheme works** (roles, flow, naming — the big picture) → `__HQ/WORKFLOW.md`. Read this to understand how the project is organised.
- **Intent / design (product)** → `__HQ/vision/` — WHY this *product* should work as it does; needed by the **Plan** role; NOT by a task executor.
- **As-built docs** → `__HQ/docs/` — how the system works **NOW** (where things live, example configs, the real flow). A landed plan's lasting consequence, reconciled by the **Doc** role.
- **How to run / test / build — and how to write this project's own recurring programs** →
  `__HQ/HowTo__<Action>.md` (`HowTo__Run`, `HowTo__Test`, …). Recurring, project-specific SERVICE docs
  that **accumulate as the project grows**: run/test/build are written by `Role__EnvSetup`; *authoring*
  HowTos (e.g. "how to write a module/harness of this project's kind", for weak local models to follow)
  emerge once such a pattern stabilises. Distinct from `__HQ/guides/` (recipes for the SCHEME's own
  artifacts). **Link each new HowTo here in START** as it appears.
- **Authoring recipes** → `__HQ/guides/` — how to shape a Plan / Task / Context (used by the Plan role).
- **Investigating the foreign system** (the thing we're embedding into, not our own code) → `__HQ/recon/`
  — verified facts about it, each with a reproduction path; per-subject raw data/tooling in
  `recon/subjects/`. Owned by the **Recon** role. Not Vision (ours, should-be) or Doc (ours, as-built) —
  a third tense: THEIRS, as-observed.
- **Open questions bridging recon ↔ product** → `__HQ/OPEN-QUESTIONS.md` — live discussion of what a
  recon finding implies for our design, not yet a settled call. Resolves into `DECISIONS.md` (our
  choice) or `recon/DECISIONS-RECON.md` (their settled fact).

---

Bootstrap (copying this skeleton into an empty/foreign folder) is a **manual action by the owner**, not a role.
