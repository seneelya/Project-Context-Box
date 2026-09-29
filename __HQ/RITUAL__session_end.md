# RITUAL — end of session (short)

A checklist of QUESTIONS, not a role. Skip what does not apply.

## Check mechanically (not from memory)

```
python __HQ/tools/validate_cards.py
python __HQ/tools/graph_from_cards.py --discrepancies
```

Touched code → its card is restamped in the same pass. The graph catches what memory does not:
a module with no card, an undeclared runtime seam. Both runs take seconds.

Tests are deliberately NOT listed: they run constantly anyway, and the full pass is slow.

## Ask yourself

1. **Did a seam appear that needs a CONTRACT?** A form where TWO sides meet and can diverge
   SILENTLY needs a home → `__HQ/guides/Guide__Contracts_candidate.md` (when to write one, and
   when NOT to freeze it yet).
2. **Anything to defer?** Found along the way, does not fit this work → `__HQ/plans/deferred/`
   (see `__HQ/Role__Plan.md` → Deferring).
3. **Any bug seen but not fixed?** Not "fix" — FILE it (tracker line / `__HQ/OPEN-QUESTIONS.md`),
   while the symptom is still fresh.
4. **Does the system now work DIFFERENTLY?** Then `__HQ/docs/Doc__…` is brought to the truth in
   the same pass. No such doc at all — **create it, don't skip**. No time to fix it — put an
   honest "stale since <date>" line in its header: a lying doc is worse than a missing one,
   because a missing one sends you to the code.
5. **What is still NOT verified live?** Say it out loud; never let it be implied.

## Do

- **TRACKER tail** — what was done → `next …` (facts only).
- **`__HQ/CONTEXT_RESTORE.md`** — prepare it for the next session: what to read, which role, what
  not to do. How to restore → `__HQ/RULE_sessionRestore.md`.
- **Closed tasks/plans** → `__HQ/plans/done/`, with `## CARRY` at the end (lessons, smells,
  do-not-reopen). Move a plan as a FAMILY; a single task only if the owner said so explicitly.
- **A plan still IN PROGRESS, with compaction ahead** — append a `HANDOFF` section: data shape,
  files with line numbers, what not to do. A compaction boundary happens more often than a
  session end.
- **Project version** (if the project has one) — bumped once per session, at the end.
- **TMP/probes** — delete throwaway junk, or keep it with a link from the restore file.
- **Commit** — on meaningful pauses; short messages. **Push only on request.**

## Don't

- Don't open new plans "while we're at it".
- Don't rewrite `Vision` outside the Plan role.
- Don't move anything live code depends on into `done/` (contracts never go there).
