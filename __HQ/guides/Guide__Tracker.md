# Guide: Tracker — folder and file

The tracker is the folder `__HQ/TRACKER/`. One entry is one file. There is no `TRACKER.md`.

```
__HQ/TRACKER/0042__Plan16-Task05-closed.md
```

**Name.** Four digits, zero-padded, only growing. A fifth digit would sort ahead of `9999`.
The next number is one more than the newest entry in the root. `0000__rule.md` is not an
entry: skip it for the number and for the tail. No entries yet → `0001`. The slug is
Latin, address then outcome (`Plan16-Task05-closed`), not a date and not `notes` /
`update` / `session`. Several outcomes are several files. A correction is a new file.

**Inside.** One claim, short enough to read the file whole. The marker line is English:
`◐ <address>` · `✅ <address> done → next <address>` · `⏸ <address> — <why>`.
The last line is always `→ next <address>`, copied from the newest entry. A fully
deferred chain goes to `__HQ/plans/deferred/`, not a `⏸` file.

**Read.** Only the newest entry file in the root.

**Archive.** Past ~40 files in the root, move the oldest by number into
`__HQ/TRACKER/archive/` unchanged. The newest entry stays. `0000__rule.md` stays.
