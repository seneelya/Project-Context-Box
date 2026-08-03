# Batch — make cards for a LIST of source files

You are a strong documentation subagent. The orchestrator gave you a **LIST of source files** (sized to
your context) and this file. Produce **ONE card per file** in your list — do the whole list in this one pass.

**The card format, the rules, and the exact path mask are in `_map/pass1-make-cards.md` — read it FIRST
and follow it for every file.** In short: a card is a HINT not a spec, facts from the code only, and it
mirrors the source path under `_map/cards/` keeping the extension:
`_map/cards/<path>/<name><ext>.md`.

## Steps

1. Read `_map/pass1-make-cards.md` (the card spec).
2. For EACH file in your assigned list:
   1. read the source file,
   2. write its card at the mask path.
3. Report: how many cards written, and any file you could not do (with the reason).

Do NOT process files outside your list — those belong to other subagents.
