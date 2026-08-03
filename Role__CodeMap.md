# Role: CodeMap — build the code map (strong agent)

Same goal as `Role__CodeMapLocal.md` — produce cards in `_map/cards/` — but for a STRONG agent.

Read `Role__CodeMapLocal.md` for the card format and intent, but:
- **Skip pass 2** (audit) — not needed for a strong agent.
- **Radically simplify pass 1**: do NOT spawn one subagent per file. Take a BATCH of files sized to
  your context window and card them in one go — fewer passes, lighter prompt.

(Fuller method — later.)
