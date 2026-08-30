---
name: kotlin-quality-gates
description: Use whenever creating, modifying, reviewing, or refactoring Kotlin or Gradle Kotlin DSL. Keeps AI-written Kotlin compliant with the repository's existing ktlint and detekt configuration, fixes root causes instead of adding suppressions, and requires the narrowest applicable Gradle quality tasks before completion.
globs:
  - "**/*.kt"
  - "**/*.kts"
---

# Kotlin Quality Gates

## Read repository policy first

- Inspect nearby Kotlin, `.editorconfig`, detekt configuration, root and module Gradle files, and existing quality-task conventions.
- Treat repository configuration as authoritative. Do not impose generic ktlint or detekt defaults over configured rules.
- Do not add, upgrade, or reconfigure ktlint, detekt, Gradle plugins, baselines, or dependencies unless explicitly requested.
- Do not edit machine-generated files under build/generated directories; change their generator or source template.

## Generate compliant Kotlin

- Match established package layout, import ordering, naming, wrapping, indentation, trailing-comma, and expression-body conventions.
- Keep functions and classes cohesive. Prefer explicit domain names, early returns, immutable values, and exhaustive `when` expressions.
- Avoid unused abstractions, nested complexity, wildcard imports, magic numbers, swallowed exceptions, empty blocks, and nullable-state ambiguity.
- Respect the repository's blocking, coroutine, or reactive execution model.
- Remove dead code and obsolete imports introduced by the change.

## Fix findings at the source

- Never add `@Suppress`, detekt exclusions, baseline entries, `// ktlint-disable`, or Gradle ignore rules merely to make generated code pass.
- Never use `@Suppress("UNCHECKED_CAST")` or unchecked casts.
- When a rule conflicts with an external constraint, explain the constraint and request approval before changing quality configuration.
- Prefer a precise source edit over running a formatter across unrelated modules. Use an existing format task only when its scope is understood and unrelated user work is protected.

## Verification workflow

1. Discover the repository's actual tasks from Gradle configuration or `./gradlew tasks --all`; do not assume task names.
2. Run the narrowest ktlint check covering the changed module or files.
3. Run the narrowest detekt task covering the changed module.
4. Run focused tests for changed behavior.
5. Run the repository's broader quality gate only when required by its conventions or the requested scope.
6. Report the exact tasks and outcomes. A formatter run is not evidence that checks passed.

Do not silently skip a missing or failing quality task. Report the task name, failure, and affected files.
