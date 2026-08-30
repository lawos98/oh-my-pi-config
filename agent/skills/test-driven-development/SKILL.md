---
name: test-driven-development
description: >-
  Enforce strict Test-Driven Development with Red-Green-Refactor cycle. Use when
  implementing new features, fixing bugs, adding business logic, or any code change
  that affects behavior. Ensures no production code is written without a failing test
  first. Triggers: tdd, test first, red green refactor, write test before code,
  test driven, failing test first.
---

# Test-Driven Development (TDD)

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

If you don't have a failing test, you cannot write production code.

## When TDD Applies (MANDATORY)

- New functions or methods
- API endpoints
- Business logic changes
- Bug fixes (reproduce the bug as a failing test FIRST)
- Behavior changes to existing code
- New domain rules or validations

## When to Skip

- Documentation changes
- Configuration updates (application.yml, properties)
- Dependency version bumps
- Formatting-only changes
- Build script changes

## The Red-Green-Refactor Cycle

### Step 1: RED — Write a Failing Test

Write ONE minimal test for the desired behavior.

**Rules:**
- Focus on BEHAVIOR, not implementation
- Mock only external dependencies (ports/adapters boundary)
- Test name describes expected behavior: `should("reject transfer for a suspended account")`
- Test MUST fail because the feature doesn't exist yet (not because of syntax errors)

```kotlin
// GOOD: Tests behavior
should("reject transfer for a suspended account") {
    val account = createAccount(status = AccountStatus.SUSPENDED)
    whenever(accountRepository.find(accountId)) doReturn account

    shouldThrow<AccountSuspendedException> {
        service.transfer(accountId, amount)
    }
}

// BAD: Tests implementation detail
should("call account status checker") {
    service.transfer(accountId, amount)
    verify(statusChecker).check(any()) // Tests HOW, not WHAT
}
```

### Step 2: VERIFY RED

Run the test. Confirm it fails for the RIGHT reason:
- ✅ Fails because method doesn't exist / throws wrong exception / returns wrong value
- ❌ Fails because of compilation error or test setup bug

If it passes → your test doesn't test what you think. Rewrite it.

### Step 3: GREEN — Write Minimal Production Code

Write the SIMPLEST code that makes the test pass.

**Rules:**
- No extras, no refactoring, no "while I'm here" improvements
- Hardcoding is acceptable at this stage
- Only address what the test requires
- Don't anticipate future tests

### Step 4: VERIFY GREEN

Run ALL tests (not just the new one). Confirm:
- New test passes
- No existing tests broken
- No compiler warnings introduced

### Step 5: REFACTOR — Improve Without Changing Behavior

Clean up code quality while keeping all tests green.

**Allowed:**
- Extract methods, rename variables
- Remove duplication
- Improve readability
- Simplify logic

**Not Allowed:**
- Adding new behavior (that needs a new test)
- Changing what the code does (only how)

Run tests after refactoring to confirm nothing broke.

### Step 6: REPEAT

Go back to Step 1 for the next behavior.

## Recovery: Code Written Before Test

**If you catch yourself writing production code without a test:**

1. STOP immediately
2. Don't revert the code (pragmatic, not dogmatic)
3. Write the test NOW
4. Verify the test actually catches regressions:
   - Comment out or break the production code
   - Confirm the test fails
   - Restore the production code
5. Note: this is recovery, not the standard workflow

## Bug Fix Protocol

For bug fixes, TDD is ESPECIALLY important:

1. **Reproduce** — Write a test that demonstrates the bug (RED)
2. **Verify** — Confirm the test fails with current code
3. **Fix** — Apply the minimal fix (GREEN)
4. **Verify** — All tests pass, including the new regression test
5. **Refactor** — Clean up if needed

This ensures the bug can never silently return.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code has the highest ROI tests. 30 seconds to write, catches regressions forever. |
| "I'll write the test after" | You won't. And if you do, you'll test the implementation, not the behavior. |
| "I know this works" | You know it works NOW. Will it work after the next refactor? After a dependency update? |
| "Tests slow me down" | Tests slow you down TODAY. They speed you up TOMORROW when you refactor with confidence. |
| "It's just a small change" | Small changes cause big bugs. The test takes 30 seconds. The debugging takes hours. |
| "I need to see the design first" | TDD IS the design process. The test tells you what the interface should look like. |
| "This is a private method" | Don't test private methods. Test the public behavior that uses them. |

## When You're Stuck

**Can't write the test?**
→ You don't understand the requirement well enough. Clarify before coding.

**Test is too complex?**
→ The design is too complex. Simplify the interface.

**Too many mocks needed?**
→ Class has too many dependencies. Decompose it.

**Test name is hard to write?**
→ Behavior is unclear. Define it before implementing.

## Verification Checklist

Before marking any implementation task complete:

- [ ] Every new behavior has a test that was written BEFORE the implementation
- [ ] Bug fixes include a regression test that reproduces the original bug
- [ ] All tests pass (full suite, not just new tests)
- [ ] Tests assert BEHAVIOR (outputs, state changes), not IMPLEMENTATION (method calls)
- [ ] Test names describe expected behavior in plain language
- [ ] No production code exists without corresponding test coverage

## Test-After vs Test-First

| Test-After | Test-First |
|------------|------------|
| Tests verify what code does | Tests define what code should do |
| Implementation drives design | Requirements drive design |
| Tests often skipped | Tests always exist |
| Hard to test = poor design | Hard to test = caught early |
| "Does it work?" | "Is it right?" |

## Red Flags — STOP and Write the Test First

- Writing any function without a test
- "Let me just get it working first"
- Implementation file open without test file
- Committing code without corresponding tests
- Tests that pass immediately (you never saw them fail)
