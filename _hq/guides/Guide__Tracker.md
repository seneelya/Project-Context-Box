# Guide: Tracker — how to fill and read the tracker

The tracker (`_hq/TRACKER.md`) is a **tail log** of execution progress, kept **separate** from plans
and tasks.

**Read:** only the **TAIL** (last few lines) — that is where we are. Never read the whole file.

**Write:** append ONE line per step to the BOTTOM, newest last:
- `◐ <address>` — in progress
- `✅ <address> done → next <address>` — a step finished + what to take next
- `⏸ <address> — <why>` — blocked / parked

`<address>` = the node coordinate from a file name, e.g. `Plan01-Task07` (see `Guide__Task`).

**Rotation:** when the file grows too large, start `TRACKER2.md`, `TRACKER3.md`, … and read the TAIL
of the latest one.

An optional compact **phase map** may sit at the top of the tracker (it changes rarely); the moving
state is the appended log.
