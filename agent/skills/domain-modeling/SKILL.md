---
name: domain-modeling
description: Build and sharpen project-specific domain vocabulary. Use when terminology is ambiguous, conflicting, or being added to CONTEXT.md or CONTEXT-MAP.md.
---

# Domain Modeling

Maintain the shared language of the problem domain. This skill owns domain terms and their relationships; `documentation-and-adrs` owns technical documentation and architectural decisions.

Reading an existing glossary for context does not activate this workflow. Use it when the vocabulary itself is changing or needs clarification.

## Locate the context

- If `CONTEXT-MAP.md` exists, follow it to the relevant bounded context.
- Otherwise use the root `CONTEXT.md`.
- If neither exists, create a root `CONTEXT.md` only after the first project-specific term is settled.

Use [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md) and match an established repository format when one exists.

## Sharpen the language

1. Compare the user's term with the existing glossary and code.
2. Surface conflicts immediately: distinguish overloaded concepts rather than merging them.
3. Test candidate definitions with concrete edge cases and relationships.
4. Choose one canonical term and record meaningful avoided synonyms.
5. Update the glossary as soon as the term is settled.

Definitions state what a concept is, not how the current implementation represents it. Keep transport types, database fields, class names, operational instructions, feature requirements, and implementation decisions out of `CONTEXT.md`.

## Cross-check

When the described domain conflicts with observable code behavior, report the mismatch and ask which represents the intended model. Do not silently rewrite the glossary to match accidental implementation behavior.

## Completion

The vocabulary work is complete when every disputed term in the current discussion has one concise definition, its important distinction from neighboring terms is explicit, and the applicable glossary contains no implementation detail introduced by this change.