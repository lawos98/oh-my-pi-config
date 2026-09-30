---
name: writing-for-agents
description: Write or revise agent-facing instructions. Use when creating or editing skills, AGENTS.md, CLAUDE.md, rules, or documents reached by those instructions.
license: MIT
metadata:
  source: https://github.com/mattpocock/skills/tree/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/productivity/writing-for-agents
  source_commit: c55ee46073ed923f86ce59a5eb3b6d895095d1b7
  adaptation: OMP
---

# Writing for Agents

Write agent-facing documents so the agent follows a reliable process rather than merely producing familiar-looking output.

When editing a skill, also read [SKILL-MECHANICS.md](./SKILL-MECHANICS.md).

## Context pointers

A context pointer names material outside the current context and states exactly when to load it. Skill descriptions and references in `AGENTS.md` are context pointers.

A useful pointer:

- starts with the capability or trigger;
- names each genuinely distinct branch that should load the target;
- omits identity and detail already available in the target;
- is strong enough that required material is not skipped.

Always-loaded pointers spend context on every turn. Keep them short and precise.

## Information hierarchy

Organize content by when the agent needs it:

1. **Steps** — ordered actions required for this workflow.
2. **Local reference** — rules needed by most branches.
3. **Disclosed reference** — branch-specific detail in a linked sibling file.

Keep common steps in the main document. Move large or branch-specific reference behind a precise pointer. Keep each concept's definition, rules, and caveats together.

Split a document only when the split reduces context or prevents later steps from pulling attention away from the current step. Do not split merely to shorten files.

## Completion criteria

Every step needs a checkable finish condition. Prefer exhaustive criteria such as “every modified public symbol has a migration decision” over vague criteria such as “review the API.”

A completion criterion must say:

- what evidence exists when the step is complete;
- which items must all be covered;
- what blocks advancing to the next step.

## Leading words

Use a compact, established term when it can anchor repeated behavior, such as *frontier*, *seam*, *red*, or *tracer bullet*. Define it once, then reuse the term instead of repeating its explanation. Prefer existing vocabulary over invented jargon.

Phrase instructions toward the desired behavior. Reserve prohibitions for hard safety boundaries and pair them with the positive action to take instead.

## Pruning

Keep one source of truth for each rule. Before retaining a sentence, ask whether it changes model behavior compared with the default.

Remove:

- duplicated rules;
- facts cheaply discoverable from configuration or code;
- stale workflow descriptions;
- speculative branches;
- generic encouragement without an observable effect.

Preserve unwritten conventions, reasons, safety constraints, and non-obvious completion criteria.

## Review checklist

- The description names the exact invocation branches.
- Steps are ordered and end in checkable outcomes.
- Branch-specific material is disclosed rather than mixed into the main path.
- Each rule has one authoritative location.
- Repository configuration is referenced instead of copied.
- Safety requirements state both the prohibition and the correct alternative.
- Examples reinforce the contract rather than add a competing one.
