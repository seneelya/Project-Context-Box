# Role: CodeMap — build the code map with a STRONG agent (batched)

You are the **ORCHESTRATOR** (a strong model). You produce cards in `_map/cards/` — a cheap map of the
code, read INSTEAD of the source. Unlike `Role__CodeMapLocal` (one weak subagent per file), you
delegate to **strong subagents (Sonnet)** in **batches sized by context**, so mapping is fast.

The card format, rules, and the path mask are shared — they live in `_map/pass1-make-cards.md`.

## Batch by context size

1. List the source files to map. Skip already-carded/fresh ones — run `python _map/check_freshness.py`.
2. Estimate each file's tokens (**≈ chars ÷ 4**).
3. Pack files into batches whose source totals **~100–120k tokens** each. That leaves the rest of the
   subagent's ~200k window for reading the spec and writing the cards. Prefer grouping files from the
   **same folder** into one batch (related context).

## Delegate: one batch = one Sonnet subagent

```
goal:  Your task is in _map/batch-make-cards.md — read it and execute it for these files:
       <file1>
       <file2>
       ...
```

The subagent reads the shared spec and produces ONE card per file at the mask path.

## Verify

After each batch: check that every expected card exists at `_map/cards/<path>/<name><ext>.md` and is
**non-zero in size** (check the size, do NOT read the file). Missing/empty → re-assign that file
(a smaller batch, or do it yourself).

## No Pass 2

A strong subagent produces reliable cards — **skip the audit pass**. If you doubt a specific card,
open just that card (and, if needed, its source) and fix it directly.

## Where things go

- Cards → `_map/cards/<path>/<name><ext>.md`.
- Instruction files hold ONLY instructions — progress/reports go to separate files.

## Restore (interrupted)

Run `python _map/check_freshness.py` → see which files already have cards; resume batching the rest.
