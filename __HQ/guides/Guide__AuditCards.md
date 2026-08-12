# Audit the cards — validator-first, then mechanical review

Two layers of checking, cheapest first:
1. **Programmatic validator** (`validate_cards.py`) — the orchestrator's gate. Deterministic,
   fast, explains exactly what is wrong. Run this FIRST, on ALL cards, and loop until green.
2. **LLM mechanical review** (this reviewer role) — catches source-free issues the validator can't
   (junk text, typos, structural nonsense). Runs AFTER the validator is green.

## The card utilities (all under `__HQ/tools/`)

- **`make_interface_card.py <file> --project-root . [--out P] [--force]`** — the STAMP: emits a fact-filled card
  (signatures + `consumers N` + deps); the author fills prose. Used to (re)create a card.
- **`validate_cards.py --project-root .`** — the validator (below).
- **`check_cards_freshness.py --project-root .`** — which cards are stale vs their source (git/mtime) and orphans.
- **`CARD_FORMAT.py`** — (not a CLI) the format contract every tool reads; its docstring is the card skeleton.

## The card schema (what "valid" is)

```
# <name><ext>                     H1 = ONLY the file name (== the source file name)

<one-line summary>                first non-empty line after H1 (blank line after H1 is fine)

## <H2 section>                   all required H2, in order; empty section body → (none)
### <H3 subsection>               only inside Public API: group by kind
#### `<signature | name>`         one entry per public symbol
consumers N: a.py, b.py           machine FACT (who imports it); consumers 0 = nobody
<one-line description>            the author's prose
```
- Required H2 (module card, in order): **Public API · Dependencies Internal · Dependencies External ·
  How it works · Doc links · Discrepancies**. A **package/index** card (`__init__.py`, `index.ts`,
  `mod.rs`, …) additionally has **Package layout** first.
- Public API H3 by kind: `Functions · Classes · Interfaces · Enums · Types · Constants · Re-exports ·
  Consumed internals` (only those that apply).
- **Dependencies Internal** = `(none)` OR a table `| Import | File Path | Symbols | Why | Kind |`; every
  `File Path` must resolve to an existing card.
- A leading-`_` (private) name is allowed in Public API **only** under `Re-exports` or `Consumed internals`.

## Layer 1 — run the validator on ALL cards (orchestrator)

```
python __HQ/tools/validate_cards.py --project-root .
```
It checks every card against the schema above and, for each INVALID card, prints the file and **exactly
what is wrong**: H1 name ≠ file, empty summary, a missing/non-canonical required section, a deps table
with wrong columns, a `File Path` that resolves to no card, a private `_name` outside the allowed
subsections, or an orphan card (no source). Exit code 1 if anything is wrong, 0 if all clean.

**The loop:** read each reason → **re-run card creation for just those files** (re-stamp with
`python __HQ/tools/make_interface_card.py <file> --project-root . --out <card-path> --force`, then have the author
re-fill the prose per `Guide__MakeCard.md`; or fix a trivial contract slip by hand) → re-validate.
Repeat until the validator exits 0. Only then start Layer 2.

---

## Layer 2 — LLM mechanical review (this reviewer)

You are a card **REVIEWER**, launched after the validator is green to catch what it cannot.

### HARD LIMITS (protect against hallucination)
- **NEVER read source code.** You judge the CARDS only.
- **Do NOT judge whether a description is correct** — that needs the source, it is not your job, and it
  invites hallucination. Only flag **concrete, checkable** errors.
- If you are not SURE something is an error, it is NOT an error — leave it.

### Read
Read every card under `__map/`. Do not skip any — even a tiny one.

### Errors to find (all checkable WITHOUT source)
- **A. Broken link** — a dependency `File Path` names a file/card not in the tree (check existence, don't open source).
- **B. Junk in internal deps** — stdlib/external packages under Dependencies Internal (they belong under External).
- **C. Self-reference** — a card lists itself as a dependency.
- **D. Placeholder / empty** — `<Agent: …>` left unfilled, `(not processed)`, `...`, or an empty required section.
- **E. Structural mismatch** — an object in `## Discrepancies` that is not in the Public API.
- **F. Private in public** — a leading-`_` object in Public API outside `Re-exports`/`Consumed internals`.
- **G. Typos / inconsistent terminology.**

### Fix vs report
- **Fix in place** the mechanical ones (junk lines, typos, self-refs, misplaced deps, private-in-API,
  leftover `<Agent: …>` directives, stray placeholders).
- **Cannot fix** without re-generating (card broken/empty) → report it for the orchestrator to re-run creation.
- **Never** change the card TEMPLATE, and **never** add information that isn't there.

### Report + status
Write findings to `__map/pass2-report.md` (issue · file · what's wrong · recommendation). End with ONE status line:
- `>> ALL_FIXED` — everything was fixable by patch and is done.
- `>> RERUN_PASS1: <files>` — some cards must be re-generated (re-stamp + re-fill).
- `>> DONE` — no issues found.
