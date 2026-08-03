# TRACKER — tail log (read only the TAIL)

**Rule:** append ONE line per step to the BOTTOM, newest last. To learn where we are, read only the
**last few lines** — never the whole file.

**Line format:**
- `✅ <address> done → next <address>` — a step finished, and what to take next
- `◐ <address>` — in progress
- `⏸ <address> — <why>` — blocked / parked

An optional compact **phase map** may sit at the top (it changes rarely); the moving state is the log below.

**Rotation:** when this file grows too large, start `TRACKER2.md`, `TRACKER3.md`, … and read the
TAIL of the latest one. Execution progress is tracked HERE, separately from plans/tasks.

---
<!-- progress log — append below, newest last -->
