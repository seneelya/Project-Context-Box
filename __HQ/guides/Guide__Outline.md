# Guide: Outline — cut markdown so the heading map is enough

`Guide__Doc` says what an as-built Doc contains. This says how **any** long markdown
(tracker entry, plan, doc, vision, recon) must be cut so it can be read as a book:

```
python __HQ/tools/get_codeblock.py --file <file.md> --outline --level 3
python __HQ/tools/get_codeblock.py --file <file.md> --line <N> --query
```

`--outline` prints headings and line ranges. `--query` fetches one range. If the titles
do not state their content, or one heading covers hundreds of lines, the map is useless
and the file gets read whole.

## The heading is the distillate

- The outline alone tells the story. A reader who never opens a body should know what
  each section decided or contains.
- Title = the result, not a label. `Plan11-Task05 done: buildContextView unblocks Plan12`
  works. `continuation`, `evening`, `notes` do not.
- One claim per heading. Several outcomes in one sitting are several headings, not one
  essay under one title.
- Depth stays at 2–3, and the scan is `--outline --level 3` so the third level is
  visible. Deeper than 3 means the file should be split, not nested further.

## A section is one fetch

- The body under a heading should fit one `--query`. Aim for under ~60 lines; split
  before ~80. A section past ~120 lines with no child heading has failed.
- Open the body with the one sentence the title could not hold. The rest is evidence.
- A fact you would grep for deserves its own heading. Do not leave it in the middle of
  a wall.

## A list is one fetch, not a map

In markdown the only split is an ATX heading. `--query` on a line in a section returns
that section's `~content` body: everything up to the next heading, glued into one block.
A numbered list, a bullet list, a `>` callout, a `---` rule, and a blank line do not
break it and do not show up in `--outline`.

Use that on purpose. Points that must be read together stay a short list under the
heading, and one `--query` brings them all back. A point that must be found from the
map gets its own heading. A blank line will not do it.

(A `.txt` file is the other tool: a blank line splits paragraphs, and two or more
`1.` / `-` markers in one paragraph become one landmark each. Our docs are markdown,
so that split does not apply.)

## When the file itself is the wall

- Past ~40 level-2 headings, or past ~1500 lines, split the file. The outline of a book
  is not a book. Tracker rotation → `Guide__Tracker`. A Doc that outgrows one subject →
  a new `Doc__<slug>`.
- Do not rewrite a chronological log to clean it up. New entries follow this guide;
  old walls stay as history.

## Check before you finish

Run `--outline --level 3`. If you cannot point at the section you need from those
titles alone, rename or split until you can.
