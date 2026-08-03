# Pass 1 — make ONE card from ONE source file

Language-agnostic. The orchestrator gave you: **this instruction file** and **ONE source file**.
Take exactly that one source file and produce exactly one card — the other files belong to other agents.

A card is a **HINT, not a spec** — a cheap orientation so another agent understands the module WITHOUT
reading the source. **Facts from the code only.** Target compression **4–10×**; full coverage of the
public API matters more than saving lines.

## WHERE THE CARD GOES — exact path mask

The card **mirrors the source's full path** but lives under `_map/cards/`, and keeps the source
filename **including its extension**, plus `.md`:

```
source:   <WORKSPACE>/<path>/<name><ext>
card:     <WORKSPACE>/_map/cards/<path>/<name><ext>.md
```

Examples:
- `_engine/retrieve.py`  →  `_map/cards/_engine/retrieve.py.md`
- `src/main.cpp`         →  `_map/cards/src/main.cpp.md`
- `utils.ts`             →  `_map/cards/utils.ts.md`

Keep the FULL path and the source extension — this exact mask is how other agents locate the card.
Create intermediate folders under `_map/cards/` as needed.

## Card format

```markdown
# <name><ext> — <one factual sentence: what the module does>

## Public API
### Functions
#### `func_name(args) -> return_type`
<1–2 sentences: what it does, params, return. Facts from code only.>

### Classes
#### `ClassName`
<1–2 sentences: purpose.>
- **Attributes:** <significant ones>
- **Methods:** every public method, one per line: `method(args) -> type` — <desc>

## Internal dependencies
| Imports | From file | Objects | Why |
|---|---|---|---|
| `name` | `module<ext>` | `obj1`, `obj2` | <one sentence> |

## How it works
<2–3 sentences, facts only; be concrete — "filters records by date and priority", not "processes data".>

## External dependencies
<Only if the reader may not know it. Skip stdlib and popular packages.>

## ⚠️ Docstring ↔ code discrepancies
<Only real contradictions between a docstring and the code. Omit the section if none.>
```

## RULES

### FACTS FROM THE CODE ONLY
No "key / main / important / core". Do NOT guess architectural role. Do NOT invent dependencies that
are not in the imports.

### CHECK DOCSTRING vs CODE
For EVERY public object: read its docstring/comment AND its implementation. Any contradiction goes to
the **⚠️ Discrepancies** section (omit the section if there are none). Mention commented-out or
disabled code in one line (fact of presence).

### DESCRIBE THE PUBLIC SURFACE, NOTHING ELSE
Every public function, class, attribute, method (list EVERY public method — one per line), and
non-obvious external imports. Do NOT describe private (`_x`) objects or helper internals.

### KEEP IT SHORT
Several× smaller than the source; one sentence per object.

## Optional helper

If a language helper exists in `_map/helpers/`, you MAY run it for a structured hint (public symbols,
imports) and cross-check. Python: `python _map/helpers/py_api.py <file>`. A hint — not a replacement
for reading the code.

## Steps

1. Read the source file you were given.
2. For each public object: read its docstring + implementation; check for discrepancies.
3. Write the card at the exact mask path `_map/cards/<path>/<name><ext>.md`.
4. Report the result.
