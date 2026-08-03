# Guide: Context — how to shape a context (the reading manifest)

A `Context` file is the **instruction for assembling context** for a task — what to read to do the
work. The **Plan** role compiles it (it holds the knowledge now); the executor consumes it and reads
little.

Put in it:
- **Facts you KNOW** → inline them (the executor then reads nothing for those).
- **Zones you are UNSURE about** → point coarsely ("explore here: `dir/…`"); do NOT fake `§`-precision.
- **"Read only this."** The executor must not blind-search beyond the manifest; if it is insufficient,
  the executor STOPS and asks.

It **improves over time**: when an executor hits a gap, it appends what was missing → the next run is
sharper (compile-once, refine-over-time).
