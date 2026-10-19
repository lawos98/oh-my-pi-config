---
name: kotlin-spring-proxy-compatibility
description: Diagnose Kotlin Spring AOP interception failures involving transactions, caching, async, method security, retry, configuration proxies, final classes or methods, compiler plugins, and self-invocation.
license: MIT
metadata:
  source: https://github.com/yalishevant/kotlin-backend-agent-skills
  source_commit: fd0ed521d22efd28221d532c9abab97af0b9bf0e
---

# Kotlin Spring Proxy Compatibility

Own Spring interception mechanics, not general service design or Ktor plugins. A compiled annotation is not proof that advice runs.

## Trace the actual call

Read the annotated declaration, external and internal callers, bean creation/registration, interface, relevant advisor configuration and tests. Read wrapper, build/catalog/convention plugins and the repository's Spring/Kotlin versions. Establish whether this path uses JDK interface proxies, class-based proxies, weaving or no interception mechanism.

1. Is the feature enabled and the target managed by Spring, or manually constructed?
2. Does the call cross the managed proxy? Ordinary self-invocation bypasses proxy advice; constructors and initialization are not ordinary calls through the completed proxy.
3. Is the target method interceptable under the actual strategy and framework version? Check final classes/methods, visibility, interface exposure and the declaration carrying the annotation.
4. Does the relevant module apply the matching Kotlin Spring/all-open compiler plugin, including any custom meta-annotation configuration? Do not assume source annotations changed compiled openness.
5. Does advice run but produce a different result because of propagation, rollback rules, key computation, authorization logic or advisor ordering?
6. Does a thread, Reactor or coroutine boundary lose transaction, security, logging or request context? Proxy presence alone proves none of those propagate correctly.

## Fix the broken mechanism

Use an existing compiler-plugin convention when missing openness is the cause. If a call bypasses a proxy, put the required boundary on an externally invoked managed method or move the responsibility into an existing appropriate bean. Change interface/proxy strategy only when evidence requires it. Do not make every class open, scatter annotations, create needless services or introduce self-injection/`AopContext` as the default repair.

Inspect combined retry/transaction/cache/security advisor ordering when relevant. An async method does not inherit all thread-local state by magic. Configuration method calls behave differently with `proxyBeanMethods = false`; preserve the intended bean lifecycle rather than treating that setting as cosmetic. Transactional event listeners require the configured transaction phase and fallback semantics.

Use `kotlin-spring-backend` for service, validation and transaction design; use `gradle-kotlin-dsl-doctor` only when build wiring is the cause. Do not add persistence-framework guidance or migration work to this diagnosis. Ktor route/plugin lifecycle is a different mechanism, handled by `ktor-runtime-troubleshooting`.

## Evidence and verification

State the expected advice, exact caller-to-target path, evidenced interception failure, minimal fix and remaining context/ordering risks. Add a focused behavioral test through the injected bean that demonstrates rollback, cache effect, authorization denial or other actual advice behavior; a proxy-class assertion alone is insufficient. Select one repository-supported check for the coordinator. Do not execute checks or repeat Gradle commands unless session policy explicitly permits; stop on any failed check.

## Provenance

Adapted from the pinned upstream `.agents/skills/kotlin-spring-proxy-compatibility/SKILL.md`, reviewed 2026-10-17. Persistence-entity and Java-migration guidance excluded. Passive text only; see `LICENSE` and `provenance.json`.
