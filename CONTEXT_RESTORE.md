# CONTEXT_RESTORE — you are resuming

You (or a previous you) were interrupted. This file gets you back on track. It is a **REDIRECT** —
the real restore method lives per-role.

## Steps

1. Read the **TAIL** of `_HQ/TRACKER.md` (last lines) → what was being done and what is next.
   If `TRACKER2.md` / `TRACKER3.md` … exist, read the tail of the **highest-numbered** one.
2. Which role were you in? (`Plan` / `Exec` / `CodeMap` / `CodeMapLocal` / `EnvSetup` / `Doc`.)
   Unclear → check `START.md`, or ask the user.
3. Open that role file (`_HQ/Role__*.md`) and follow its **Restore** section.
4. Check `git status` → what is half-done. Decide: continue if it is clear, else roll back the
   uncommitted changes and restart that unit. Unsure → **ask the user**.

Do NOT re-litigate settled decisions. Do NOT blind-read the whole repo — restore from the tail up.
