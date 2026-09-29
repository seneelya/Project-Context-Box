HOW TO DEPLOY the ProjectStarter template into a consumer project
(local note — gitignored, not shipped with the template)
==================================================================

TOOL:  __dev/deploy_hq.py      (run from the ProjectStarter root)

    py __dev/deploy_hq.py --target <PROJECT>              # DRY-RUN (default): show what would change
    py __dev/deploy_hq.py --target <PROJECT> --apply       # actually write the template files
    py __dev/deploy_hq.py --target <PROJECT> --apply --init  # + create missing scaffolds (new project)
    py __dev/deploy_hq.py --target <PROJECT> --apply --force '__HQ/tools/**'   # override a CONFLICT

Example:
    py __dev/deploy_hq.py --target T:\AgentsWork\memohood

WHAT GETS DEPLOYED (template-owned — overwritten):
    everything lives INSIDE __HQ/ (Vision08) — nothing is written to the project root:
    __HQ/START.md, __HQ/CONTEXT_RESTORE.md, __HQ/RITUAL__session_end.md, __HQ/RULE_sessionRestore.md
    __HQ/WORKFLOW.md, __HQ/Role__*.md (incl. Role__Recon), __HQ/guides/**
    __HQ/TRACKER/0000__rule.md   (the rule only — the folder's entry files are not template)
    __HQ/tools/**  (minus .git / __delme / __pycache__ / test / _logs / .pytest_cache / *.tmp / *.pyc / *.bak)
    --init also creates __HQ/TRACKER/archive/
    old root START.md / CONTEXT_RESTORE.md / AGENTS.md, and a leftover __HQ/TRACKER.md
        -> reported as ORPHAN, delete by hand. There is no TRACKER.md in the template.

WHAT IS NEVER TOUCHED (project-owned — by omission):
    DECISIONS.md, HowTo__*.md, plans/**, vision/**, docs/**
    __HQ/TRACKER/NNNN__slug.md (every entry except 0000__rule.md), __HQ/TRACKER/archive/**
    OPEN-QUESTIONS.md, recon/**  (the Recon role FINDINGS — evidence, never overwritten)
    __HQ/__map/**  (cards; scaffolded empty on --init)
    __HQ/tools/CONFIG__TOOLS.py   (per-project config; seeded once on --init)

STALE-CONFIG (CONFIG__TOOLS.py never auto-merges, so it needs its own signal):
    the template's CONFIG_SCHEMA_VERSION is compared against the project's copy;
    project's lower (or missing entirely) -> "STALE-CONFIG" line in the report and a
    non-zero exit code, same as an unresolved CONFLICT. Fix: diff the template's
    CONFIG__TOOLS.py against the project's and copy in whatever's new, by hand.

DRIFT DETECTION (per file, no state file in the project — git history IS the baseline):
    known versions of a file = ALL its historical git blob-ids in the OWNING repo
    (__HQ/tools/** -> the nested tools repo; everything else -> the ProjectStarter repo)
      no project file            -> NEW      (copied)
      project == current template -> UPTODATE (skipped)
      project == a KNOWN old ver   -> UPDATE   (stale but unedited -> overwritten)
      project matches NOTHING      -> CONFLICT (project edited it -> manual merge, or --force)

    exit code: 0 if no conflicts, 1 if any CONFLICT.

UNDO:
    The consumer project's own git is the undo. After --apply, review there:
        git -C <PROJECT> status
        git -C <PROJECT> diff
    then commit or revert.
    CAUTION: if the project has OTHER uncommitted work, do NOT blanket
    `git checkout .` / `reset --hard` — it wipes that work too. Revert only the
    files the deploy touched (the tool's report lists them).

ORPHANS:
    The tool never deletes. Files that exist in the project but no longer in the
    template (renamed/removed upstream) are left in place — delete them BY HAND
    after reviewing. No auto-prune on purpose (silent deletion is dangerous).
