---
name: prototype
description: Build a throwaway prototype to resolve a concrete logic, state-model, or UI design uncertainty. Use when the user requests a prototype or implementation is blocked by uncertainty that prose cannot settle reliably.
license: MIT
metadata:
  source: https://github.com/mattpocock/skills/tree/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/prototype
  source_commit: c55ee46073ed923f86ce59a5eb3b6d895095d1b7
  adaptation: OMP
---

# Prototype

A prototype is throwaway code that answers one named design question. It is not an implementation phase or a reason to add speculative code.

If the user did not explicitly request a prototype, state the unresolved question, explain why repository evidence and prose are insufficient, and get approval before creating prototype files.

## Choose the smallest branch

### Logic or state model

Default to a self-contained artifact in the OS temporary directory. Use plain HTML/JavaScript or the smallest language-native script that can expose inputs, actions, state transitions, and invalid cases. Keep state in memory unless persistence is the question being tested.

The artifact must display:

- the question it answers;
- the initial state and assumptions;
- the actions a reviewer can perform;
- the resulting state after each action;
- at least one normal path and one difficult boundary case.

### UI

First prefer a self-contained temporary HTML prototype. Use the real application only when routing, data density, component behavior, or design-system context is necessary to answer the question.

Before adding project-local prototype files, explain why a temporary artifact is insufficient and get explicit approval. Follow the existing framework and component system. Compare two to four structurally different variants, not color-only variations.

## Constraints

- Mark every artifact clearly as a prototype.
- Add no dependency unless the user explicitly approves it.
- Use no production credentials, services, or data.
- Avoid persistence and real mutations by default.
- Add no permanent tests, generalized abstractions, compatibility layers, or production error handling.
- Do not create branches, commits, tags, issues, or pull requests.
- Do not silently promote prototype code into production.

## Verify the question, not production readiness

Run the prototype and exercise the scenarios that distinguish the candidate decisions. For a web UI, inspect the actual rendered surface with the browser tools. Report what the experiment demonstrated and what remains uncertain.

## Cleanup

After the user accepts or rejects the result:

- capture the resulting decision in the requested durable location, if any;
- implement the chosen behavior separately under production standards when requested;
- remove temporary project-local prototype code and generated artifacts unless the user explicitly asks to retain them;
- leave OS-temporary artifacts outside the repository and report their location while they remain useful.
