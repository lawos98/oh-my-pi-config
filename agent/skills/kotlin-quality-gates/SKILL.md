---
name: kotlin-quality-gates
description: Use whenever creating, modifying, reviewing, or refactoring Kotlin or Gradle Kotlin DSL. Follow repository ktlint and detekt conventions without suppressing failures; apply the global risk-based execution policy, with no mandatory quality commands.
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

## IDE Project Files

- This project uses IntelliJ IDEA; do not create Eclipse project files such as
  `.classpath`, `.project`, or `.settings/`.

## Generate compliant Kotlin

- Match established package layout, import ordering, naming, wrapping, indentation, trailing-comma, and expression-body conventions.
- Keep functions and classes cohesive. Prefer explicit domain names, early returns, immutable values, and exhaustive `when` expressions.
- Avoid unused abstractions, nested complexity, wildcard imports, magic numbers, swallowed exceptions, empty blocks, and nullable-state ambiguity.
- Respect the repository's blocking, coroutine, or reactive execution model.
- Remove dead code and obsolete imports introduced by the change.

## Preserve quality without hiding failures

- Never add `@Suppress`, detekt exclusions, baseline entries, `// ktlint-disable`, or Gradle ignore rules merely to make generated code pass.
- Never use `@Suppress("UNCHECKED_CAST")` or unchecked casts.
- When a rule conflicts with an external constraint, explain the constraint and request approval before changing quality configuration.
- Prefer precise source edits that follow repository style. Never run `ktlintFormat` or other formatters unless explicitly requested; protect unrelated user work. A failed check stops automatic repair, including source and test edits.

## Review and execution workflow

The global `RULES.md` execution policy applies to this skill and every subagent; only a later explicit user request authorizes retries or a different workflow.

1. Discover actual task names from repository Gradle configuration, not exploratory `tasks` commands.
2. Add or update meaningful tests when warranted. Use available LSP diagnostics as non-command feedback, and perform one end-of-change correctness self-review before any optional check. Do not run per-edit architecture reviews, automatic second reviews, or replacement model-verifier loops; small changes require no reviewer-model call.
3. For small, localized, low-risk changes, skip test, build, lint, and format runs unless requested. For larger or riskier work, choose at most one narrow relevant check invocation for the entire change, coordinated with the main agent. Do not bundle ktlint, detekt, and tests or escalate to broader suites.
4. Any test, build, lint, or format failure stops further validation and automatic repair, including LSP- or review-driven remediation. Report the exact command and concise actual failure, then await the user's next prompt; do not retry, fix tests, or substitute another check.
5. Report changes applied, tests added or updated, and tests not run or actual check outcomes separately. Identify missing tasks and unrun checks; never equate edits with verified correctness, claim unrun tests passed, or treat formatting as proof.

Never weaken tests, add suppressions or baseline entries, or change configuration to hide failures.
