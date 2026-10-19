---
name: testing
description: Generate, execute, and analyze tests for codebases, covering unit, integration, and end-to-end testing with coverage reporting. Use when the user requests testing or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills contributors
  version: 1.0.0
---

# Testing

This skill enables an AI agent to systematically generate, run, and evaluate tests for a given codebase. It covers the full testing lifecycle — from analyzing source code and identifying meaningful test cases, through writing and executing tests, to measuring coverage and recommending improvements. The agent supports unit tests, integration tests, and end-to-end tests across multiple languages and frameworks.

## Workflow

1. Identify the requested behavior and relevant public boundary. Read its implementation, callers, and existing tests; expand dependency analysis only where needed to understand observable effects.

2. Select cases that protect plausible regressions: normal behavior, meaningful boundaries, errors, and state transitions. Do not enumerate every helper or pursue coverage percentages unless requested.

3. Write deterministic, isolated tests using the repository's framework and conventions. Assert observable results, not private wiring, copied values, or mock echoes.

4. Follow RULES.md's review and execution policy. When a check is warranted and permitted, select one narrow repository-configured invocation covering the change. Do not automatically run a suite and then rerun it for coverage.

5. Use existing coverage evidence when relevant. If coverage measurement is explicitly requested, account for it in the permitted invocation rather than adding an automatic second run. A failure stops validation and automatic repair under the global policy.

6. Report tests added or updated, the exact check and result if run, and remaining gaps. Do not introduce production refactoring, CI changes, or broader testing work without task scope.

## Supported Languages

The runner commands below and in the examples are illustrative, not commands to run automatically. Select actual invocations from repository configuration under the workflow above.

| Language   | Framework       | Runner Command                  |
|------------|-----------------|---------------------------------|
| Python     | pytest          | `pytest --cov=src -v`           |
| JavaScript | Jest            | `npx jest --coverage --verbose` |
| TypeScript | Jest / Vitest   | `npx vitest run --coverage`     |
| Java       | JUnit 5         | `mvn test`                      |
| Go         | testing (stdlib) | `go test -cover ./...`         |
| Rust       | cargo test      | `cargo test`                    |

## Usage

Provide one or more of the following inputs:

- **Source file or directory** to generate tests for (e.g., `src/utils/parser.py`).
- **Existing test file** if you want the agent to extend or improve current tests.
- **Test framework preference** if the project does not already have one configured.
- **Coverage threshold** if you want the agent to target a specific percentage (e.g., 90%).

## Examples

Read the relevant [pytest or Jest example](examples.md) only when a concrete test pattern is needed and the repository's existing tests do not provide one. Otherwise use the workflow and conventions above without loading the examples.

## Best Practices

- **Name tests after the scenario, not the implementation.** Use names like `test_empty_cart_total_is_zero` rather than `test_total_method`. This makes failures self-documenting.
- **Keep tests independent.** Each test should set up its own state via fixtures or setup methods. Never rely on test execution order.
- **Prefer parameterized tests for input variations.** When the same logic applies to many inputs, use `@pytest.mark.parametrize` or `test.each` instead of duplicating test bodies.
- **Mock external dependencies, not internal logic.** Stub network calls, databases, and file I/O. Avoid mocking the code under test itself — that defeats the purpose.
- **Target meaningful coverage, not 100%.** Aim for thorough branch coverage of critical paths. Trivial getters and framework-generated code rarely need dedicated tests.
- Preserve existing CI behavior. Propose CI changes only when requested or required by the task.

## Edge Cases

- **Dynamically generated code:** If the codebase uses metaprogramming, decorators, or code generation, the agent may not detect all callable paths. Provide hints about generated interfaces.
- **Global state and singletons:** Tests for code that mutates global state require careful teardown. The agent will flag these but may need guidance on acceptable reset strategies.
- **Async and concurrent code:** Testing async functions requires framework-specific patterns (`pytest-asyncio`, Jest's async handling). The agent will use the appropriate pattern but may ask for confirmation on timeout thresholds.
- **Environment-dependent tests:** Tests that depend on environment variables, file system layout, or network access should be clearly marked as integration tests and excluded from fast unit-test runs.
- **Flaky tests:** If test runs produce intermittent failures, the agent will flag non-deterministic patterns (e.g., reliance on wall-clock time, unordered collection comparisons) and suggest fixes.
