---
name: clean-code
description: >-
  Use when creating or modifying code, reviewing code, or discussing architecture and design.
  Apply SOLID principles plus Clean Code craft for naming, functions, classes, dependencies,
  interfaces, refactoring, and code smells. Complementary to linting, formatting, and tests.
category: code-quality
risk: safe
source: merged
tags: [clean-code, solid, uncle-bob, code-review, craftsmanship, architecture]
---

# Clean Code

Use this skill for code-quality decisions beyond syntax: naming, structure, dependencies,
boundaries, and maintainability. Prefer the smallest design that preserves the observable
contract and remains easy to change.

It covers:
- cohesive responsibilities and searchable domain vocabulary
- dependency and boundary decisions
- practical refactoring and code-review heuristics
- behavior-preserving tests and error handling

## When to Use

- Creating or modifying classes, modules, or functions
- Designing interfaces or inheritance hierarchies
- Adding behavior or changing an observable contract
- Reviewing coupling, duplication, or unclear ownership
- Deciding whether to extract, split, or invert dependencies
- Refactoring toward clearer, more maintainable code

## Core Rules

- Keep each unit cohesive and give it an obvious responsibility.
- Choose existing code, language features, framework capabilities, or installed dependencies before adding an abstraction.
- Depend on abstractions at real replaceable, isolatable, or independently contracted boundaries; use a direct concrete dependency when no such boundary exists.
- Make invalid states difficult to represent and preserve existing contracts.
- Introduce patterns only when they solve a current problem.
- Refactor in small, behavior-preserving steps.

## SOLID Principles

| Principle | Rule |
|-----------|------|
| S — Single Responsibility | Keep one cohesive reason for a unit to change |
| O — Open/Closed | Keep stable policy separate from variation when variation is real |
| L — Liskov Substitution | Subtypes must honor the complete parent contract |
| I — Interface Segregation | Interfaces should match the capabilities their clients use |
| D — Dependency Inversion | Isolate policy from replaceable implementation details |

### S — Single Responsibility

- Keep orchestration, persistence, formatting, and business rules separate when they have different ownership or change pressure.
- Extract only when the extracted code has a cohesive responsibility, names a real repeated concept, or forms an external boundary with its own contract.
- Do not split a clear flow into fragments merely to make units look smaller.

**Red flags:**
- Many unrelated public operations share one unit
- Section comments are needed to navigate mixed responsibilities
- A change to one concern risks unrelated behavior

### O — Open/Closed

- Keep a stable policy closed to accidental changes when a genuine variation point exists.
- For a small, fixed set of cases, direct control flow is often clearer than a strategy or plugin.
- Introduce polymorphism, a strategy, or a plugin when independent implementations or recurring change make the boundary useful.

### L — Liskov Substitution

- Do not create subtypes that throw, silently do nothing, weaken guarantees, or change meaning.
- If a type cannot honor the parent contract, use composition or a capability-specific abstraction instead.

### I — Interface Segregation

- Shape interfaces around cohesive client capabilities.
- Do not force clients to depend on unused operations.
- Do not add an interface solely to hide one fixed implementation or make trivial code appear testable.

### D — Dependency Inversion

- Keep domain policy independent from replaceable transport, storage, framework, or vendor details when that separation protects a real rule.
- Inject dependencies at composition or adapter boundaries when callers need replacement, isolation, or an independent contract.
- Do not hide simple, fixed dependencies behind pass-through interfaces.

## Clean Code Craft

### Naming

- Use intention-revealing, searchable, pronounceable names.
- Class names usually name domain things; method names usually describe actions or observable outcomes.
- Prefer explicit domain names over vague `Manager`, `Processor`, `Handler`, `Data`, or `Utils`; a generic name is acceptable only when it is genuinely the domain term.
- Avoid disinformation, unexplained abbreviations, and near-duplicate names.

**Good:** `elapsedTimeInDays`, `postPayment`, `UserRepository`
**Bad:** `d`, `genymdhms`, `Data`, `Manager`

### Functions

- Keep a function at one readable level of abstraction and make its success path easy to follow.
- Extract a helper when it exposes a real concept, owns a cohesive responsibility, has an independently useful contract, or crosses an external boundary.
- Keep parameters explicit. Group them only when the group is a real domain concept or enforces an invariant.
- Avoid hidden side effects and boolean-flag combinations that obscure behavior.

### Classes

- Keep classes focused and cohesive.
- Prefer composition when behavior varies or when inheritance would weaken contracts.
- Minimize public surface area and split by responsibility, not convenience.

### Comments

- Prefer clear code over narration.
- Comments explain constraints, provenance, legal requirements, or surprising trade-offs.
- Remove stale comments and rewrite code that needs a comment merely to describe its mechanics.

### Formatting

- Put high-level ideas before implementation details.
- Keep related lines together and use spacing to show structure.
- Follow the repository's formatter and established layout.

### Error Handling

- Make failure semantics explicit at the boundary that owns them.
- Preserve causes and context; do not silently fall back or expose internal details through public errors.
- Use exceptions, result types, or sentinels according to the language and repository convention; do not force one mechanism everywhere.
- Do not return or pass null where a validated type, explicit optional, or domain error can prevent ambiguity.

### Tests

- Test observable behavior, invariants, boundaries, transitions, and meaningful failure modes.
- Keep tests deterministic and independent where the repository's test framework supports it.
- When using TDD, write the failing behavior test before implementation.
- Design code so behavior can be tested without replacing every internal detail with a mock.

## Architecture and Boundaries

- Business rules should live inward from UI, transport, frameworks, databases, and vendors when that separation protects policy.
- Map request, document, SDK, and vendor representations at the edge instead of making them the domain model by convenience.
- Keep adapters responsible for translation, I/O, and persistence; they should not make business decisions.
- Encapsulate mutable state and representation behind operations that preserve invariants.
- Dependencies point toward stable policy across a real boundary; otherwise prefer the simpler direct relationship.

## Patterns

- Use a pattern only to address current duplication, rigidity, variation, or an external contract.
- Reuse a shared abstraction when callers need the same behavior, invariant, and failure semantics. Similar syntax alone is not enough.
- Prefer direct control flow to speculative factories, strategies, repositories, event buses, or extension points.
- Name a pattern when doing so clarifies the domain or the contract; do not introduce pattern vocabulary for ceremony.

## Common Smells

| Smell | Meaning |
|------|---------|
| Rigidity | A legitimate change requires unrelated edits |
| Fragility | A change breaks behavior outside its ownership |
| Immobility | Code is hard to reuse because concerns are entangled |
| Viscosity | The safe or correct change is harder than a risky shortcut |
| Needless complexity | Abstraction or indirection has no current owner or benefit |
| Needless repetition | One invariant or policy has multiple owners |
| Opacity | Names or control flow hide the behavior |

## Refactoring Heuristics

1. Make the behavior correct.
2. Make the design clear.
3. Improve efficiency when evidence calls for it.

- Fix one concern at a time and preserve observable behavior.
- Refactor code you are already touching when the ownership improvement is clear.
- Record genuine unresolved debt in the repository's normal tracking system; do not add comments that merely defer understanding.

## Error Proofing

- Validate untrusted input at the boundary, then use validated types internally.
- Prefer enums, sealed types, and value objects when they enforce a domain invariant.
- Fail fast at startup when configuration is invalid and continuing would make later failures ambiguous.

## Quick Review Checklist

- [ ] Does each unit have a cohesive responsibility?
- [ ] Are names explicit, searchable, and outcome-oriented?
- [ ] Are extraction and reuse justified by a real concept, boundary, or shared policy?
- [ ] Are dependencies direct or abstracted for a demonstrated reason?
- [ ] Are interfaces focused and honored by their implementations?
- [ ] Are inheritance relationships safe and meaningful?
- [ ] Are comments limited to constraints, provenance, and surprising trade-offs?
- [ ] Do tests protect observable behavior and meaningful failure modes?
- [ ] Are patterns solving a current problem rather than adding ceremony?

## What This Skill Is Not

- It is not a linter or formatter.
- It is not a replacement for tests or repository-specific conventions.
- It is not permission to over-engineer or to treat size, coverage, duplication, or complexity metrics as quotas.
