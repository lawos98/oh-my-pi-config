---
name: simplify-code
description: Directly remove duplication and accidental complexity while preserving observable behavior.
---

Simplify the requested code directly. Do not return a list of refactoring suggestions when the code can be changed safely.

1. Read and apply `simplify`, `software-architecture`, `clean-code`, and the relevant language/framework quality skill.
2. Read the full affected implementation, every caller of the symbols to change, tests, configuration, and public or persisted contracts. Use LSP references for symbol-aware call sites.
3. Establish the current observable behavior, error paths, side-effect ordering, performance-sensitive paths, and existing verification before editing.
4. Remove dead code, duplicate business rules, unnecessary wrappers, speculative abstractions, vague names, deep nesting, boolean-flag control flow, and parallel compatibility paths within the requested scope.
5. Reuse existing code. Extract only a real shared concept with the same invariant and failure semantics; do not create a generic helper merely because two blocks look similar.
6. Prefer direct control flow and cohesive modules. Keep meaningful names and boundaries that protect behavior, testability, or an actual variation.
7. Preserve outputs, failures, side effects, ordering, public APIs, persisted data, and performance characteristics unless the user explicitly requests a behavior change.
8. Update every caller and delete the replaced path. Do not add deprecations, aliases, suppressions, or comments that keep obsolete structure alive.
9. Run LSP diagnostics on every edited source file and the narrowest applicable tests, typecheck, lint, and build checks. For a reported bug or runtime concern, exercise the original path after the refactor.
10. Report what was simplified and the actual verification evidence. Do not append unrelated improvement suggestions.

Stop without changing a construct when its behavior cannot be established from code, tests, or runtime evidence. Do not commit, push, change branches, or refactor unrelated files.
