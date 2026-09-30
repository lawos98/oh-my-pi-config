---
name: test-driven-development
description: Use only when the user explicitly requests TDD/test-first development or the repository explicitly requires it. Run behavior-focused Red-Green-Refactor at an agreed public seam under OMP's execution policy.
---

# Test-Driven Development

TDD is opt-in. A request for tests, coverage, or a bug fix is not by itself a request for strict test-first development.

When the user explicitly requests TDD, that request authorizes repeated execution of the one narrow test target needed for the Red-Green-Refactor loop. It does not authorize project-wide suites, lint, builds, formatters, or unrelated checks. OMP's global execution policy remains authoritative for every other command.

## Choose the seam

Identify the highest stable public interface that exposes the required behavior. Agree on the seam when the choice materially changes test cost or design. Tests observe outputs, state transitions, durable side effects, or public errors; they do not assert private methods, internal calls, field copying, or mock echoes.

## Cycle

1. **Red:** write one minimal test for one observable behavior.
2. Run the narrow test and confirm it fails because the behavior is absent or wrong.
3. **Green:** implement only enough behavior to pass that test.
4. Run the same narrow test and confirm it passes.
5. **Refactor:** simplify without changing behavior when the improvement is supported by the current evidence.
6. Repeat for the next distinct behavior.

An expected Red failure is evidence for the TDD cycle. Any unrelated compilation, setup, infrastructure, or test failure is not expected Red: stop, report the exact command and failure, and await direction under the global policy.

## Test quality

A permanent test must fail for a plausible regression in observable behavior. Keep it deterministic, isolated, and full-suite-safe. Prefer worked examples and domain invariants over implementation-derived expected values.

Do not keep tests that assert source text, incidental defaults, plumbing, bare non-throwing behavior, or interactions with internal collaborators. Use a throwaway smoke harness instead when the behavior has no stable seam worth maintaining.

## Bug fixes

Use the smallest reproduction that exercises the user's reported symptom at the real seam. Preserve it as a regression test only when it protects a plausible recurrence without coupling to internals.

## Completion

Report the Red and Green commands and outcomes actually observed. Final verification beyond the focused TDD loop follows the global execution policy and requires separate authorization when that policy calls for it.
