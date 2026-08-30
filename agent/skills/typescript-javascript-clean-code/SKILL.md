---
name: typescript-javascript-clean-code
description: Use when creating, modifying, reviewing, or refactoring JavaScript or TypeScript. Enforces readable naming, explicit boundaries, safe types, cohesive modules, simple control flow, and changes that remain easy to extend without speculative abstractions.
globs:
  - "**/*.js"
  - "**/*.jsx"
  - "**/*.mjs"
  - "**/*.cjs"
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*.mts"
  - "**/*.cts"
---

# JavaScript and TypeScript Clean Code

## Start with the repository

- Read nearby implementation, callers, tests, `package.json`, and compiler/linter configuration.
- Preserve the established module system, framework, formatter, and public API unless the task changes them.
- Reuse an existing helper or platform API before adding code or a dependency.

## Make intent obvious

- Name values by meaning: `retryDelayMs`, not `delay`; `hasPermission`, not `check`.
- Name functions by observable outcome. Avoid vague `handle`, `process`, `manage`, and `utils` names.
- Keep one abstraction level per function. Use early returns instead of deeply nested branches.
- Keep functions cohesive. Extract only when the extracted operation has a useful name or independent contract.
- Prefer plain objects and functions. Add classes only when identity, lifecycle, or encapsulated mutable state requires them.

## Use types to protect boundaries

- Never use `any`, `@ts-ignore`, or unchecked casts. Accept `unknown` at untrusted boundaries and narrow it.
- Model alternatives with discriminated unions instead of optional-field combinations or boolean flags.
- Make illegal states hard to construct. Validate external input once, then use the validated type internally.
- Let inference handle local implementation details; annotate exported APIs and ambiguous boundaries.
- Prefer `satisfies` when checking an object shape without widening its inferred type.
- Do not create wrapper types, generic parameters, or interfaces for a single speculative implementation.

## Keep modules easy to change

- Give each module one cohesive reason to change and expose the smallest useful public surface.
- Keep side effects at boundaries. Separate data transformation from I/O when that makes behavior independently testable.
- Pass dependencies explicitly when replacement is real; do not add factories or dependency injection for one fixed dependency.
- Avoid catch-all shared utility modules. Put behavior beside the domain concept that owns it.
- Delete obsolete exports, aliases, comments, and compatibility paths after migrating every caller.

## React and browser UI

- Preserve the repository's framework, router, state, data-fetching, component, and styling conventions. Do not add a second system for the same concern.
- Keep state at its nearest real owner. Distinguish server, URL, form, and local interaction state; do not mirror props into state.
- Prefer semantic HTML and native controls. Preserve accessible names, keyboard operation, visible focus, and reduced-motion behavior; use ARIA only to fill a native semantic gap.
- Make loading, empty, error, disabled, and retry states explicit. Prevent duplicate submissions while an async mutation is pending.
- Use existing design tokens and responsive primitives. Add memoization only for measured work or required referential stability.
- Exercise changed user journeys in the browser at relevant viewport sizes and inspect the accessibility tree, console, and failed network requests.

## Errors and asynchronous code

- Do not swallow failures. Add context while preserving the original error with `cause` when supported.
- Use `Promise.all` only for independent operations. Keep dependent work sequential and visible.
- Await promises or deliberately return/store them; never leave accidental floating promises.
- Preserve cancellation signals and timeouts across API boundaries when the surrounding code supports them.

## Comments and tests

- Comment constraints and non-obvious decisions, not line-by-line mechanics.
- Tests defend observable behavior, boundaries, precedence, and failure cases—not implementation structure.
- For a refactor, keep behavior unchanged and run the narrowest existing typecheck, lint, and test commands covering the change.

## Review checklist

- Can a reader understand names and control flow without comments?
- Is input validated at the trust boundary?
- Are exported types and failure semantics explicit?
- Does the change reuse existing code and remove the replaced path?
- Is every new abstraction required by a current second implementation or variation?
- Can the likely next change be made in one obvious place?
