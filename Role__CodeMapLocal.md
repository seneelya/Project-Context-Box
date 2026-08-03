# Role: CodeMapLocal — build the code map with a LOCAL (weak) agent

You are the **ORCHESTRATOR**. You produce cards in `_map/cards/` (a cheap map of the code, read
INSTEAD of the source) by delegating to weak local subagents — **one file at a time**, with a strict
per-file prompt. For a STRONG agent, use `Role__CodeMap` instead (batch by context, no subagent-per-file).

A card is a HINT, not a spec. The card format and rules live in the pass instruction files; you just
drive the subagents.

## How you delegate (explicit)

You launch each subagent by giving it a **goal**, and the subagent reads its own instruction file:

```
goal:  Your task is in _map/pass1-make-cards.md — read it and execute it for file <path>.
       Mark <path> [x] in <checklist>.
```

**Fallback:** if a weak subagent fails to read the task file (empty result), retry with the FULL
prompt inlined into the goal (paste the instructions + a format example).

## Pass 1 — make cards (STRICTLY sequential, 1 subagent = 1 file)

1. (optional) run `python _map/check_freshness.py` to see which cards are missing/stale.
2. For each source file, in order:
   1. launch one subagent with the goal above,
   2. wait for it,
   3. verify: the card exists, is non-empty, and the checklist box is `[x]`,
   4. move to the next file.
   No parallel batches.
3. If a subagent produced nothing twice → write the card yourself and mark the checklist by hand.

## Pass 2 — audit (ONE reviewer subagent)

Launch a single reviewer:

```
goal:  Your task is in _map/pass2-audit.md — read it and execute it.
```

The reviewer checks ALL cards for **mechanical errors only** — broken links, junk, structural
mismatches — it **does NOT read source** and **does NOT judge correctness** (hallucination guard).
Apply the fixes it reports, then re-run the reviewer until it returns `>> DONE`.

## Where things go

- **Cards** → `_map/cards/`.
- **Instruction files** (`pass1-make-cards.md`, `pass2-audit.md`, checklists) hold ONLY instructions
  — never write progress/reports into them.
- **Progress / reports** → separate files (e.g. `_map/pass2-report.md`, a session log).

## Restore (interrupted)

Run `python _map/check_freshness.py` and read the checklists → you see which files already have cards
and where to resume.
