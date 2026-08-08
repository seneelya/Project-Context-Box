---
name: split-large-files
description: split large modules into packages without breaking public seams
---

When a source file grows too large (rule of thumb: ~40KB / ~850+ lines), split it — so future edits
and re-reads touch small, atomic files, not a wall of context. Prefer FEW logical parts, each atomic,
over many tiny fragments.

**Why:** editing means re-reading; a large file burns context every time it is touched.

**How to apply — module → package:**
turn `X.<ext>` into an `X/` package. Keep the PUBLIC entry points (dispatchers / the exported surface)
in the package's init file, and move leaf implementations into submodules. Then **re-export every name
that callers or tests reference** from the init, so existing imports and test hooks keep working with
ZERO churn. Verify by running the full test suite — the result must be identical before and after
(same count, same pass/fail).

**Test files:** split by concern freely — no imports depend on test-file layout, so it is zero-risk.
**Cards:** keep one card per source file mirroring the tree — more small cards is fine, less to read later.
