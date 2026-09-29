#!/usr/bin/env python3
"""Deploy the ProjectStarter template (the __HQ brain, entry files included) into a consumer project.

The ONLY blessed way to push template updates into a project — replaces hand-diffing.

    py __dev/deploy_hq.py --target <project>            # DRY-RUN: show what would change
    py __dev/deploy_hq.py --target <project> --apply     # actually write template files
    py __dev/deploy_hq.py --target <project> --apply --init   # + create missing scaffolds
    py __dev/deploy_hq.py --target <project> --apply --force '__HQ/tools/**'  # override a CONFLICT

WHAT IS DEPLOYED (template-owned; everything else in the project is left untouched):
  - entry + rules, all INSIDE the HQ (Vision08 — nothing of ours outside __HQ/):
    __HQ/START.md, __HQ/CONTEXT_RESTORE.md, __HQ/RITUAL__session_end.md, __HQ/RULE_sessionRestore.md
  - __HQ/WORKFLOW.md, __HQ/Role__*.md, __HQ/guides/**
  - __HQ/tools/**   (minus .git / __delme / __dev / __pycache__ / test / _logs / .pytest_cache /
                     *.pyc / *.tmp / *.bak)
  Old root entry files (START.md, CONTEXT_RESTORE.md, AGENTS.md) are reported as ORPHAN — delete
  them by hand; the tool never deletes.

Project-owned files are defined by OMISSION — DECISIONS.md, TRACKER.md, HowTo__*.md,
plans/**, vision/**, docs/** never match the template set, so they are never touched.

HOW DRIFT IS DETECTED (answers "did the project change this file?"):
  The set of "known template versions" of a file = ALL its historical git blob-ids in the
  owning repo (__HQ/tools/** -> the nested tools repo; everything else -> the ProjectStarter
  repo). For each file we compare the project's current blob-id (ph) against that set:
    - no project file            -> NEW      (copy)
    - ph == current template     -> UPTODATE (skip)
    - ph is a KNOWN older version-> UPDATE   (project never edited it, just stale -> overwrite)
    - ph matches NOTHING known   -> CONFLICT (project edited it -> manual merge, or --force)

No state file is stored in the project: git history IS the baseline. The consumer's own git
is the undo — after --apply, review `git status`/`git diff` there and commit or revert.

CONFIG__TOOLS.py is project-owned and NEVER auto-merged (see above) — its own
CONFIG_SCHEMA_VERSION is compared instead: project's < template's prints a STALE-CONFIG
line (which settings changed lives in the template's own file, diff it by hand) and flips
the exit code, same as an unresolved CONFLICT.
"""

import argparse
import fnmatch
import os
import re
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

# --- template membership -----------------------------------------------------

_TOOLS_PREFIX = "__HQ/tools/"
_TOOLS_EXCLUDE_PARTS = {".git", "__delme", "__dev", "__pycache__", "test", "_logs", ".pytest_cache"}
_HQ_ENTRY = {"__HQ/START.md", "__HQ/CONTEXT_RESTORE.md", "__HQ/RITUAL__session_end.md",
             "__HQ/RULE_sessionRestore.md", "__HQ/WORKFLOW.md"}
# Entry files that used to live in the project ROOT (before Vision08 moved them into __HQ/):
# their old-path history counts as "known versions" of the new path (a stale unedited copy is an
# UPDATE, not a CONFLICT), and a leftover root copy is reported as ORPHAN.
_MOVED_FROM = {"__HQ/START.md": "START.md", "__HQ/CONTEXT_RESTORE.md": "CONTEXT_RESTORE.md"}
_ROOT_ORPHANS = ["START.md", "CONTEXT_RESTORE.md", "AGENTS.md"]

# create-if-absent scaffolds for --init (never overwrite; establish empty structure)
_INIT_FILES = ["__HQ/DECISIONS.md", "__HQ/TRACKER.md", "__HQ/plans/INDEX.md",
               "__HQ/__map/.gitkeep",   # cards: CONFIG__TOOLS.MAP_DIR = "__map", relative to the HQ
               "__HQ/docs/.gitkeep", "__HQ/vision/.gitkeep",
               # Recon role's homes. Project-owned like every scaffold here: the
               # ROLE file is template-owned and keeps getting updates, its
               # FINDINGS never are — a deploy must not touch evidence.
               "__HQ/OPEN-QUESTIONS.md", "__HQ/recon/INDEX.md",
               "__HQ/recon/DECISIONS-RECON.md",
               "__HQ/tools/CONFIG__TOOLS.py"]  # per-project config: seed once, then project-owned
_INIT_DIRS = ["__HQ/plans/deferred", "__HQ/plans/done", "__HQ/plans/superseded",
              "__HQ/recon/subjects", "__HQ/recon/draft-research/subjects",
              "__HQ/recon/superseded"]


def is_template(rel):
    """rel = posix path relative to the source (ProjectStarter) root."""
    if rel in _HQ_ENTRY:
        return True
    parts = rel.split("/")
    if len(parts) == 2 and parts[0] == "__HQ" and fnmatch.fnmatch(parts[1], "Role__*.md"):
        return True
    if rel.startswith("__HQ/guides/") and rel.endswith(".md"):
        return True
    if rel == "__HQ/tools/CONFIG__TOOLS.py":
        return False  # per-project config (PROJECT_ROOT/LANGUAGE/DECL_BACKEND) — project-owned
    if rel == "__HQ/tools/CLONE_TOOLS_HERE.md":
        return False  # outer-repo-only setup note (explains the nested-repo clone step),
                       # not part of the tools repo's own content
    if rel.startswith(_TOOLS_PREFIX):
        if any(p in _TOOLS_EXCLUDE_PARTS for p in parts) or rel.endswith((".pyc", ".tmp", ".bak")):
            return False
        return True
    return False


def template_files(source):
    out = []
    for root, dirs, files in os.walk(source):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", ".pytest_cache", "_logs")]
        for name in files:
            rel = os.path.relpath(os.path.join(root, name), source).replace(os.sep, "/")
            if is_template(rel):
                out.append(rel)
    return sorted(out)


# --- git plumbing ------------------------------------------------------------

def _git(repo, *args):
    r = subprocess.run(["git", "-C", repo, *args],
                       capture_output=True, text=True, encoding="utf-8")
    return r.stdout


def blob_id(path):
    """git blob-id (sha1 over content) of a file, repo-independent; None if absent."""
    if not os.path.isfile(path):
        return None
    r = subprocess.run(["git", "hash-object", path],
                       capture_output=True, text=True, encoding="utf-8")
    return r.stdout.strip() or None


def repo_for(source, rel):
    """(repo_dir, path_inside_repo) — tools/** live in the nested tools repo."""
    if rel.startswith(_TOOLS_PREFIX):
        return os.path.join(source, "__HQ", "tools"), rel[len(_TOOLS_PREFIX):]
    return source, rel


def known_ids(source, rel, current):
    """All historical blob-ids of rel in its owning repo (plus its pre-move path, see
    _MOVED_FROM), plus the current one."""
    ids = {current} if current else set()
    for path in (rel, _MOVED_FROM.get(rel)):
        if path:
            ids |= _history_ids(source, path)
    return ids


def _history_ids(source, rel):
    repo, inpath = repo_for(source, rel)
    commits = [c for c in _git(repo, "log", "--all", "--pretty=%H", "--", inpath).split() if c]
    ids = set()
    if commits:
        spec = "".join(f"{c}:{inpath}\n" for c in commits)
        r = subprocess.run(["git", "-C", repo, "cat-file", "--batch-check"],
                           input=spec, capture_output=True, text=True, encoding="utf-8")
        for line in r.stdout.splitlines():
            f = line.split()
            if len(f) >= 2 and f[1] == "blob":
                ids.add(f[0])
    return ids


# --- classification ----------------------------------------------------------

def classify(source, target, rel):
    th = blob_id(os.path.join(source, rel))
    ph = blob_id(os.path.join(target, rel))
    if ph is None:
        return "NEW", th, ph
    if ph == th:
        return "UPTODATE", th, ph
    if ph in known_ids(source, rel, th):
        return "UPDATE", th, ph
    return "CONFLICT", th, ph


_CONFIG_TOOLS_REL = "__HQ/tools/CONFIG__TOOLS.py"
_SCHEMA_VER_RE = re.compile(r"^CONFIG_SCHEMA_VERSION\s*=\s*(\d+)", re.MULTILINE)


def config_schema_version(path):
    """CONFIG_SCHEMA_VERSION from a CONFIG__TOOLS.py, read by REGEX (never imported — it's a
    project file, importing it would run arbitrary project-owned code). None if the file is
    absent or predates this constant."""
    if not os.path.isfile(path):
        return None
    text = open(path, encoding="utf-8").read()
    m = _SCHEMA_VER_RE.search(text)
    return int(m.group(1)) if m else None


def config_drift(source, target):
    """CONFIG__TOOLS.py is project-owned (never overwritten, see is_template()) — this is the
    ONLY signal a project gets that its copy is missing settings the template has since grown.
    Returns None if the project's copy is current or the file doesn't exist yet (--init's job),
    else (project_version_or_None, template_version) to report as STALE-CONFIG."""
    tmpl_ver = config_schema_version(os.path.join(source, _CONFIG_TOOLS_REL))
    proj_path = os.path.join(target, _CONFIG_TOOLS_REL)
    if not os.path.isfile(proj_path) or tmpl_ver is None:
        return None
    proj_ver = config_schema_version(proj_path)
    if proj_ver is not None and proj_ver >= tmpl_ver:
        return None
    return proj_ver, tmpl_ver


# --- main --------------------------------------------------------------------

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    default_source = os.path.dirname(here)  # __dev/.. == ProjectStarter root

    ap = argparse.ArgumentParser(description="Deploy ProjectStarter template into a project.")
    ap.add_argument("--target", required=True, help="consumer project root")
    ap.add_argument("--source", default=default_source, help="ProjectStarter root (default: auto)")
    ap.add_argument("--apply", action="store_true", help="write files (default: dry-run)")
    ap.add_argument("--init", action="store_true", help="also create missing scaffolds")
    ap.add_argument("--force", action="append", default=[], metavar="GLOB",
                    help="overwrite CONFLICT files matching GLOB (repeatable)")
    args = ap.parse_args()

    source = os.path.abspath(args.source)
    target = os.path.abspath(args.target)
    if not os.path.isdir(os.path.join(source, "__HQ")):
        sys.exit(f"not a ProjectStarter source (no __HQ): {source}")
    if not os.path.isdir(target):
        sys.exit(f"target not found: {target}")

    def forced(rel):
        return any(fnmatch.fnmatch(rel, g) for g in args.force)

    buckets = {k: [] for k in ("NEW", "UPDATE", "UPTODATE", "CONFLICT")}
    for rel in template_files(source):
        action, _th, _ph = classify(source, target, rel)
        buckets[action].append(rel)

    def copy(rel):
        src, dst = os.path.join(source, rel), os.path.join(target, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

    def seed_config_tools(rel):
        """Сеет CONFIG__TOOLS.py с PROJECT_ROOT, вписанным как реальный АБСОЛЮТНЫЙ путь ЭТОГО
        деплоя — не статичный список путей-кандидатов «повезёт/не повезёт» (REQ-002-C: список
        кандидатов может молча подобрать ЧУЖОЙ существующий каталог на диске). Делает card-тулов
        неявный дефолт (`--project-root` не задан -> `CONFIG__TOOLS.PROJECT_ROOT`, см.
        __HQ/tools/__dev/vision/Vision01__path-and-flag-conventions.md) безопасным."""
        src, dst = os.path.join(source, rel), os.path.join(target, rel)
        text = open(src, encoding="utf-8").read()
        pattern = re.compile(r'PROJECT_ROOT = _resolve_root\(\[.*?\]\) or "\."', re.DOTALL)
        target_abs = os.path.abspath(target)
        replacement = (f"PROJECT_ROOT = {target_abs!r}  "
                       f"# written by deploy_hq.py --init for THIS project — don't copy elsewhere")
        # lambda, not a string: re.sub parses backslashes in a string replacement, which turned
        # repr's 'y:\\SRC' back into 'y:\SRC' (an invalid-escape warning, or a silently broken
        # path for \t \n \b ...). A function's return value is inserted verbatim.
        new_text, n = pattern.subn(lambda _m: replacement, text, count=1)
        if n == 0:
            raise RuntimeError(
                "deploy_hq.py: CONFIG__TOOLS.py template's PROJECT_ROOT block wasn't found in the "
                "expected shape — update seed_config_tools()'s pattern before using --init.")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "w", encoding="utf-8") as f:
            f.write(new_text)

    written = 0
    print(f"deploy  source={source}\n        target={target}\n")

    for rel in buckets["NEW"]:
        print(f"  NEW       {rel}")
        if args.apply:
            copy(rel); written += 1
    for rel in buckets["UPDATE"]:
        print(f"  UPDATE    {rel}")
        if args.apply:
            copy(rel); written += 1
    for rel in buckets["CONFLICT"]:
        if forced(rel):
            print(f"  FORCED    {rel}   (was CONFLICT)")
            if args.apply:
                copy(rel); written += 1
        else:
            print(f"  CONFLICT  {rel}   <- project-modified; merge by hand or --force")
            print(f"            diff: git diff --no-index \"{os.path.join(target, rel)}\" \"{os.path.join(source, rel)}\"")
    if buckets["UPTODATE"]:
        print(f"  UPTODATE  {len(buckets['UPTODATE'])} file(s) already current")
    for rel in _ROOT_ORPHANS:
        # only OUR old copy — a foreign project may have its own AGENTS.md/START.md (llama.cpp does)
        ph = blob_id(os.path.join(target, rel))
        if ph and ph in _history_ids(source, rel):
            print(f"  ORPHAN    {rel}   <- old root entry file of the template; everything lives in "
                  f"__HQ/ now — delete by hand after review (never auto-deleted)")

    drift = config_drift(source, target)
    if drift:
        proj_ver, tmpl_ver = drift
        proj_str = f"v{proj_ver}" if proj_ver is not None else "no version (predates this check)"
        print(f"  STALE-CONFIG  {_CONFIG_TOOLS_REL}   project {proj_str} < template v{tmpl_ver}"
              f" — never auto-merged, compare and copy in the new settings by hand")

    # --init: create-if-absent scaffolds (never overwrite)
    if args.init:
        print("\n  -- init scaffolds (create-if-absent) --")
        for rel in _INIT_DIRS:
            dst = os.path.join(target, rel)
            if not os.path.exists(dst):
                print(f"  MKDIR     {rel}/")
                if args.apply:
                    os.makedirs(dst, exist_ok=True)
        for rel in _INIT_FILES:
            src, dst = os.path.join(source, rel), os.path.join(target, rel)
            if os.path.isfile(src) and not os.path.exists(dst):
                print(f"  SCAFFOLD  {rel}" + ("  (PROJECT_ROOT <- this deploy's path)"
                                               if rel == "__HQ/tools/CONFIG__TOOLS.py" else ""))
                if args.apply:
                    if rel == "__HQ/tools/CONFIG__TOOLS.py":
                        seed_config_tools(rel)
                    else:
                        copy(rel)
                    written += 1

    n_conflict = len([r for r in buckets["CONFLICT"] if not forced(r)])
    print(f"\n  summary: NEW {len(buckets['NEW'])}  UPDATE {len(buckets['UPDATE'])}  "
          f"UPTODATE {len(buckets['UPTODATE'])}  CONFLICT {n_conflict}"
          + ("  STALE-CONFIG 1" if drift else ""))
    if args.apply:
        print(f"  wrote {written} file(s). Review in the target's git: git -C \"{target}\" status")
    else:
        print("  DRY-RUN — nothing written. Add --apply to write.")
    sys.exit(1 if (n_conflict or drift) else 0)


if __name__ == "__main__":
    main()
