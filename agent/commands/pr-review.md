---
name: pr-review
description: Review the current GitHub pull request and create draft line comments only after explicit approval.
---

Review the pull request for the current branch without modifying code.

1. Read the current branch and pull-request metadata with `gh pr view`. Stop if no pull request exists.
2. Read linked issue or ticket context only through repository-accessible sources. Continue without it when it is unavailable. Do not request or store credentials.
3. Read the pull-request diff and the full relevant implementation, callers, configuration, and tests.
4. Dispatch the built-in `reviewer` and `security-reviewer` in parallel. Reconcile their evidence and discard duplicates or speculative findings.
5. Report findings with severity, exact file and line, impact, and the smallest correction. Include missing acceptance criteria and unrelated scope.
6. Show the complete set of proposed GitHub comments and ask for approval before posting them.
7. After approval, create one pending GitHub review. Omit the API `event` field; `COMMENT` submits immediately and `PENDING` is invalid.
8. Never approve, request changes, submit the review, commit, push, or edit code.

This command uses the caller's existing `gh` authentication. The repository does not contain GitHub credentials.

If there are no actionable findings, report that result without creating a GitHub comment.
