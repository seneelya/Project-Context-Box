# Guide: Context — the reading manifest (what to read for a task)

A `Context` file is the **instruction for assembling context** for a task — the LIST of what to read
to do the work. The **Plan** role compiles it (it holds the knowledge now); the executor consumes it
and reads little, never blind-searching.

**Prefer cards over source.** List the relevant `__map/*.md` FIRST — the executor reads those
cheap descriptive headers INSTEAD of the source. Point to actual source only when the card is not enough.

Fill it as a LIST:
- **Cards to read** → `__map/…` (preferred — read these first).
- **Code files** → the few source files the task truly touches.
- **Docs** → the `.md` files that matter (a design note, another plan, a `HowTo__…`).
- **Facts you KNOW** → inline them (the executor then reads nothing for those).
- **Zones you are UNSURE about** → point coarsely ("explore here: `dir/…`"); do NOT fake `§`-precision.

**"Read only this."** If the manifest is insufficient, the executor STOPS and asks — no blind search.
It **improves over time**: an executor that hits a gap appends what was missing → the next run is sharper.
