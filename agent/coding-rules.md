# Kotlin backend review rules

- Match the repository's Kotlin, Spring, testing, and architectural conventions before introducing a new pattern.
- Prefer constructor injection, explicit configuration properties, Bean Validation at boundaries, and centralized error mapping.
- Do not mix blocking Spring Data MongoDB calls with reactive or coroutine flows without an explicit boundary.
- For MongoDB changes, review query shape, indexes, uniqueness, pagination, nullability, schema evolution, optimistic concurrency, and retry/idempotency behavior.
- Do not assume MongoDB transactions are available; verify replica-set deployment and whether a transaction is actually necessary.
- Use real MongoDB integration tests through Testcontainers when persistence behavior matters. Follow the project's existing test framework.
- Reject unbounded collection reads, accidental N+1 queries, silent exception swallowing, nullable-state ambiguity, and tests that merely reproduce the implementation.
- When an authorized check uses Gradle, use `./gradlew` and discover task names from repository configuration, not exploratory task invocations.
- Follow `RULES.md` review and execution policy: skip test/build/lint/format runs for small, localized, low-risk changes; larger or riskier work allows at most one narrow relevant check invocation, not focused tests followed by `check`. Never run formatters unless explicitly requested. Perform one end-of-change correctness self-review before any optional check, not repeated architecture or model reviews. On failure, stop validation and automatic repair, report the command and actual failure, and await the next prompt. Never weaken tests or add suppressions, baseline entries, or configuration changes to hide failures. Use available LSP feedback without a post-failure remediation loop. Report changes applied, tests added/updated, and tests not run or actual check outcomes separately; edits are not verified correctness. Only a later explicit user request changes this workflow.
