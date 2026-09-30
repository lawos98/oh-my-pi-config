---
name: resolving-merge-conflicts
description: Use when resolving an in-progress Git merge or rebase conflict by recovering each side's intent and preserving compatible behavior.
---

# Resolving Merge Conflicts

1. Inspect the merge or rebase state and every unresolved conflict block.
2. Recover both intents from the conflicting changes, nearby code, commits, PRs, issues, tests, and documentation. Treat those primary sources as stronger evidence than the textual shape of the conflict.
3. Resolve each hunk deliberately. Preserve compatible intent from both sides; when intents conflict, choose the behavior that matches the operation's stated goal and report the trade-off. Do not invent unrelated behavior.
4. Remove conflict markers and self-review the complete resolved paths, including callers and tests affected by the combined behavior.
5. If the resolution is significant or risky, run at most one narrow relevant check under the global execution policy. On failure, stop and report the exact command and result.
6. Report the resolved files, decisions, and remaining Git state. Ask for explicit approval before staging, committing, continuing a rebase, merging, pushing, or performing any other persistent Git operation.

Keep the in-progress operation intact unless the user explicitly asks to abort it.