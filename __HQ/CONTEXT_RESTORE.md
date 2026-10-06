# CONTEXT_RESTORE — you are resuming

You (or a previous you) were interrupted. This file gets you back on track. It is a **REDIRECT** —
the real restore method lives per-role.

## Steps

1. Open the newest **entry file** in the folder `__HQ/TRACKER/` (skip `0000__rule.md`)
   → what was being done and what is next. There is no `TRACKER.md`.
2. Which role were you in? (`Plan` / `Exec` / `CodeMap` / `CodeMapLocal` / `EnvSetup` / `Doc`.)
   Unclear → check `__HQ/START.md`, or ask the user.
3. Open that role file (`__HQ/Role__*.md`) and follow its **Restore** section.
   A role may keep its own journal for state the tracker doesn't hold: `__HQ/CONTEXT_RESTORE_<ROLE>.md`
   (project-owned, the template never ships one; Recon's lives at `__HQ/recon/CONTEXT_RESTORE_RECON.md`).
   One exists for your role → read it right after the role file.
4. Check `git status` → what is half-done. Decide: continue if it is clear, else roll back the
   uncommitted changes and restart that unit. Unsure → **ask the user**.

Do NOT re-litigate settled decisions. Do NOT blind-read the whole repo — restore from the tail up.
How to read big files while restoring (outline → block, never whole) → `__HQ/RULE_sessionRestore.md`.
