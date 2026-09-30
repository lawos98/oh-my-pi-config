---
name: improve-codebase-architecture
description: Survey architectural friction and deep-module opportunities. Use when the user requests an architecture improvement survey; when implementation or debugging exposes scattered ownership or shallow modules, suggest this survey but wait for approval before running it.
license: MIT
metadata:
  source: https://github.com/mattpocock/skills/tree/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/improve-codebase-architecture
  source_commit: c55ee46073ed923f86ce59a5eb3b6d895095d1b7
  adaptation: OMP
---

# Improve Codebase Architecture

Survey for deepening opportunities: changes that put substantial behavior behind a smaller interface, improve locality, and create a useful test seam.

A broad survey runs only after an explicit user request. If another task merely reveals architectural friction, name the evidence and offer the survey without interrupting the current work.

## 1. Scope the survey

Use the scope the user names. Otherwise identify the smallest relevant hotspot from current work, recent changes, or repeated maintenance friction. Do not turn a local concern into a repository-wide audit without approval.

Read before evaluating:

- `CONTEXT.md` or the applicable entry from `CONTEXT-MAP.md`;
- ADRs governing the area;
- relevant implementation, callers, configuration, and tests;
- the `codebase-design` skill for module, interface, depth, seam, adapter, leverage, locality, and the deletion test.

Use read-only scouts only when independent areas justify parallel exploration.

## 2. Find evidence-backed candidates

Look for:

- understanding one behavior requiring many shallow modules;
- an interface nearly as complex as its implementation;
- policy duplicated across callers;
- coupled modules leaking knowledge across a seam;
- tests reaching through an interface because the seam is misplaced;
- a frequently changed area where better locality would repay the refactor.

Apply the deletion test. If deleting a module removes complexity rather than concentrating it elsewhere, the module is probably weightless and should be removed rather than deepened.

Reject candidates that are speculative, contradict an ADR without material new evidence, or introduce a seam with only one fixed adapter.

## 3. Report in chat

Return at most five ranked candidates. For each include:

- **Strength:** Strong, Worth exploring, or Speculative.
- **Files:** exact relevant paths.
- **Evidence:** concrete friction observed.
- **Current shape:** modules, interfaces, and leaking knowledge.
- **Deepening move:** responsibility to concentrate and interface to simplify, without prematurely designing every method.
- **Payoff:** locality, leverage, and the resulting test surface.
- **Cost or conflict:** migration risk, affected callers, and relevant ADRs.

End with one top recommendation and why it has the best evidence-to-cost ratio. If no candidate clears the bar, say so; a clean survey is a valid outcome.

Do not create HTML, load external CDNs, edit production code, or create architecture documents during the survey. After reporting, ask which candidate—if any—the user wants to explore.
