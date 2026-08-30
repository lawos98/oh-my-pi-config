---
name: quick-pr-creator
description: Streamlined GitHub PR creation workflow. Use when creating pull requests, preparing branches for review, writing PR descriptions, or pushing feature branches. Handles branch naming, commit organization, PR template filling, and reviewer assignment. Triggers - create PR, pull request, push branch, prepare for review, open PR, submit for review, ready for merge.
---

# Quick PR Creator

Streamlined workflow for creating well-structured GitHub Pull Requests.

## Pre-Flight Checks (MANDATORY)

Before creating any PR:
1. Confirm current branch is NOT main/master
2. Run `git status` — no uncommitted changes
3. Run `git log main..HEAD --oneline` — verify commit history
4. Run tests: `./gradlew test` or project-specific test command
5. Run `lsp_diagnostics` on changed files — no errors

## Branch Naming Convention

Format: `{type}/{ticket-id}-{short-description}`

Types: `feat/`, `fix/`, `refactor/`, `docs/`, `chore/`, `test/`

Examples:
- `feat/PROJ-123-add-session-persistence`
- `fix/PROJ-456-null-pointer-in-health-check`

## PR Creation Workflow

### Step 1: Gather Context
```bash
git diff main..HEAD --stat          # Files changed
git log main..HEAD --oneline        # Commits
git diff main..HEAD --shortstat     # Lines added/removed
```

### Step 2: Draft PR Description

Structure:
```markdown
## Summary
[1-3 bullet points describing WHAT changed and WHY]

## Changes
- [File/module]: [What was done]
- [File/module]: [What was done]

## Testing
- [ ] Unit tests pass
- [ ] Manual verification: [describe what you tested]
- [ ] No regressions in existing functionality

## Notes for Reviewer
[Any context that helps review: tradeoffs, alternatives considered, areas of concern]
```

### Step 3: Push & Create
```bash
git push -u origin HEAD
gh pr create --title "{type}: {description}" --body "..."
```

## Rules
- ALWAYS ask user for approval before `git push` and `gh pr create`
- ALWAYS show draft PR title + body for user review first
- NEVER force-push
- NEVER create PR to main without user confirmation
- Include ticket ID in PR title if available
- Request reviewers only if user specifies them
