# Commands quick reference

Run these inside an OMP conversation opened from the repository you want to work on.
The six custom workflows below are defined in `agent/commands/`. They are agent
instructions, not shell commands or permission sandboxes.

| Command | What it does | Example | Profiles |
| --- | --- | --- | --- |
| [pr-review](../agent/commands/pr-review.md) | Reviews local changes in chat; an explicit PR writes `PR_REVIEW.md`. Does not edit source or publish. | `/pr-review` or `/pr-review 42` | All |
| [learn](../agent/commands/learn.md) | Extracts verified lessons from this conversation; asks before saving memory or a reusable skill. | `/learn request validation` | All |
| [developer-docs](../agent/commands/developer-docs.md) | Creates or updates source-backed docs. `audit` reports gaps without edits. | `/developer-docs audit API contracts` | All |
| [arena](../agent/commands/arena.md) | Compares approaches, then follows the chosen available command's workflow once. | `/arena developer-docs explain the request flow` | All |
| [pr-comments](../agent/commands/pr-comments.md) | Reads all PR comments, writes `PR_COMMENTS.md`, and applies supported fixes locally. Does not reply on GitHub. | `/pr-comments 42` | Backend, frontend |
| [simplify-code](../agent/commands/simplify-code.md) | Removes unnecessary complexity while preserving behavior. State the target in the conversation first. | `/simplify-code` | Backend, frontend |

## Arguments and limits

- `/pr-review`: omit the argument for local review, or supply a positive PR number
  or GitHub PR URL. Free-text review topics are not valid arguments.
- `/pr-comments`: accepts a PR number or URL; without one, it uses the current
  branch's PR. The checkout must match the target PR.
- `/developer-docs [create|update|audit] [scope]`: no mode updates existing docs
  and creates missing coverage. Installation and publication need separate approval.
- `/arena <command> <prompt>`: the target must be available in the current profile.
  It does not wrap shell commands or arbitrary built-in UI actions. It uses extra model work.
- `/learn`: does not automatically select newly created skills in launcher profiles.
- `/simplify-code`: makes local edits; it does not commit, push, or switch branches.

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
