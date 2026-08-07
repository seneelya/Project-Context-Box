---
name: file-size-and-splits
description: large modules split into packages; how to split without breaking seams
---

Owner dislikes big source files — when a `.py` pushes \~40KB / \~850+ lines it should be split, so future edits (and my re-reads) touch small, atomic files.
Prefer FEW logical parts, each atomic, not many tiny fragments.

**Why:** editing means re-reading; a 900-line file wastes context every time

**How to apply — module → package (the pattern used for** **`_engine/backends/`):**
turn `X.py` into `X/` package. Keep the PUBLIC dispatchers in `__init__.py` and
move leaf implementations into submodules, then **re-export every name tests or
callers reference** from `__init__`.  Then imports (`from ._engine import
backends`) and all monkeypatches keep working with ZERO test churn. Verify:
run the full suite, count must be identical .
Also expose `import time` at package top if any test patches `mod.time.sleep`.

Test files: split by concern (per-driver) freely — no imports depend on test
file layout, zero risk. Cards: owner wants them FULLY duplicated (one card per
file mirroring the tree), more cards is fine — less to read later.

