---
name: pr-comments
description: Triage every GitHub PR comment into PR_COMMENTS.md with verdicts and paste-ready replies, then apply accepted fixes as uncommitted changes.
---

Triage all comments on a GitHub pull request, write a decision document to `PR_COMMENTS.md` at the repository root, then apply accepted fixes to the working tree. GitHub is read-only for the whole run: never post a reply, never resolve a thread, never approve, never commit, never push.

Target: `$ARGUMENTS` — optional PR number or URL. With no argument, use the PR for the current branch (`gh pr view`). With an argument, resolve it with `gh pr view <arg> --json headRefName`; if `headRefName` differs from `git branch --show-current`, STOP and tell the user to `gh pr checkout <arg>` first. Never auto-checkout.

## Skills and subagents (load before triage)

- `code-review` skill, "Receiving Reviews": verify before acting, when to push back, reply in the inline thread, no performative agreement ("great point", "you're absolutely right"), no promising implementation before verification.
- `code-research` skill: trace callers, configuration, and tests outside the diff before judging a comment.
- `humanizer` skill: final prose pass only (see Finalization). This command is the explicit invocation gate.
- Built-in `reviewer` subagent: independent second pass over substantive comments. Reconcile with your own verdicts; evidence wins.

## Preconditions

Trust the user's environment: the repository, `gh` auth, checked-out branch, and working-tree state are set up exactly as the user wants. Do not block on `git status` and do not ask to commit or stash. Resolve the target PR as described above and proceed.

## Collect

Fetch all three sources; keep GitHub comment database IDs as stable references:

1. Review threads (GraphQL — `gh pr view --json` does not expose `reviewThreads`):

   ```
   gh api graphql -f owner=<owner> -f name=<repo> -f number=<n> -f query='
   query($owner:String!,$name:String!,$number:Int!){
     repository(owner:$owner,name:$name){ pullRequest(number:$number){
       title url headRefName baseRefName isDraft
       reviewThreads(first:100){ nodes { isResolved isOutdated path line originalLine
         comments(first:50){ nodes { databaseId url body createdAt author { __typename login } } } } } } } }'
   ```

2. Unthreaded review comments: `gh api repos/{owner}/{repo}/pulls/{n}/comments`; drop IDs already inside threads; treat each remaining comment as a one-comment thread.
3. Conversation comments: `gh pr view <n> --json comments,reviews`.

Bot classification: author `__typename` is `Bot`, or login ends in `[bot]`. Everything else is human.

## Judge

For every thread, before giving a verdict:

- Read the commented file at that line, the surrounding implementation, callers, and tests (`code-research`). Never judge from the diff alone.
- A comment claiming library or framework behavior: verify against `context7` docs. A comment that could conflict with repository standards or ADRs: verify against the checked-in project documentation and linked public primary sources. Do not require private documentation services.
- Bot comments: defect or vulnerability claims with severity high or above (Sonar bug/vulnerability, Snyk high, similar) get the full pass. Style, coverage-threshold, and status bot noise is `SKIPPED` with a one-line note; never verified.
- Threads already resolved on GitHub: verdict N/A, status `SKIPPED`, listed last.

Verdicts: `VALID` (fix it), `PARTIALLY VALID` (concern is real; the proposed fix is wrong or oversized), `INVALID` (reviewer misread the code, or a style preference conflicts with project convention), `N/A` (bots-noise, resolved, outdated).

## Write PR_COMMENTS.md (repo root)

Always overwrite any existing file. Scratch document: never `git add` it; never edit `.gitignore` or git config — the user manages the ignore entry themselves (IntelliJ global gitignore).

Format for a Markdown reader (IntelliJ preview), not plain text:

- Title block: PR title linked to the PR, `head → base` branches, a one-line fetch summary, then a summary table — one row per entry: entry number linking to the entry's anchor, status badge, verdict badge, `File.kt:line`, author. Give each entry a small HTML anchor (e.g. `<a id="c1"></a>` above its header) so the table links work in preview.
- Badges for every status and verdict: `<span style="color:#2da44e;font-weight:bold">APPLIED</span>` with 🟢, `<span style="color:#bf8700;font-weight:bold">DEFERRED</span>` with 🟡, `<span style="color:#cf222e;font-weight:bold">DECLINED</span>` with 🔴, `<span style="color:#6e7781;font-weight:bold">SKIPPED</span>` with ⚪; verdicts ✅ <span style="color:#2da44e">VALID</span>, 🟠 <span style="color:#bf8700">PARTIALLY VALID</span>, ❌ <span style="color:#cf222e">INVALID</span>, ⚪ N/A. Keep the plain uppercase word inside every span — color never carries meaning alone.
- Order: VALID, then PARTIALLY VALID, then INVALID, then bots and resolved. Each entry:
  - Header: `## #<n> · <status badge> · \`<File.kt>:<line>\` · @<author>`. Full relative file path plus the GitHub comment URL on the next line.
  - **Original comment** — the reviewer's exact comment body, verbatim, in a fenced code block (choose a fence longer than any backtick run in the body). Never trim, rephrase, or translate it.
  - **Summary** — what the reviewer actually asks for, one or two sentences.
  - **Verdict** — colored verdict badge plus a one-line reason.
  - **What we do** — intended action.
  - **Change** (APPLIED only) — the real edit as a fenced `diff` block taken from the actual `git diff` hunks, followed by the final `file:line` locations.
  - **Recommended reply** — English, paste-ready, addressed to the inline thread, not top-level; put it in a fenced `markdown` code block so copying yields exactly the reply. State what changed and the evidence; no flattery, no promises before verification.
- Bot and resolved entries keep the same structure but wrapped in a collapsed `<details>` block whose summary is the entry header.
- Footer: the suite result — colored 🟢/🔴 badge, the exact command run, caveats as bullets.

Statuses maintained during the run: `APPLIED` (record the actual file:line changed), `DEFERRED` (contested design; list 2–3 concrete options with trade-offs as bullets), `DECLINED` (with the reason), `SKIPPED`.

## Apply

No go/no-go checkpoint; apply directly after writing the initial file.

- `VALID`: always apply the smallest correct fix.
- **Same-pattern sweep**: when a `VALID` comment is a mechanical convention fix (string literal → named constant such as `"Content-Type"` → `HttpHeaders.CONTENT_TYPE`, fully-qualified class name → import, similar), fix the cited line AND search the whole codebase for the identical pattern — grep the exact literal/FQN/API call, or use LSP references — and apply the same fix at every matching site. Skip look-alikes with different semantics (e.g. a literal that is deliberately asserted against the raw wire value, generated code). List every swept location in the entry's **Change** section and state the sweep in the Recommended reply so the reviewer sees the pattern is covered repo-wide, not just at the commented line.
- `PARTIALLY VALID`: apply only when the corrected fix is the obvious small one (single file, no public API change, no new behavior). Otherwise mark `DEFERRED` with 2–3 design options and move on — contested items never block other work.
- `INVALID`: no edit; entry becomes `DECLINED` with the evidence from the judging pass.
- Tests: fix existing tests that asserted the old behavior the reviewer rejected. Add a new test only when the reviewer asked for one, or an applied behavior fix has no coverage. Never add tests for style-only edits; never edit a test to make it green.
- After each edit, run LSP diagnostics on the touched files and resolve reported errors before the next comment.

## Verify (one suite, stop on red)

After all edits, run once the narrowest test suite covering the touched modules (discover it from the repository build config). Any failure: stop immediately. Report the exact failing tests, leave every change in the tree, and do not auto-repair, revert, or edit tests. Record the suite result in the document footer per the format rules above.

## Finalize

1. Rewrite every Recommended reply so it matches what actually happened (or why the item was declined). Each reply must be paste-ready as-is.
2. One `humanizer` pass over the whole `PR_COMMENTS.md`. Never alter: code identifiers, file paths, line numbers, commands, URLs, GitHub comment IDs, status labels, verdict words, numbers, HTML color spans, emoji badges, anchors, table structure, and code fences.
3. If `DEFERRED` entries exist, present them all as one batched question set with the recorded options. When the user answers in the same session, implement the chosen option under the same rules, then repeat LSP checks and the suite run.
4. Final report: counts per status, `git diff --stat`, suite outcome, and a reminder that changes are uncommitted — `git diff` shows exactly what changed and `git checkout .` reverts exactly that.

## Never

Post or reply on GitHub, resolve threads, approve, commit, push, create branches, touch `.gitignore` or git config, or weaken tests or quality settings to get green.
