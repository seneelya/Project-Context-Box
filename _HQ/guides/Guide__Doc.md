# Guide: Doc — as-built docs (how the system works NOW)

A `Doc` file (`_HQ/docs/Doc__<slug>.md`) describes **how the system actually works right now** — the
lasting consequence of landed plans. Written by the **Plan** role (it holds the whole picture; the weak
executor does not). Distinct from its neighbours:

- **Vision** = WHY / how it *should* work (intent).  **Doc** = how it *does* work (reality).
- **Cards** (`_map/cards/`) = per-file mechanical map.  **Doc** = the woven, cross-cutting picture.

## What goes in

Practical, current facts a newcomer (human or agent) needs to operate the system:
- where things live now (configs, entry points, data) — with a concrete **example**;
- the real end-to-end **flow** (A → B → C);
- what replaced what (module Y now does the job Z used to).

Facts, not plans or intent. If a statement stops being true, fix it (git keeps the history).

## Shape

One `Doc__<slug>.md` per coherent area (`Doc__config.md`, `Doc__pipeline.md`, …). Keep it short and
current; a small change is a couple of edited lines, a big new capability is a new `Doc`.
