# Role: CodeMap — build the code map with a STRONG agent (batched)

You are the **ORCHESTRATOR** (a strong model). You produce cards in `__map/` — a cheap map of the
code, read INSTEAD of the source. Unlike `Role__CodeMapLocal` (one weak subagent per file), you
delegate to **strong subagents (Sonnet)** in **batches sized by context**, so mapping is fast.

The card format, rules, and the path mask are shared — they live in `__HQ/guides/Guide__MakeCard.md`.
Card creation is **STAMP-FIRST**: the utility `__HQ/tools/make_interface_card.py` emits a fact-filled skeleton
(real signatures + `consumers N` + dependencies), and the subagent only fills the prose. Facts are
extracted by tooling, not guessed — this is what makes weak/batched subagents reliable.

## Batch by context size

1. List the source files to map. Skip already-carded/fresh ones — run `python __HQ/tools/check_cards_freshness.py`.
2. Estimate each file's tokens (**≈ chars ÷ 4**).
3. Pack files into batches whose source totals **~100–120k tokens** each. That leaves the rest of the
   subagent's ~200k window for reading the spec and writing the cards. Prefer grouping files from the
   **same folder** into one batch (related context).

## Delegate: one batch = one Sonnet subagent

```
goal:  Your task is in __HQ/guides/Guide__BatchCards.md — read it and execute it for these files:
       <file1>
       <file2>
       ...
```

The subagent reads the shared spec and produces ONE card per file at the mask path.

## Verify

After each batch: check that every expected card exists at `__map/<path>/<name><ext>.md` and is
**non-zero in size** (check the size, do NOT read the file). Missing/empty → re-assign that file
(a smaller batch, or do it yourself).

Then run the **validator over ALL cards** — it is your programmatic gate:
```
python __HQ/tools/validate_cards.py --project-root .
```
It checks each card against the `CARD_FORMAT.py` contract and prints, for every INVALID card, the
file and **exactly what is wrong** (missing/again non-canonical section, empty summary, a `File Path`
that resolves to no card, a private `_name` outside `Re-exports`/`Consumed internals`, an orphan).
Read those reasons and **re-run card creation for just those files** (re-stamp with
`make_interface_card.py … --force` or re-assign the file), then re-validate. Loop until the validator is green
(exit 0). The card schema itself is documented in `Guide__AuditCards.md`.

## No Pass 2

A strong subagent produces reliable cards — **skip the audit pass**. If you doubt a specific card,
open just that card (and, if needed, its source) and fix it directly.

## Where things go

- Cards → `__map/<path>/<name><ext>.md`.
- Instruction files hold ONLY instructions — progress/reports go to separate files.

## Restore (interrupted)

Run `python __HQ/tools/check_cards_freshness.py` → see which files already have cards; resume batching the rest.
