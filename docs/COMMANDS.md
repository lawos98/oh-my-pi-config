# Commands quick reference

Run these inside an OMP conversation opened from the repository you want to work on.
The seven custom workflows below are defined in `agent/commands/`. They are agent
instructions, not shell commands or permission sandboxes.

| Command | What it does | Example | Profiles |
| --- | --- | --- | --- |
| [pr-review](../agent/commands/pr-review.md) | Reviews local changes or a specified PR and writes `PR_REVIEW.md` in both modes. Does not edit source or publish. | `/pr-review` or `/pr-review 42` | All |
| [learn](../agent/commands/learn.md) | Extracts verified lessons from this conversation; asks before saving memory or a reusable skill. | `/learn request validation` | All |
| [developer-docs](../agent/commands/developer-docs.md) | Creates, updates, regenerates or improves source-backed docs and their visuals. `audit` reports gaps without edits. | `/developer-docs regenerate onboarding journeys` | All |
| [arena](../agent/commands/arena.md) | Compares approaches, then follows the chosen available command's workflow once. | `/arena developer-docs explain the request flow` | All |
| [pr-comments](../agent/commands/pr-comments.md) | Reads all PR comments, writes `PR_COMMENTS.md`, and applies supported fixes locally. Does not reply on GitHub. | `/pr-comments 42` | Backend, frontend |
| [simplify-code](../agent/commands/simplify-code.md) | Removes unnecessary complexity while preserving behavior. State the target in the conversation first. | `/simplify-code` | Backend, frontend |
| [task-context](../agent/commands/task-context.md) | Saves requirements, decisions, acknowledged trade-offs, evidence, full links, paths and pending work in `<TICKET>-CONTEXT.md` at the repository root. | `/task-context` or `/task-context PROJ-123 focus on the pending API design` | All |

## Arguments and limits

- `/pr-review`: omit the argument for local review, or supply a positive PR number
  or GitHub PR URL. Free-text review topics are not valid arguments.
- `/pr-comments`: accepts a PR number or URL; without one, it uses the current
  branch's PR. The checkout must match the target PR.
- `/developer-docs [create|update|regenerate|improve|audit] [scope]`: no mode updates
  existing docs and creates missing coverage. `regenerate` re-inspects the requested
  source scope and refreshes docs in place; `improve` strengthens existing content
  and navigation. Both preserve manual notes, historical decisions and useful URLs.
  Source-to-section evidence guides synchronization of related pages and visuals;
  this is invoked maintenance, not a watcher. Installation and publication need
  separate approval. For example, `/developer-docs improve background-work explanations`.
  HTML sites and rendered ADRs follow the command's
  [HTML-site diagram contract](../agent/commands/developer-docs.md#html-site-diagram-contract):
  one full-width, content-height iframe per interactive diagram, with outer-page
  scrolling and searchable adjacent explanation/evidence. Keep editable sources
  and generated static assets for offline/export delivery, not duplicate page visuals.
  ADR requests also follow the shared [ADR authoring style](ADR-AUTHORING.md): full
  tabbed options with implementation steps, relevant examples and Positive/Negative
  callouts, not comparison tables alone. The global rule applies this ADR default
  across direct skill use and ordinary conversations as well as this command;
  accepted decisions stay accepted and team proposals stay unselected.
- `/arena <command> <prompt>`: the target must be available in the current profile.
  It does not wrap shell commands or arbitrary built-in UI actions. It uses extra model work.
- `/learn`: does not automatically select newly created skills in launcher profiles.
- `/simplify-code`: makes local edits; it does not commit, push, or switch branches.
- `/task-context [JIRA-TICKET] [additional task context]`: an explicit ticket overrides
  a ticket detected in the current branch. Missing or ambiguous tickets require a
  decision; directory names are not used as ticket evidence. Refreshes an existing
  note for the same task while preserving useful manual notes and decision history.
  Captures actual verification results without rerunning checks. In a new session,
  attach the generated file or ask the LLM to read its absolute path and verify it
  against the current checkout before continuing. Saving context does not authorize
  pending edits, Git mutations, production access or retries of failed checks.

GitHub PR modes require authenticated GitHub access. Local `/pr-review` does not.
Use trusted repositories; project instructions and remote comments can affect context.

## Other command owners

Ponytail commands belong to its plugin; see [extensions](EXTENSIONS.md).
Skills are selected through natural language or supported native skill invocation;
see [the skill catalog](SKILLS.md). Native OMP commands are version-dependent and
are not redefined by this setup. Use the running session's command completion for
its full list. This page is the complete custom file-command list, not all host commands.

`/self-review` is replaced by `/pr-review` without arguments. `/create-skill` is
retired; request skill authoring explicitly. Restart the launcher after command changes.
