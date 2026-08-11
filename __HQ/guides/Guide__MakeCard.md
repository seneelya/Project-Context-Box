# Guide — make ONE card from ONE source file

Language-agnostic. You were given: **this file** and **ONE source file**. Produce exactly one card.

A card is a **HINT, not a spec** — a cheap orientation so another agent understands the module WITHOUT
reading the source. **Facts from the code only.** Target compression **4–10×**; full coverage of the
public API matters more than saving lines. 

## The exact token contract lives in:  `__HQ/tools/card_format.py` read this file.
(the machine reads that); this guide is how to write card.

## WHERE THE CARD GOES — exact path mask

Mirror the source's full path under `__map/`, keep the source filename **including its extension**, add `.md`:

```
source:   <WORKSPACE>/<path>/<name><ext>
card:     <WORKSPACE>/__map/<path>/<name><ext>.md
```
Examples: `_engine/retrieve.py` → `__map/_engine/retrieve.py.md` · `src/main.cpp` → `__map/src/main.cpp.md`.

## Card format (ALL sections present, in this order; if section id empty → then write its header and in its body write exactly `(none)`)

```markdown
# <name><ext>
<one-line summary: WHAT the module does — never empty>

## Public API
### Functions
#### `func_name(args) -> return_type`
<1–2 sentences: what it does, params, return. Facts from code only.>
### Classes
#### `ClassName`
<1–2 sentences: purpose.>
- **Attributes:** <significant ones>
- **Methods:** every public method, one per line: `method(args) -> type` — <desc>

## Dependencies Internal
| Import | File Path | Symbols | Why | Kind |
|---|---|---|---|---|
| `config` | `path/config.<ext>` | `DEFAULTS`, `load()` | reads config | normal |

## Dependencies External
<third-party/stdlib the reader may not know; else `(none)`>

## How it works
<2–3 sentences on the MECHANISM (the "how"); be concrete — "filters records by date and priority",
not "processes data". The one-line summary above already carries the "what".>

## Doc links
<links to project docs / ticket or task numbers referenced in docstrings; else `(none)`>

## Discrepancies
<real contradictions between a docstring/comment and the code; else `(none)`>
```

## Line 1 / line 2 (STRICT — parsed automatically)

- **Line 1** is the H1 and is **ONLY the file name**  that was given to you  `# <name><ext>`  Example: `# db.py` — it must equal the card's file name.
  No `— summary` on this line.
- **Line 2** is the **one-line summary** (what the module does). It is extracted automatically —
  **never leave it empty.**   Line could be long. It should clearly answer on question: what the file/module does. 

## Public API — group exports by kind (H3)

Put each public export under an H3 by its kind. Common kinds: **Functions · Classes · Constants ·
Types · Objects**. This list is **open** — add kinds that fit the language (Enums, Interfaces, Macros,
Traits, …). Include only the kinds that actually occur.

- **`### Re-exports`** — names this module exposes but that live in another file (incl. back-compat
  aliases like `_setup = register_cli`). Here a leading-`_` name is fine: it is a *deliberate*
  interface, not a private helper. Format: `exposed_name -> origin`.
- If the module has no public surface at all → the whole section body is `(none)`.

Cards may **link to sibling cards** as `[name](relative/name.ext.md)` — cheap navigation for the reader.

## Dependencies Internal — the table

- **File Path** = the dependency's **root-relative path WITH extension** (`_core/registry.py`), the
  same address as its card. **NOT** the language import path (`._core`, `agent.memory_provider`) —
  that goes in the **Import** column. This is what lets tools link cards into a graph.
- **Import** = how it is referenced in code (module/name). **Symbols** = objects used. **Why** = one
  line. **Kind** = `normal` / `lazy` / `conditional` / `type` (default `normal`).
- No internal deps → section body is `(none)` (no table).

## Package cards (`__init__.py` and language index files: `mod.rs`, `index.ts`, …)

A package/index file is a **node, not a leaf** — usually no functions/classes of its own. Its card adds
one section and reshapes Public API (all other sections are as for a module card):

- **`## Package layout`** — the submodules, each a **link to its card** + a one-line role:
  ```
  - [`_http.py`](_http.py.md) — transport floor: timeouts, retries, headers.
  - [`resolve.py`](resolve.py.md) — offline config → backend chain.
  ```
- **`## Public API`** here = **re-exports grouped by origin** (what the package exposes from its
  submodules) + any dispatchers/functions defined in the index file itself:
  ```
  ### Re-exports
  from `_http`: `BackendError`, `_post_with_retries`
  from `resolve`: `resolve_chain`, `is_local_backend`
  ### Functions
  #### `chat(cfg, role, ...) -> str | None`
  Dispatcher defined here; walks the role's chain, first success wins.
  ```

## **RULES**

### **FACTS FROM THE CODE ONLY** 
No "key / main / important / core". Do NOT guess architectural role. Do NOT invent dependencies that are not in the imports.
### **Skip** 
skip helpers used only inside this file. (Re-exports/aliases → `### Re-exports`, `_`-names ok there.)
### **CHECK DOCSTRING vs CODE** 
for every public object; real contradictions → `## Discrepancies`.
  Mention commented-out / disabled code in one line.
### **KEEP IT SHORT**
several `×` smaller than the source; one sentence per object.
### **DESCRIBE THE PUBLIC SURFACE, NOTHING ELSE**
Every public function, class, attribute, method (list EVERY public method — one per line), and
non-obvious external imports.
### Try to Add "Consumed surface", not just real "public"
Try to identify the "consumed surface," not just public exports. Check for non-obvious exports. Describe any symbol imported by other files from this package (even _-prefixed ones) if it acts as the effective interface. Avoid reading full files. If unsure, mark them as "Possible exports."

## Language notes

Kinds and extensions vary by language (a `.h`/`.hpp` card describes declarations; `Types`/`Interfaces`
matter in typed languages; `Kind=lazy` where the language defers imports). Use judgement — the H3 kind
list is a suggestion, not a fixed enum.

## Optional helper

Python: `python __HQ/tools/py_api.py <file>` for a structured hint (public symbols, imports) — a hint,
not a replacement for reading the code.

## Steps

1. Read the source file. If a card already exists at the mask path → **read it and correct it** to the
   code and this contract (the card is the object being processed; the correct shape is here).
2. For each public object: read its docstring + implementation; note discrepancies.
3. Write the card at `__map/<path>/<name><ext>.md`, following the format above (all sections present).
4. **Self-check:** `python __HQ/tools/validate_cards.py --cards-dir __map` — fix everything it flags for
   your card (missing section, deps columns, a `File Path` that doesn't resolve, private in Public API).
5. Report the result.
