# Kotlin backend review rules

- Match the repository's Kotlin, Spring, testing, and architectural conventions before introducing a new pattern.
- Prefer constructor injection, explicit configuration properties, Bean Validation at boundaries, and centralized error mapping.
- Do not mix blocking Spring Data MongoDB calls with reactive or coroutine flows without an explicit boundary.
- For MongoDB changes, review query shape, indexes, uniqueness, pagination, nullability, schema evolution, optimistic concurrency, and retry/idempotency behavior.
- Do not assume MongoDB transactions are available; verify replica-set deployment and whether a transaction is actually necessary.
- Use real MongoDB integration tests through Testcontainers when persistence behavior matters. Follow the project's existing test framework.
- Reject unbounded collection reads, accidental N+1 queries, silent exception swallowing, nullable-state ambiguity, and tests that merely reproduce the implementation.
- Run Gradle through `./gradlew`. Discover available tasks before assuming detekt, ktlint, Kover, integration-test, or mutation-test tasks exist.
- After editing, run focused tests first, then the applicable `check` or equivalent quality gate.
