# Guide: MakeCard — write a code card (STAMP-FIRST)

You are given **ONE source file**. Produce its **card**.

## What a card is

A card is a **HINT, not a spec** — a cheap orientation so another agent understands the module
**WITHOUT reading the source**. **FACTS FROM THE CODE ONLY.** Target compression **4–10×**; full
coverage of the public API matters more than saving lines. The exact format contract is
**`__HQ/tools/CARD_FORMAT.py`** (its docstring is the card skeleton) — this guide is how to write to it.

Two parts:
- **Part 1 (primary):** the stamp utility `make_interface_card.py` fills the FACTS; you fill only the prose.
- **Part 2 (fallback):** used ONLY if the utility does not work — and you MUST tell your caller first.

## WHERE THE CARD GOES — exact path mask

Mirror the source's full path under `__map/`, keep the source filename **including its extension**,
add `.md`:
```
source:   <path>/<name><ext>
card:     __map/<path>/<name><ext>.md
```
Examples: `_engine/retrieve.py` → `__map/_engine/retrieve.py.md` · `src/main.cpp` → `__map/src/main.cpp.md`.

---

## Part 1 — STAMP-FIRST  (use this)

### Step 1 — generate the card file
Run from the project root:
```
python __HQ/tools/make_interface_card.py <path>/<name><ext> --project-root . --out __map/<path>/<name><ext>.md
```
`--out` writes the card file directly (creating folders). Without `--out` it PRINTS to stdout —
then YOU redirect it (`… > __map/<path>/<name><ext>.md`). Prefer `--out`.

The card comes with the **FACT** sections already filled:
- `## Public API` — real signatures grouped by kind (`### Functions/Classes/…`); under each entry a
  fact line `consumers N: file1, file2` (who really imports it; `consumers 0` = nobody).
- `## Dependencies Internal/External`; `## Package layout` (for a package/index file).
- Prose slots are **directives** `<Agent: …>` — that is YOUR job (Step 3).

### Step 1b — if the card ALREADY exists
`make_interface_card --out` refuses to overwrite (exit 2, `card already exists`). Decide:
- an **unfilled stamp** (still full of `<Agent: …>` lines) → re-run with **`--force`**;
- a card with **real prose** → do NOT `--force` (you would delete descriptions). Instead run WITHOUT
  `--out` (to stdout) and update only the changed FACT sections into the existing card by hand, keeping
  the prose. (`python __HQ/tools/check_freshness.py` shows which cards are stale.)

### Step 2 — if stderr shows the tree-sitter WARNING → REPORT UP
`WARNING: … REGEX FALLBACK … pip install tree-sitter …` means the high-fidelity parser is not
installed; the card is **still usable** (lower-fidelity signatures) — NOT a failure, do not stop.
But do **NOT** decide alone and do **NOT** self-install. **Report it to your caller (boss):** the
parser is missing, the card is on the regex fallback, and pass the exact command upward —
`pip install tree-sitter tree-sitter-<lang>`. The boss escalates to the user (install or not).
Meanwhile continue on the fallback unless told otherwise.

### Step 3 — fill the prose (read the source ONCE), following the RULES below
- summary line under the H1 → one line: what the module does;
- each `#### <symbol>` → one concise sentence (what it does + its role), OR **delete the directive
  line** if trivial;
- `## Dependencies Internal` "why" cells; `## How it works`; `## Discrepancies`; `## Package layout`.
- **KEEP the fact lines** (`consumers N: …`) — verified; never invent or alter them.

### Step 4 — validate
```
python __HQ/tools/validate_cards.py --project-root .
```
Fix what it flags for your card (missing section, empty summary, unresolved `File Path`). Green = done.

---

## Package cards (`__init__.py` and language index files: `mod.rs`, `index.ts`, …)

A package/index file is a **node, not a leaf** — usually no functions/classes of its own. Its card adds
one section and reshapes Public API (other sections as for a module card):
- **`## Package layout`** — the submodules, each a **link to its card** + a one-line role.
- Public API there = the dispatchers the file defines + `### Re-exports`.

(`make_interface_card` already emits `## Package layout` and `### Re-exports` for these files.)

---

## RULES  (apply when filling prose — Part 1 Step 3 — and in the Part 2 fallback)

- **FACTS FROM THE CODE ONLY.** No "key / main / important / core". Do NOT guess architectural role.
  Do NOT invent dependencies that are not in the imports.
- **SKIP** helpers used only inside this file. (Re-exports/aliases → `### Re-exports`; a `_`-private
  name is allowed there and in `### Consumed internals` when other files import it.)
- **CHECK DOCSTRING vs CODE** for every public object; real contradictions → `## Discrepancies`.
  Mention commented-out / disabled code in one line.
- **KEEP IT SHORT** — several× smaller than the source; one sentence per object.
- **DESCRIBE THE PUBLIC SURFACE, NOTHING ELSE** — every public function, class, attribute, method
  (list EVERY public method — one per line) and non-obvious external imports.

---

## Part 2 — FALLBACK  (the utility is NOT working)

Enter this ONLY if Step 1 fails: `make_interface_card.py` errors, will not run, or prints nothing.

### Step 0 — REPORT TO YOUR CALLER FIRST (do not switch silently)
> "`make_interface_card.py` is not working (`<paste the exact error>`). Switching to MANUAL card authoring
> (fallback). Facts (consumers/signatures) will be hand-derived and may be less complete."

### Manual recipe
Author the card by hand to the **`__HQ/tools/CARD_FORMAT.py`** contract (its docstring = the skeleton)
and the **RULES** above: H1 = the file name only; next non-empty line = one-line summary; then all H2
sections in order (empty → `(none)`). Build the deps table `| Import | File Path | Symbols | Why | Kind |`
with root-relative `File Path`s. Prefer the **consumed surface** (what other files actually import) over
a bare "public" list; if unsure who uses a symbol, mark it "possible export" rather than guessing.
Then run `validate_cards.py` (it is independent of `make_interface_card.py`); if the whole toolchain is down, tell the caller.
