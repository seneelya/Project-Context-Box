# Pass 1 — make a card for ONE source file

You are a documentation subagent. The orchestrator gave you: **this instruction file**, **ONE source
file** to process, and a **checklist** to mark. Do only your one file — the rest belong to other agents.

**Goal:** create/update a card `<file>.md` next to the source file, so ANOTHER agent understands the
module cheaply WITHOUT reading the source. A card is a **HINT, not a spec** — facts from code only.
Target compression **4–10×**; completeness of the public API matters more than saving lines.

## Card format

```markdown
# <file> — <one factual sentence: what the module does>

## Public API
### Functions
#### `func_name(args) -> return_type`
<1–2 sentences: what it does, params, return. Facts from code only.>

### Classes
#### `ClassName`
<1–2 sentences: purpose.>
- **Attributes:** <significant ones>
- **Methods:** list EVERY public method (no leading `_`), one per line: `method(args) -> type` — <desc>

## Internal dependencies
| Imports | From file | Objects | Why |
|---|---|---|---|
| `name` | `module.ext` | `obj1`, `obj2` | <one sentence> |

## How it works
<2–3 sentences, facts from code only; be concrete ("filters records by date", not "processes data").>

## External dependencies
<Only if the reader may not know it. Skip stdlib and popular packages.>

## ⚠️ Docstring ↔ code discrepancies
<Only real contradictions between a docstring and the actual code. Omit the section if none.>
```

## Critical rules

1. **Facts from code ONLY.** No "key / main / important / core". Do NOT guess architectural role.
   Do NOT invent dependencies that are not in the imports.
2. **Check docstring vs code** for each public object → contradictions go to the ⚠️ section (omit if
   none). Mention commented-out / disabled functions in one line (fact of presence).
3. **Describe:** all public functions/classes/attributes/methods; external imports if non-obvious.
   **Do NOT describe:** private (`_x`), helper internals.
4. **Brevity:** several× smaller than the source; one sentence per object.

## Optional helper

If a language helper exists in `_map/helpers/`, you MAY run it for a structured hint (public symbols,
imports) and cross-check. Python: `python _map/helpers/py_api.py <file>`. A hint, not a replacement
for reading the code.

## Steps

1. Read the source file you were given.
2. For each public object: read its docstring + its implementation; check for discrepancies.
3. Write the card `<file>.md` next to the source.
4. Mark your file `[x]` in the checklist.
5. Report the result.
