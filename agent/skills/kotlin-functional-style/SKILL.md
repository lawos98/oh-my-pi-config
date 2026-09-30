---
name: kotlin-functional-style
description: >-
  Kotlin functional-style guidance for readable expression-oriented code,
  collection transformations, null safety, extension functions, and restrained
  use of scope functions. Use when writing or reviewing Kotlin code, especially
  Kotlin Spring services. Triggers: Kotlin functional style, Kotlin expressions,
  scope functions, let also run apply with, map filter fold, Elvis operator,
  Kotlin readability.
---

# Kotlin Functional-Style Guidance

This is supplemental guidance. The target repository's `AGENTS.md`, contracts,
tests, and existing Kotlin Spring architecture conventions prevail. In
particular, this skill does not replace or contradict
`kotlin-spring-hexagonal-service`.

## Principle

Prefer clarity over functional density. When the result stays equally clear or
clearer, avoid imperative `if` statements, loops, and mutable `var` state:
prefer expressions, `when`, null-safe operators, collection transformations,
and immutable `val` values. This is a preference, not a blanket ban—use `if`,
loops, mutation, builders, and `try`/`catch` when they are clearer, safer, or
required by framework APIs.

## Imports

Prefer direct imports for enum constants and other static members when ownership
is unambiguous. For example, import `MigrationMode.NOT_MIGRATED` and use
`NOT_MIGRATED` rather than repeating `MigrationMode.NOT_MIGRATED`. Keep the
qualified form when a direct import would cause ambiguity or make ownership
harder to understand.

## Expressions and Branching

- Use expression bodies for short, obvious functions.
- Use `when` for multiple exclusive cases, especially sealed hierarchies.
- `if` remains correct and preferred for simple two-way decisions,
  clarity-critical conditions, and smart-cast conditions. Never adopt
  no-`if` absolutism; first consider whether an expression, guard clause, or
  `when` makes the intent clearer.

```kotlin
fun nextLabel(state: State): String = when (state) {
    State.New -> "new"
    State.Done -> "done"
}
```

## Null Safety

- Use safe calls, `?.let`, and Elvis (`?:`) for clear defaults or guard clauses.
- Use `takeIf` when it directly names an eligibility condition.
- Avoid nested scope-function pyramids and validation hidden inside lambdas.

```kotlin
fun requiredUserId(request: Request): String {
    return request.userId?.takeIf { it.isNotBlank() }
        ?: throw IllegalArgumentException("userId is required")
}
```

## Collections

- Use `map`, `filter`, `mapNotNull`, `flatMap`, `associate`, `groupBy`, and
  `fold` for clear transformations.
- Use `Sequence` only for a proven large-input or lazy-processing benefit.
- Prefer loops for early exit, complex state, indices, or folds that become hard
  to read; otherwise prefer an immutable collection pipeline over loop-driven
  mutable accumulation.

```kotlin
val activeIds = users.mapNotNull { user ->
    user.id.takeIf { user.active }
}
```

## Scope Functions

Choose scope functions by intent:

- `let`: nullable transformation or a limited context.
- `also`: visible side effects while preserving the subject.
- `run`: compute a receiver-based result.
- `apply`: configure an object and return it.
- `with`: group operations on a known receiver.

Avoid chains used only to eliminate names.

## Extension Functions

- Use extensions for cohesive mappings, predicates, and domain vocabulary; place
  them near their conceptual type.
- Preserve existing `toDomain` / `toEntity` conventions.
- Never conceal IO, transactions, mutation, network calls, or surprising side
  effects in an extension.

```kotlin
fun UserDto.toDomain() = User(id = id, displayName = name.trim())
```

## Function Extraction

- Keep one business transformation per line.
- Extract a private function when a lambda contains branching or multiple
  business decisions; make it public only for an intentional API or port.
- Name intermediate business values. Avoid clever one-liners and non-local
  lambda returns.

## Spring Boundaries

Do not weaken hexagonal ports and adapters, constructor injection, synchronous
`RestTemplate`, `MongoOperations`, error mapping, logging, observability, or
existing Kotest conventions. Keep side effects explicit at application and
adapter boundaries. Builder APIs, `try`/`catch`, and local mutation are valid
where natural and readable.

## Review Checklist

- Does the code favor clarity over functional density?
- Are expressions, `when`, and `if` selected for the clearest branching form?
- Where equally clear, did the code avoid imperative `if`, loops, and mutable
  `var` state in favor of immutable expressions and collection transformations?
- Are null guards explicit, without nested scope pyramids or hidden validation?
- Are collection operators clear, with loops used where they improve readability?
- Does each scope function communicate its specific intent?
- Are extensions cohesive and free of concealed side effects?
- Are lambdas small, business values named, and multi-decision logic extracted?
- Are hexagonal, Spring, persistence, error-handling, logging, observability,
  and Kotest conventions preserved?
- Does the change preserve the target repository's `AGENTS.md`, contracts,
  tests, and established conventions?
