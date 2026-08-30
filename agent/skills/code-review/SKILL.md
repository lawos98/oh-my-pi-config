---
name: code-review
description: >-
  Unified code review skill for giving reviews, adversarial review personas, and
  receiving review feedback. Use when reviewing code changes, PRs, or review comments.
  Covers correctness, architecture, security, performance, maintainability, test
  coverage, hostile review mindset, and technical response to feedback.
---

# Code Review

## Giving Reviews

### Goal

Produce technical, actionable review output. Never rubber-stamp.

### Review Workflow

1. Read the original requirement.
2. Read the plan, if any.
3. Read the tests.
4. Read the implementation in full context.
5. Decide if the change is correct, safe, and maintainable.

### Review Checklist

#### Correctness

- Does it satisfy the request?
- Does it match the plan?
- Do tests pass?
- Does the build pass?
- Are edge cases handled?

#### Code Quality

- Is it readable and named well?
- Is there duplication that should be removed?
- Are functions too large or nested?
- Does it follow local idioms and patterns?

#### Architecture

- Are layers separated cleanly?
- Are dependencies minimal and justified?
- Are files in the right place?
- Does it match established project conventions?

#### Security

- Are inputs validated?
- Are secrets or PII exposed?
- Are auth/access checks correct?
- Do errors leak internals?

#### Performance

- Any N+1s or repeated work in loops?
- Are queries/indexes reasonable?
- Are resources cleaned up?
- Any unnecessary allocations or recomputation?

#### Maintainability

- Any dead code or magic values?
- Is error handling explicit?
- Is logging useful and not noisy?
- Any unsafe casts or suppressions?

#### Test Coverage

- Are changed paths tested?
- Are error paths tested, not just happy paths?
- Are tests behavior-focused?
- Do test helpers keep setups simple?

### Bug Fix Review Additions

- Does the fix address root cause?
- Is regression risk controlled?
- Is the scope minimal?
- Is there a regression test?

### Severity

- **CRITICAL**: security breach, data loss, outage
- **HIGH**: major bug, architectural violation, serious perf issue
- **MEDIUM**: maintainability issue or missing edge case
- **LOW**: minor suggestion or style preference

### Output Format

Use one of these:

```markdown
## Review Verdict: APPROVE ✓
### Summary
### Quality Assessment
### Highlights
### Minor Suggestions
```

```markdown
## Review Verdict: REQUEST_CHANGES ✗
### Summary
### Issues Found
#### Issue 1: [title] — [severity]
**Category:** ...
**Location:** `path:line`
**Problem:** ...
**Impact:** ...
**Fix:** ...
```

### Adversarial Personas

Run all three mindsets. Each must find at least one issue or at least one fragile assumption.

#### 1) Saboteur

Mindset: break it in production.

Look for:

- Unvalidated input
- State inconsistency
- Concurrency hazards
- Bad failure handling
- Bad assumptions about data size/shape/availability
- Off-by-one / null / overflow / resource leaks

Questions:

- What is the worst input?
- What if this call fails or times out?
- What if this runs twice or concurrently?
- What if neither branch is correct?

#### 2) New Hire

Mindset: understand and modify it in 6 months with no context.

Look for:

- Confusing names
- Logic spread across too many files
- Magic constants
- Multi-purpose functions
- Hidden knowledge in code
- Tests that assert internals instead of behavior

Questions:

- Can the intent be understood from the function signature and body?
- How many files are needed to trace one path?
- Where would a new contributor add a similar feature?

#### 3) Security Auditor

Mindset: an attacker will hit this code.

Look for:

- Injection
- Broken auth
- Missing access control
- Sensitive data exposure
- Insecure defaults
- Dependency risk
- Secrets in code or comments

Questions:

- What trust boundaries are crossed?
- Is input validated and output sanitized?
- Can privileges be escalated?
- Does this add attack surface?

### Adversarial Rules

- Do not say “LGTM, no issues.”
- Do not soften findings.
- Do not review only changed lines.
- Deduplicate repeated findings.
- Promote findings caught by 2+ personas one severity level.

### Review Anti-Patterns

- Vague concerns instead of concrete fixes
- Cosmetic-only findings while missing real bugs
- Approving despite major issues
- Requesting changes without saying how to fix them

## Receiving Reviews

### Goal

Verify review feedback before acting on it. Technical correctness over performative agreement.

### Response Pattern

1. Read the feedback fully.
2. Restate the requirement in your own words.
3. Verify against the codebase.
4. Evaluate whether it is correct here.
5. Respond technically.
6. Implement one item at a time and test each change.

### Rules

- Do not say “you’re absolutely right.”
- Do not say “great point.”
- Do not promise implementation before verification.
- If unclear, stop and ask for clarification.
- If wrong, push back with facts and tests.
- If correct, just fix it and state what changed.

### When Feedback Is Unclear

- Stop.
- Do not partially implement.
- Ask which items are intended before proceeding.

### When to Push Back

Push back if the suggestion:

- breaks behavior
- conflicts with existing decisions
- violates YAGNI
- is technically wrong for this stack
- cannot be verified yet

Use evidence, not defensiveness.

### Implementation Order

1. Blocking issues
2. Simple fixes
3. Complex refactors
4. Test each fix individually
5. Verify no regressions

### GitHub Replies

Reply in the inline thread, not as a top-level PR comment.

### Common Mistakes

- Performative agreement
- Blind implementation
- Batch changes without testing
- Proceeding while unclear
- Avoiding justified pushback

### Bottom Line

Review feedback is input to verify, not an order to obey.
