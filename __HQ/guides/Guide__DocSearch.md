# Guide: search the docs by meaning (byeori)

Use it when you look for **where something was discussed** in `.md` (plans, tracker, vision, cards,
reports) and don't know the exact words. It answers with file paths. Exact names in code → grep; code
structure → `get_codeblock`; a module's real interface → `find_code_usage`.

## Step 0 — installed? If not, install

```bash
python -m byeori --help
```

Fails with `No module named byeori` → install (pinned commit, do not change it on your own):

```bash
python -m pip install --user "byeori @ git+https://github.com/peterkimpmp/byeori@c6decd5" ripgrep
```

- `ripgrep` gives `rg`, the exact-word half of the hybrid search; without it search is meaning-only.
- The first `index` downloads the embedding model `minishlab/potion-multilingual-128M` from Hugging
  Face. It takes a while once; it is not a hang.
- Use `python -m byeori` everywhere: the `byeori` command may be missing from PATH.

## Step 1 — keep the index out of git

The index is written into the searched folder as `<folder>/.byeori/`. Before the first index, add the
line `.byeori/` to `.git/info/exclude` of the repo that holds that folder (if not there yet). It is a
local ignore: no project file changes.

## Step 2 — index and search in one call

```bash
python -m byeori index __HQ && python -m byeori search __HQ "phrase with the concept" --top-k 5
```

- Always both: `index` is incremental (only changed sections re-embed) and cheap; without it you
  search stale docs.
- Folder: `__HQ` for our docs; the project's own docs folder for theirs. One folder per call.
- Modes: `--mode hybrid` (default, meaning + exact words), `semantic`, `lexical`. `--json` for machine
  output.
- Output = a file list, no lines. Then open the file with `get_codeblock --file F` (outline) and
  `--line N --query`. The outline shows each section's `> [!info]` note after its title: pick the
  section by it.

## Writing docs: the section note is mandatory

Every `##` / `###` section with content opens with a one-line callout right under the heading:
`> [!info] <what this section holds or decided>`. It names the concept in plain words, so the
search finds the file, and the outline then shows which section to open. Details:
`Guide__Doc`, `Guide__Outline`.

## Tips

- Short vague queries ("hermes") give noise. Write a phrase with the concept: "split the monster file
  faster", "who owns the card format".
- Russian and English both work (multilingual model).
- Nothing found → try `--mode semantic` with other words, then grep.

## Fallback — Vexor (only if already installed; don't install it yourself)

Slower (a real transformer; minutes to index hundreds of files), but gives lines and snippets and
sometimes catches a vague topic byeori misses. Index lives outside the folder (`~/.vexor/`).

```bash
vexor index -p __HQ -e .md -m full
vexor search "phrase" -p __HQ -e .md -m full -k 5 --format porcelain
```

Search must use the same `-p/-e/-m` as index. Scores are flat (~0.82–0.87): read the list, not the number.
