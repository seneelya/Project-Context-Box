# Scheme — open questions (ProjectStarter itself)

Unsettled questions about the SCHEME (not any product). Captured as they surface while running the
scheme on a real project (memohood). Resolve deliberately, not at session-end.

## 1. `superseded/` confuses — probably park it

Our model is **iterative**: plan → build → **check → correct** (next generation). A closed plan is
**done** (a delivered increment), NOT *obsolete* — even when a later generation refines it. So
`superseded/` (which reads as "outdated") sends the wrong signal for the common case.

- **Proposal:** park `superseded/`. Live on `done/` (delivered increments) + `deferred/` (out of flow).
  A next generation `PlanNN.K` **links to its predecessor** (`follows:` / `refines:`) instead of
  marking it superseded; the predecessor stays in `done/`.
- Keep `superseded/` (or reintroduce) ONLY for a plan abandoned **before** delivery — rare. Until that
  case is real, dropping it removes noise.
- First real instance: memohood `Plan01` (lab, first increment) → `done/`; next is `Plan01.01`
  (iteration), and calling `Plan01` "superseded" felt wrong.

## 2. Generation semantics: rework vs iteration

Two different things the current scheme conflates under "supersede":
- **rework** — the plan was WRONG → replace it (the superseded case).
- **iteration** — the plan was DELIVERED, the next generation extends/corrects it (our norm).
The scheme should name these distinctly (link verbs: `supersedes:` vs `follows:`/`refines:`).

## 3. Branching problem (anticipated, unsolved)

When a plan spawns **variants/branches** (not a linear "next generation"), addressing (`PlanNN.K`) and
status-folders may get messy. Watch for it on a real case before designing a fix.

## Why these matter

The atomic-rule aim (for every action a path to an atomic rule; a gap = the signal to add one) is a
scheme invariant — see `_dev/vision/Vision01__project-starter.md`. This file is where the gaps it
exposes get parked until resolved.
