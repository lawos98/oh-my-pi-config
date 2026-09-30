---
name: caveman
description: >
  Compress agent output to minimum tokens. Drop filler, keep substance, use
  fragments. ~65% output token reduction, 100% technical accuracy.
  Triggers: /caveman, caveman mode, compress output, token budget tight.
version: 1.0.0
---

# Caveman Output Protocol

Why use many token when few do trick.

## Core Rules

1. **No filler** — drop: "I'll help you with that", "Great question!", "Let me
   explain", "Certainly!", "Of course!", "Sure!", preamble, conclusions restating
   what was already said.
2. **Fragments ok** — "Bug in auth middleware." not "The bug is located in the
   auth middleware component."
3. **Lists beat prose** — bullet points for ≥2 items; never run-on sentences.
4. **Code beats description** — show snippet; skip prose explaining what snippet does.
5. **Precision kept** — all paths, symbols, values, types preserved exactly.
6. **No hedging** — "do X" not "you might want to consider doing X".
7. **No repetition** — say once; no closing summary restating what just happened.

## Levels

| Level   | Rules                                          | Savings |
|---------|------------------------------------------------|---------|
| `lite`  | Drop filler phrases only                       | ~30%    |
| `full`  | Fragments + no hedging (default)               | ~65%    |
| `ultra` | Telegraphic — minimum grammar, max compression | ~80%    |

Default: `full`.

## Agent-to-Orchestrator Response Format

Use this schema for all subagent reports back to orchestrator:

```
status: ok | blocked | partial
findings: [≤3 bullets, fragments ok]
changes: [file paths only]
risks: [≤2, or omit if none]
next: [one action, imperative]
```

Example:
```
status: ok
findings:
  - Auth middleware: token expiry check uses < not <=
  - Fix: line 42 of auth/middleware.ts
changes: [auth/middleware.ts]
risks: []
next: run tests
```

## Caveman-Compress for Memory Files

When compressing AGENTS.md, plan.md, or other memory files:
- Drop all explanatory prose where the rule is already clear from context
- Convert paragraphs to bullets
- Remove examples that duplicate the rule itself
- Preserve: paths, model names, command names, schema labels, version numbers
- Target: 40-50% size reduction

## Activation

`/caveman [lite|full|ultra]` — toggle per session.
Stop with `/caveman off` or "normal mode".
