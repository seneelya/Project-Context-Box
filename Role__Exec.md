# Role: Exec — execute one task

You are EXECUTING. Take ONE task, do it, record progress. Read ONLY what the task needs —
NOT the vision, NOT the whole codebase.

## Get your task

- From the user's explicit words ("do Task X", "implement Y"), OR
- From the **TAIL** of `_hq/TRACKER.md` (last lines = where we stopped → what's next).
- Unclear which task? **ASK the user**, then proceed.

## Read only what you need (scoped)

1. Open the task file `_hq/plans/<Plan>__<slug>/<Plan>-Task<NN>__<slug>.md` — goal, in→out contract, steps.
2. Read its **Context** (`<Plan>-Context__…` file, or the plan's context section). This is a
   **compiled reading manifest** written by the planner — read exactly what it lists, no more:
   - Inline facts → use them, do NOT re-look-up. Named zones → read only those files.
   - Manifest insufficient? **STOP and ask/report — do NOT blind-search the repo.**
3. Need to run or test? → read `_hq/HowTo__Run.md` / `_hq/HowTo__Test.md`.
   Empty / missing? → switch to `Role__EnvSetup` first (or ask the user).
- You do NOT need `_hq/vision/` or sibling plans. Skip them.

## Do it

- Follow the task's decomposed steps in order (they are sized for your grade).
- Edit source (`*.py`, `*.cpp`, `*.ts`, …) → in the SAME pass update its card in `_map/cards/`.
- Keep the trunk green: small, verifiable steps.

## Track progress

- Log to the **TAIL** of `_hq/TRACKER.md`: `◐ <address>` when you START, then
  `✅ <address> done → next <address>` when finished.
- **Outcome note — only to cross a context boundary.** Write a short **Outcome** note INTO the
  task file ONLY if the next task's executor would MISS it otherwise: a tacit decision / constraint /
  gotcha that is NOT visible in the code they will read. If you continue to the next task yourself
  now (same context), you already know it → write nothing. If it is already reflected in the code /
  interfaces → write nothing. Unsure whether anyone will need it later? → **ASK the user.**
  Default: write nothing (rarely-but-precisely).
- Whole plan finished → move the family (`<Plan>__…md` + its `<Plan>__…/` folder) to `_hq/plans/done/`.

## Restore (interrupted)

1. **TAIL** of `_hq/TRACKER.md` → which task you were on.
2. The task file + `git status` → what is half-done.
3. Decide: continue if it is clear; else roll back the uncommitted changes and restart the task.
   Unsure → **ask the user**.

## Naming & addressing (full rules)

File name = **address + human name**: `<Tag><N>[-<Tag><N> …]__<slug>.md`.
Parse: `split("__")[0].split("-")` → address levels; the rest is the human slug (may contain `-`).

- **Separators:** `__` = address↔slug · `-` = between coordinates (tree levels) · `.` = generation of a node.
- **Self-addressing:** the name carries the FULL address (`Plan01-Task07__extract.md`), never derived
  from the folder path — so grepping the address finds the file directly.
- **Tags:** `Plan` · `Task` · `Context` · `Vision` · `Role` · `HowTo` · `Guide`.
- **Fractal node:** any node = `<addr>__<slug>.md` (+ a same-named folder for its children — created
  ONLY when there are many; otherwise children sit as flat files beside it). A **subtask** is a child
  with a bare trailing number: `Plan01-Task08-1__<slug>.md` (rare — if it needs real splitting, make
  it a separate task).
- **Status by folder (whole chain):** active in `_hq/plans/`; finished → `_hq/plans/done/`;
  replaced → `_hq/plans/superseded/`. The address (file name) never changes when a family moves.
- **Generations:** an address is IMMORTAL within its generation. A genuine rework = a NEW plan
  `Plan01.2` with its OWN tasks (`Plan01.2-Task01…`) + frontmatter `supersedes: Plan01`; the old
  chain moves to `superseded/`. A small text edit is just git — same address.
