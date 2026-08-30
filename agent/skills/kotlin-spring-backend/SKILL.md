---
name: kotlin-spring-backend
description: Use for implementing, reviewing, testing, or debugging Kotlin Spring Boot backend services. Inspect the repository's actual build, starters, runtime model, and persistence before giving stack-specific advice.
---

# Kotlin Spring Backend

## Discovery

Before editing, inspect the repository's build, configuration, package structure, entry points, domain types, persistence adapters, deployment manifests, and tests. Establish facts before prescribing a pattern:

1. Read the Gradle wrapper/build scripts and version catalogs, or the Maven wrapper and POMs. Record the actual Spring Boot, Kotlin, JDK/toolchain, and dependency-management versions.
2. Identify the starters and managed dependencies actually present, such as `spring-boot-starter-web`/Spring MVC, `spring-boot-starter-webflux`, security, validation, actuator, persistence, HTTP clients, and test infrastructure. Do not add a library merely because a recommendation commonly uses it.
3. Trace representative request and persistence paths. Classify each boundary as servlet MVC, Reactor WebFlux, Kotlin coroutine (`suspend`/`Flow`), or mixed. Check controller return types, adapters, schedulers/dispatchers, and client APIs; a module name or one dependency is not enough to describe every path.
4. Preserve the discovered execution model. Do not introduce blocking work into a reactive event loop, `runBlocking` into request handling, or an accidental Reactor/coroutine bridge without an explicit, cancellation-safe boundary.

When a repository has mixed boundaries, document the boundary and keep one execution model inside each path. Advice below is conditional: apply only the parts supported by the discovered versions, starters, and deployment.

## Design

Keep controllers thin. Put business invariants in domain/application services and persistence mechanics behind repositories or gateways. Prefer explicit types and boundaries over reflection-heavy or generic abstractions. Reuse an existing dependency and configuration convention before adding another one.

### Configuration and validation

- Group related settings in immutable, typed `@ConfigurationProperties` classes using the repository's existing registration and constructor-binding style. Prefer types such as `Duration`, `URI`, and `DataSize` over unvalidated strings.
- If the repository includes Spring's validation support, validate configuration at startup with its established `@Validated`/Bean Validation pattern. Required, unsafe, or mutually inconsistent values should fail startup rather than silently fall back.
- Trace profile and environment overrides, and keep secrets in the repository's existing secret-management path. Never log bound properties, credentials, tokens, or complete connection strings; ensure management endpoints redact them.

### Transactions

Use `@Transactional` only when the actual datastore and deployment topology support it and the invariant needs atomicity. Put the boundary on a public method of a Spring-managed service and call it through the injected proxy. Do not rely on self-invocation, private methods, or Kotlin-final methods unless the repository's existing proxy or weaving strategy explicitly supports them; check the Kotlin Spring/all-open setup rather than assuming it.

Match transaction handling to the execution model: imperative transactions for blocking paths, the repository-supported reactive transaction operator/context for Reactor, and the repository-supported coroutine transaction context for `suspend` code. Do not block an event loop, lose coroutine cancellation, hold a database transaction across a remote call, or catch an exception that should trigger rollback. Verify propagation, isolation, timeout, and rollback behavior with the actual framework version.

### Outbound client boundaries

For every HTTP or messaging client already used by the service, configure finite connect, read/response, and overall request deadlines in the client's native configuration. At the boundary:

- Retry only transient failures and only operations that are safe to repeat, or require an idempotency key/request fingerprint and an explicit deduplication policy.
- Use bounded attempts with backoff and jitter, respect cancellation and server retry guidance, and avoid stacking independent retry loops.
- Add circuit breaking only when an existing dependency and repository convention provide it; scope it per dependency and make fallback behavior explicit. Do not add a library just to satisfy this checklist.
- Propagate tracing/correlation context without forwarding credentials, and record outcomes without logging request bodies or secrets.

Use the client and timeout semantics appropriate to the discovered MVC, WebFlux, or coroutine path; never hide a blocking client behind an unexplained scheduler.

### Operations

If the repository includes Actuator, expose only the endpoints required by its operators and protect them at the management boundary. Keep health details and environment/configuration/property data restricted, redact credentials and tokens, and never make diagnostic endpoints such as heap dumps, thread dumps, mappings, or log files public by default. Match the repository's Spring Boot version and deployment network/authentication model rather than copying a universal endpoint list.

If the runtime and deployment support graceful shutdown, stop readiness before termination, drain in-flight work, and close managed clients within the platform's termination grace period. Keep liveness about process health and readiness about whether this instance should receive traffic; do not make every optional dependency failure a liveness failure. Verify the actual load balancer/orchestrator probes and Spring Boot version before changing settings.

## Persistence

If the repository uses MongoDB, trace each repository method to its query shape and expected index. Account for document compatibility, missing fields in old documents, uniqueness races, optimistic locking, pagination, and idempotent retry behavior. Use Mongo transactions only when the deployment topology and driver support them and cross-document atomicity genuinely requires them.

If it uses another store, follow that store's existing adapter, transaction, migration, consistency, and indexing conventions instead of importing MongoDB or JPA assumptions. Keep persistence types and vendor errors at the adapter boundary.

## Testing and verification

Use the build tool and wrapper that the repository actually provides (`./gradlew`, `./mvnw`, or its documented equivalent); discover the narrowest applicable tasks instead of assuming Gradle task names. Run focused tests for changed behavior and the repository's configured quality gates.

For integration tests, use the real service when behavior depends on wire protocols, mapping, indexes, aggregation, transactions, or broker semantics. When the discovered Spring Boot version supports `@ServiceConnection` and the matching Testcontainers integration is already present, use the repository's existing service-connection pattern. Otherwise retain its established dynamic-property or environment wiring; do not add Testcontainers or another library solely to follow this guidance. Never replace persistence behavior with an in-memory fake.

Before finishing, inspect the final diff for unnecessary code, public API changes, missing tests, unbounded queries, swallowed failures, concurrency hazards, and configuration or secret leaks.
