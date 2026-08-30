# `__HQ/tools/` — clone the tools repo here

This folder is intentionally near-empty in THIS (outer) repo. `__HQ/tools/` holds its
own SEPARATE git repository — own history, own remote, own commits — not a submodule,
just a plain nested repo. This outer repo's `.gitignore` ignores everything under
`__HQ/tools/` except this one file, so a fresh checkout of the outer repo always shows
an empty-looking folder with just this note explaining what to do.

## First-time setup

```
rm __HQ/tools/CLONE_TOOLS_HERE.md
git clone https://github.com/seneelya/Project-Context-Box-Tools __HQ/tools
```

`git clone` refuses to clone into a non-empty directory — delete this file first
(that's the whole reason for the `rm` above), or it fails with:

```
fatal: destination path '__HQ/tools' already exists and is not an empty directory.
```

## After that

This file is gone locally once you've cloned — that's expected. It's tracked in the
OUTER repo only so a fresh checkout has something explaining the empty folder; nobody
commits its deletion back (the outer repo's `.gitignore` already keeps everything else
under `__HQ/tools/` out of its history regardless).

Once cloned, `__HQ/tools/TOOLS.md` is the router for what's in there.
