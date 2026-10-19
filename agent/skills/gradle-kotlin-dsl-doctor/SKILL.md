---
name: gradle-kotlin-dsl-doctor
description: Diagnose and repair Kotlin Gradle Kotlin DSL plugin resolution, dependency alignment, toolchains, source sets, generated sources, task wiring, and test/runtime classpaths with minimal compatible edits.
license: MIT
metadata:
  source: https://github.com/yalishevant/kotlin-backend-agent-skills
  source_commit: fd0ed521d22efd28221d532c9abab97af0b9bf0e
---

# Gradle Kotlin DSL Doctor

Repair the build model, not the symptom. Preserve repository version authority and Kotlin DSL conventions; do not introduce a second dependency-management scheme.

## Read before editing

Read the reported failing command and first meaningful error; do not rerun a reported failure to confirm it. Inspect relevant settings/root/module scripts, wrapper properties, catalogs, convention plugins/included builds, Gradle properties, lockfiles and verification metadata. Avoid exposing repository credentials or secrets from properties and logs.

Identify the owning layer for each relevant version: Gradle wrapper, JDK/toolchain, Kotlin/compiler plugins, framework plugin/BOM/platform, catalog, convention plugin or explicit override. Compare the actual compatibility requirements in version-matched official documentation, not remembered latest versions.

## Classify and trace

- Plugin resolution: plugin repositories, `pluginManagement`, catalog aliases, included build and plugin application scope.
- Kotlin DSL/accessors: plugin application timing, receiver type and generated accessors; do not replace Kotlin DSL with Groovy syntax.
- Dependency/variant resolution: selected platform constraints, `platform` versus `enforcedPlatform`, capabilities, JVM attributes, classifier, substitution and local versus published artifacts.
- Compiler/toolchain: Gradle runtime JDK versus compile toolchain, Java/Kotlin targets and matching Kotlin compiler plugins. Check Spring plugin only for Spring proxy-dependent code; serialization plugin only for the serializer actually used.
- Source sets/code generation: existing KAPT/KSP conventions, generated outputs, task dependencies, test fixtures and runtime classpaths.
- Task/model issues: lazy registration versus eager access, configuration-cache requirements, convention-plugin scope and executable versus library packaging.
- CI-only differences: documented JDK/vendor, wrapper, flags, repository access and environment configuration. Never print credentials to diagnose them.

## Patch narrowly

Keep existing framework-managed versions where authoritative; Spring Boot BOM advice applies only to Boot projects, not automatically to Ktor or plain Kotlin modules. Remove an explicit version only after establishing that the intended platform manages it. Do not invent version pins, add repositories, force dependency versions or use blanket exclusions to hide incompatible constraints. Preserve locks and verification policy; do not clear caches as a substitute for fixing the model.

Edit the owning module or convention, not every similar build file. Explain the dependency edge when several modules genuinely require a change. Do not bundle upgrades, unrelated formatting, persistence-framework setup or language migration with a build repair.

## Verification boundary

Select one narrow repository-supported command that answers the actual uncertainty: for example a module's configured compile task for a compiler issue, or configuration-specific `dependencyInsight` for a resolution issue. These are alternatives, not a sequence. Do not run `help`, compilation, tests and `build` in succession. Never run a formatter unless explicitly requested.

Session execution policy takes precedence: propose the command when execution is not authorized; share the single allowed invocation with the coordinator when it is. A failed check stops validation and automatic repair; report its exact command and error and await instructions. Never retry, substitute another check, weaken gates, add baselines or suppress failures.

Return the failing layer and evidence, minimal patch, compatibility reason, one recommended check with its actual/unrun status, and any unresolved risk. Use the repository wrapper, not a globally installed Gradle.

## Provenance

Adapted from the pinned upstream `.agents/skills/gradle-kotlin-dsl-doctor/SKILL.md`, reviewed 2026-10-17. Removed persistence-framework setup and escalating command lists. Passive guidance only; see `LICENSE` and `provenance.json`.
