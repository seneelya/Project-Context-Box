# RULE — restoring context at the start of a session

A rule, not a memo: breaking it spends the context you will need for the work.

## Markdown is read by OUTLINE, then by BLOCK — never whole

Our docs grow large (`TRACKER.md` reaches thousands of lines; plans and contracts run 400–800).
Reading one in full to reach one section spends on scouting what was meant for the work.

```
python __HQ/tools/get_codeblock.py --file <file.md> --outline --level 2   # what is inside
python __HQ/tools/get_codeblock.py --file <file.md> --line <N> --query    # fetch that block
```

`--query` is the normal way to FETCH, better than reading by line range: when the block is small
it also pulls a bit of the neighbouring zone (capped ~40 lines), so context does not get cut
mid-thought.

**Do not pipe it through `| tail 40` or `| head`.** The tool already caps its own output — that
protection is built in. Piping only cuts the ANSWER, and usually the part that mattered.

Trap: `--query` with several `--line` on a huge file can return the whole thing. Past ~1000
lines, outline first, then one block at a time.

Only the entry files (`__HQ/START.md`, `__HQ/CONTEXT_RESTORE.md`) are read in full — they are
short and exist to say where to go next.

## Order

1. `__HQ/START.md` — in full. Name your role from the owner's words.
2. `__HQ/CONTEXT_RESTORE.md` — in full.
3. **TAIL** of `__HQ/TRACKER.md` — the last lines, not the file.
   If `TRACKER2.md`… exist, the tail of the highest number.
4. Your role file (`__HQ/Role__*.md`), its Restore section.
5. `git status` / `git log` — what is half-done, in EACH repo involved (the sources and, if it has
   its own, the HQ). Uncommitted work may be someone ELSE's: a project can have more than one
   agent. Do not claim it and do not roll it back.
6. Topic docs in `__HQ/docs/`, by outline.

## Map before code

Cards in `__HQ/__map/` are read INSTEAD of sources — cheaper, and they show more than the task.

```
python __HQ/tools/graph_from_cards.py --file <file>     # slice around one file
python __HQ/tools/graph_from_cards.py --discrepancies   # map vs reality
```

The graph shows **every link declared in the cards, import and runtime alike**. What it cannot
do is DISCOVER a runtime link: the card stamp leaves the `## Runtime seams` zone, and filling
it — by-path loading, HTTP between halves, a file shared by two processes — is your job, on the
CONSUMING side's card. Declared once, it is on the map forever.

A full `--view tree` is not a per-session ritual: it pays off when entering an unfamiliar part
of the project, and adds almost nothing on a narrow task.

## Don't

- Don't read the repo blind. Restore from the tail upwards, not from the root down.
- Don't reopen settled calls (`__HQ/DECISIONS*.md`, "do not reopen" sections).
- Don't infer the TASK from restore files. They say where we stopped; what to do now is the
  owner's to say. Unclear — ask in one line instead of scouting.
- Don't read what a context manifest explicitly lists as "do not read".

## Links

- `__HQ/START.md` — entry and roles · `__HQ/CONTEXT_RESTORE.md` — redirect.
- `__HQ/RITUAL__session_end.md` — the other side: what to leave behind.
- `__HQ/tools/TOOLS.md` — which tool for which task.
