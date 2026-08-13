# reports

Run artifacts written by roles/guides — **audit findings, pass logs, session notes**.
They are NOT cards and must never be written into `__map/` (that folder is cards only,
and mixing a report in there pollutes the map tools).

## Naming — date-first, sortable

```
__HQ/reports/<YYYY-MM-DD>_<kind>.md
```

Examples: `2026-08-13_audit.md`, `2026-08-13_audit-pass2.md`, `2026-08-13_codemap-session.md`.
If a same-day report of the same kind already exists, add a counter: `…_audit-2.md`.

## Who writes here

- **Auditor** (`Guide__AuditCards.md`) → `<date>_audit.md` (issue · file · what's wrong · recommendation).
- **CodeMap orchestrator** (`Role__CodeMap*.md`) → progress / pass logs.

Instruction files (guides, roles) hold ONLY instructions — never progress or reports.
