# Global engineering rules

- Treat `omp` as the orchestrator. Delegate independent discovery, testing, and review work when that reduces wall-clock time; do not delegate trivial work.
- Use parallel agents primarily for read-only analysis. Keep one coherent writer/integrator for production changes unless files are cleanly partitioned.
- Prefer the smallest solution that satisfies the requirement. Do not introduce speculative abstractions, dependencies, frameworks, or compatibility layers.
- Keep every PR scoped to the requested task and as small as correctness permits, so reviewers can inspect it easily. Leave unrelated code identical to the target branch: no opportunistic refactors, formatting, renames, cleanup, or dependency/configuration changes. Include only implementation, tests, and documentation needed for the requested behavior; never shrink agreed acceptance criteria just to reduce the diff.
- Validate Kotlin request data at service entry points using Jakarta Bean Validation annotations on request data classes and `@Valid` on the receiving endpoint. Do not use Kotlin `require`, `check`, or `verify`-style guards for validation inside domain code or the service layer. Keep genuine domain invariants and business rules explicit; report invalid requests through the existing boundary error handling.
- Treat Clean Code, SOLID, and complexity metrics as diagnostic signals, not quotas. Repository conventions, observable contracts, and the smallest verified design win; never extract code solely because of line, argument, branch, coverage, or duplication counts.
- Read the relevant implementation, callers, configuration, and tests before editing.
- Preserve public API and persisted-data compatibility unless the request explicitly changes them.
- Report changes applied, tests added or updated, and tests not run or the actual check outcome separately. Never equate edits with verified correctness or claim unrun tests passed.
- Never expose credentials or connect to production infrastructure unless the user explicitly places it in scope.
- Use only OMP's bundled agents: `scout` for read-only code research, `librarian` for external facts and library docs, `reviewer` for correctness review, `security-reviewer` for security review, `designer` for UI/UX, `sonic` for mechanical work, and `task` for general implementation. Never invent or require custom agent names.
- Use available LSP diagnostics as non-command feedback on edited source files, subject to the execution policy below; do not start a remediation loop after a failed check.
- For Kotlin or Gradle Kotlin DSL edits, apply `kotlin-quality-gates` under the execution policy below. Never weaken tests or quality configuration, add baseline entries, or suppress rules to hide failures.
- In JavaScript and TypeScript, never use `any`, `@ts-ignore`, or unchecked casts to bypass the type system.
- Ask before commits, pushes, branch changes, merges, tags, stashes, cherry-picks, or other persistent Git operations. Never force-push, rebase, hard-reset, delete a branch with `-D`, amend, or squash commits.
- Commit messages use `<TICKET-ID> | <description>` after the user supplies and approves the ticket ID and message.
- GitHub pending PR reviews omit the `event` field. `COMMENT` submits immediately; `PENDING` is invalid.

## Communication and skill selection

- Select skills from the user's natural-language intent; do not require slash commands or exact skill names.
- Use `i-have-adhd` for this user's answer-first, attention-friendly response default. A current request for full detail or a different style wins; never shorten scope or delegate agent-owned work to satisfy presentation rules.
- Use `stop-slop` for drafting or revising prose. Choose one principal prose skill: `humanizer` for explicitly requested documentation humanization, or `simple-english` for its scoped plain-English technical prose. Do not stack full rewrites or apply prose styling to code and structured data.
- Use `session-handoff` when the user asks to save or resume working context, and `lesson-learned` when they ask to reflect on a change. Do not capture notes or memories automatically.
- The installed Ponytail plugin is the sole owner of minimalism skills. Its implementation guidance does not override requested completeness, response preferences, safety, or the execution policy below.

## Balanced overhaul control

- Apply clear, small, scoped implementation requests directly. For a broad codebase or OMP overhaul, inspect first, present a short ranked proposal, and agree on the target and boundaries before broad edits. Once that scope is confirmed, proceed without re-asking about each mechanical step.
- Keep audits and plans read-only unless implementation is requested. Do not treat a broad improvement request as permission for destructive operations, production access, Git mutations, credential changes, approval-mode changes, new plugins or package installation.
- Use `deprecation-and-migration` for replacing or retiring systems and persisted formats, `spec-to-code-compliance` for checking documented promises against code, and `omp-setup-maintenance` for setup audits and approved configuration fixes. Reuse existing architecture, simplify and review skills rather than adding another orchestrator.

## Review and execution policy

- This policy governs all skills, checklists, and subagents, including mandatory test-first or quality-gate instructions. Only a later explicit user request authorizes retries or a different workflow.
- Small, localized, low-risk changes skip test, build, lint, and format runs unless the user asks. Add or update meaningful tests when warranted, but report them as unrun unless actually executed.
- Larger or riskier changes may use at most one narrow, relevant check invocation for the entire change, shared across the main agent and subagents. Choose it from repository configuration; do not bundle checks or escalate serially to additional suites.
- Any test, build, lint, or format failure stops further validation and automatic repair, including source/test fixes and LSP-driven remediation. Report the exact command and concise actual failure, then await the user's next prompt; do not retry or substitute another check.
- Never run `ktlintFormat` or any other formatter unless explicitly requested.
- Perform one correctness self-review at the end of the change, before any optional check. Do not run per-edit architecture reviews, automatic second reviews, or replacement model-verifier loops; small changes require no reviewer-model call. A failed check is terminal for the prompt: report it without review-triggered fixes.
