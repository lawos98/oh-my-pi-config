---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
---

# Systematic Debugging

Use this skill to move from an observed failure to a verified root-cause fix. Prefer evidence
over guesses, and keep the smallest useful change isolated from unrelated cleanup.

Apply RULES.md's execution and failure-stop policy throughout this workflow. A debugging hypothesis does not authorize repeated test/build/lint/format runs or automatic repair after a failed check.

## Core Principle

Investigate the cause before changing the code. A workaround may be necessary to contain an
active incident, but containment is not the root-cause fix; record it and continue the
investigation.

## When to Use

Use for:
- Test, build, integration, and deployment failures
- Production bugs and unexpected behavior
- Performance, concurrency, and resource problems
- Failures that appear environmental or intermittent

Do not skip the process because a fix looks obvious or the issue is under time pressure.

## The Workflow

### 1. Investigate the symptom

Before proposing a fix:

- Read the complete error, warning, and stack trace. Record the relevant file, line, error code,
  request or correlation identifier, and timestamp.
- Define the expected and actual behavior, including inputs, state, timing, and affected users.
- Treat user-reported failures and supplied output as evidence; do not rerun a check merely to confirm them. When additional observation is needed, identify the smallest permitted scenario that distinguishes the suspected causes.
- Compare the current behavior with recent code, dependency, configuration, data, and
  environment changes.
- Trace the failing value or state backward through callers, transformations, persistence, and
  external boundaries until its first incorrect origin is identified.

For a multi-component path, inspect each boundary without logging secrets or unnecessary
personal data:

- Record safe input and output shape, relevant identifiers, configuration source, and state.
- Check that the expected value or state is actually propagated to the next component.
- Run the smallest diagnostic observation that identifies the failing boundary.
- Investigate that component instead of changing every layer at once.

For a deep call stack, trace the bad value or state backward:

- Where did the bad value or state originate?
- Which caller supplied it?
- Which transformation first made it invalid?
- Which invariant should have rejected or handled it?

### 2. Form a hypothesis

State one falsifiable hypothesis in the form: “I think **X** causes **Y** because **evidence**.”
List the observation that would support it and the observation that would disprove it.

When several causes are plausible, rank them by evidence and test the least expensive
discriminating observation first. Do not present a list of untested fixes as an analysis.

### 3. Test the hypothesis

- Make the smallest experiment that distinguishes the hypothesis from its alternatives.
- Change one relevant variable at a time.
- Prefer a focused reproduction, trace, query, or diagnostic over a broad rewrite.
- Confirm that the result actually tests the hypothesis, rather than merely making the symptom
  disappear.
- If an observation disproves the hypothesis, retain the evidence and revise the explanation. If a test/build/lint/format check failed, stop under the global policy rather than starting another experiment or repair.

When a lasting regression test can protect the observable behavior, add one at a stable public boundary. Invoke test-driven-development only under that skill's explicit opt-in conditions. Otherwise follow the global execution policy; adding a regression test does not authorize a Red-Green execution loop. For environmental or unreliable reproductions, retain the diagnostic evidence and state the verification limit.

### 4. Fix and verify

- Fix the root cause at the layer that owns the invariant.
- Keep the fix focused; do not bundle speculative refactoring or unrelated improvements.
- Use existing before-change evidence and the permitted focused verification to assess the fix. Include relevant adjacent behavior in that verification only where the changed contract requires it; do not automatically launch additional checks.
- Check that the original error, failure semantics, and useful context remain visible.
- Re-check boundaries, cancellation, retries, concurrency, persistence, and compatibility when
  they are part of the failing path.

Do not claim success from a passing test that does not exercise the original behavior.

## Pattern Analysis

Before changing an unfamiliar path:

- Find a working example in the same repository or deployment.
- Compare inputs, control flow, state, configuration, dependencies, and error handling.
- Read the relevant reference or local implementation far enough to understand its contract.
- Treat every meaningful difference as a possible cause until evidence rules it out.

## Red Flags

Stop and return to investigation if you catch yourself:

- Applying a “quick fix” before reproducing or tracing the failure
- Changing several variables and being unable to say which mattered
- Assuming an input, configuration value, or timing without observing it
- Adding a fallback that hides an invalid state or swallowed exception
- Declaring the issue fixed because the symptom moved
- Repeating a failed approach without a new hypothesis
- Proposing architecture changes without evidence that the current boundary causes the failure

## When the Cause Is External or Intermittent

If investigation shows the trigger is environmental, timing-dependent, or outside the system:

1. Document the observations, scope, attempted reproductions, and remaining uncertainty.
2. Add only the handling needed by the contract, such as a bounded retry, timeout, or clear error.
3. Preserve the original cause and useful correlation context.
4. Add monitoring or a diagnostic that can distinguish recurrence from a different failure.

Do not call a cause “unknown” until the relevant boundaries and state transitions have been
observed.

## Additional Technique

Use `git bisect` only after explicit user approval because it changes the checked-out revision.
Require a known good revision and a repeatable check, preserve unrelated work, and return the
repository to its original revision when the investigation finishes.

## Stack-Specific Branches

Apply these checks only when the repository uses the corresponding stack and already supports
the relevant tooling.

### Kotlin and Spring

- Use existing Spring Boot health, metrics, logger, environment, or thread-dump diagnostics
  to capture runtime state before restarting or rolling back.
- Inspect nested configuration binding, bean wiring, profiles, and startup causes from the
  innermost exception outward.
- Name important coroutines and include safe correlation context when tracing dispatcher
  misuse, leaked work, or cancellation.
- Follow the repository's logging and tracing conventions; never log credentials, tokens, or
  sensitive payloads just to improve a diagnosis.

### MongoDB

- Inspect the exact query or aggregation, its parameters, indexes, and consistency assumptions.
- Use `explain()` or slow-query evidence to compare examined work with returned results.
- Check connection-pool waiters, held-connection duration, timeouts, and retry behavior when
  diagnosing resource exhaustion.

## Bug Record

For a lasting fix, record enough context for another engineer to reproduce and verify it:

```markdown
## Bug: <title>
**Symptom:** <observable behavior>
**Root cause:** <first incorrect state or invariant violation>
**Fix:** <focused change>
**Verification:** <reproduction, test, or smoke check>
**Remaining uncertainty:** <none, or what is still unknown>
```
