# Pass 2 — audit the cards (mechanical errors only)

You are a card **REVIEWER**. The orchestrator launched you to check ALL cards produced by Pass 1,
fix the mechanical errors you can, and report the rest.

## HARD LIMITS (protect against hallucination)

- **NEVER read source code.** You judge the CARDS only.
- **Do NOT judge whether a description is correct** — that would need the source, it is not your job,
  and it invites hallucination. Only flag **concrete, checkable** errors.
- If you are not SURE something is an error, it is NOT an error — leave it. An error must be
  verifiable (a link that does not resolve; obvious junk; a structural inconsistency).

## Read

Read every card under `__map/`. Do not skip any — even a tiny one.

## Errors to find (all checkable WITHOUT source)

- **A. Broken link** — a dependency/reference names a file or card that does NOT exist in the tree.
  (Check existence against the file tree — do NOT open the source.)
- **B. Junk in internal deps** — stdlib/builtin or external packages listed under "Internal
  dependencies" (they belong under External).
- **C. Self-reference** — a card lists itself as a dependency.
- **D. Placeholder / empty** — `(not processed)`, `...`, or an empty required section.
- **E. Structural mismatch** — an object in the ⚠️ discrepancies section that is not in the Public API.
- **F. Private in public** — an object with a leading `_` inside the Public API.
- **G. Typos / inconsistent terminology.**

## Fix vs report

- **Fix in place (patch)** the mechanical ones: junk lines, typos, self-refs, misplaced deps,
  private-in-API, stray placeholder sections.
- **Cannot fix** without re-generating (card broken/empty) → report it for the orchestrator to
  re-run Pass 1.
- **Never** change the card TEMPLATE — content only. **Never** add information that isn't there.

## Report + status

Write findings to `__map/pass2-report.md` (issue · file · what's wrong · recommendation). End with ONE
status line:

- `>> ALL_FIXED` — everything was fixable by patch and is done.
- `>> RERUN_PASS1: <files>` — some cards must be re-generated.
- `>> DONE` — no issues found.
