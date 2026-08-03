# TRACKER — tail log (read only the TAIL)

**Rule:** append ONE line per step to the BOTTOM, newest last. To learn where we are, read only the
**last few lines** — never the whole file.

**Line format:**
- `✅ <address> done → next <address>` — a step finished, and what to take next
- `◐ <address>` — in progress
- `⏸ <address> — <why>` — blocked / parked

An optional compact **phase map** may sit at the top (it changes rarely); the moving state is the log below.

---
<!-- progress log — append below, newest last -->
