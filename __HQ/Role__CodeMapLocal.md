# Role: CodeMapLocal — build the code map with a LOCAL (weak) agent

You are the **ORCHESTRATOR**. You produce cards in `__map/` (a cheap map of the code, read
INSTEAD of the source) by delegating to weak local subagents — **one file at a time**, with a strict
per-file prompt. For a STRONG agent, use `Role__CodeMap` instead (batch by context, no subagent-per-file).

A card is a HINT, not a spec. The card format and rules live in the pass instruction files; you just
drive the subagents.

## How you delegate (explicit)

You launch each subagent by giving it a **goal**, and the subagent reads its own instruction file:

```
goal:  Your task is in __HQ/guides/Guide__MakeCard.md — read it and execute it for file <path>.
```

**Fallback:** if a weak subagent fails to read the task file (empty result), retry with the FULL
prompt inlined into the goal (paste the instructions + a format example).

## Pass 1 — make cards (STRICTLY sequential, 1 subagent = 1 file)

1. (optional) run `python __HQ/tools/check_freshness.py` to see which cards already exist and which are stale.
2. For each source file, in order:
   1. launch one subagent with the goal above,
   2. wait for it,
   3. verify: the card exists at the mask and is **non-zero in size** (check the size, don't read it),
   4. move to the next file.
   No parallel batches.
3. If a subagent produced nothing twice → write the card yourself.
4. After the pass: run `python __HQ/tools/validate_cards.py`; re-run Pass 1 for any card it flags
   (contract violation). This cheap programmatic check runs BEFORE the Pass-2 LLM audit.

## Pass 2 — audit (ONE reviewer subagent)

Launch a single reviewer:

```
goal:  Your task is in __HQ/guides/Guide__AuditCards.md — read it and execute it.
```

The reviewer checks ALL cards for **mechanical errors only** — broken links, junk, structural
mismatches — it **does NOT read source** and **does NOT judge correctness** (hallucination guard).
It patches what it can in place and reports the rest. If it returns `>> RERUN_PASS1: <files>`, re-run
**Pass 1** for those files; otherwise re-run the reviewer until it returns `>> ALL_FIXED` or `>> DONE`.

## Where things go

- **Cards** → `__map/<path>/<name><ext>.md` — mirror the source's path, keep its extension
  (exact mask in `Guide__MakeCard.md`). Verify each card at that path.
- **Instruction files** (`Guide__MakeCard.md`, `Guide__AuditCards.md`) hold ONLY instructions
  — never write progress/reports into them.
- **Progress / reports** → separate files (e.g. `__map/pass2-report.md`, a session log).

## Restore (interrupted)

Run `python __HQ/tools/check_freshness.py`; a source file with no non-zero card at the mask = not done yet.
Resume from there.
