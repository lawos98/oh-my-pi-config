# Global engineering rules

- Treat `omp` as the orchestrator. Delegate independent discovery, testing, and review work when that reduces wall-clock time; do not delegate trivial work.
- Use parallel agents primarily for read-only analysis. Keep one coherent writer/integrator for production changes unless files are cleanly partitioned.
- Prefer the smallest solution that satisfies the requirement. Do not introduce speculative abstractions, dependencies, frameworks, or compatibility layers.
- Treat Clean Code, SOLID, and complexity metrics as diagnostic signals, not quotas. Repository conventions, observable contracts, and the smallest verified design win; never extract code solely because of line, argument, branch, coverage, or duplication counts.
- Read the relevant implementation, callers, configuration, and tests before editing.
- Preserve public API and persisted-data compatibility unless the request explicitly changes them.
- Never claim completion without running the narrowest meaningful verification and reporting the actual result.
- Never expose credentials or connect to production infrastructure unless the user explicitly places it in scope.
- Use only OMP's bundled agents: `scout` for read-only code research, `librarian` for external facts and library docs, `reviewer` for correctness review, `security-reviewer` for security review, `designer` for UI/UX, `sonic` for mechanical work, and `task` for general implementation. Never invent or require custom agent names.
- Run LSP diagnostics on every edited source file and the narrowest applicable project checks before completion.
- For every Kotlin or Gradle Kotlin DSL edit, apply `kotlin-quality-gates` and run the repository's existing narrowest ktlint and detekt checks. Fix source findings; never weaken configuration, add baseline entries, or suppress rules merely to pass.
- In JavaScript and TypeScript, never use `any`, `@ts-ignore`, or unchecked casts to bypass the type system.
- Ask before commits, pushes, branch changes, merges, tags, stashes, cherry-picks, or other persistent Git operations. Never force-push, rebase, hard-reset, delete a branch with `-D`, amend, or squash commits.
- Commit messages use `<TICKET-ID> | <description>` after the user supplies and approves the ticket ID and message.
- GitHub pending PR reviews omit the `event` field. `COMMENT` submits immediately; `PENDING` is invalid.
