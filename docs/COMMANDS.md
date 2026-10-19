# Commands

Files in `agent/commands/` become named OMP prompt workflows. The profile YAML
selects which commands are available; the Markdown files hold their full instructions.

| Command | Available in | Purpose |
| --- | --- | --- |
| `/pr-review [PR]` | All profiles | Review local changes in chat, or a named PR in `PR_REVIEW.md`; no source edits or publication |
| `/learn [focus]` | All profiles | Summarize verified lessons, then ask before saving them |
| `/developer-docs [create\|update\|audit] [scope]` | All profiles | Maintain repository-based developer docs; audit mode is read-only |
| `/arena <command> <prompt>` | All profiles | Compare approaches, then run the selected available workflow once |
| `/pr-comments [PR]` | Backend, frontend | Triage all PR comments and apply supported fixes locally; GitHub remains read-only |
| `/simplify-code` | Backend, frontend | Remove unnecessary complexity without changing behavior |

Examples:

```text
/pr-review
/developer-docs audit API contracts and local setup
/arena developer-docs explain the request flow for new contributors
```

These are instructions to an agent, not deterministic programs or security
boundaries. Git writes, installation, publication, and external actions retain
their normal approval requirements.

`/self-review` is replaced by `/pr-review` without arguments. `/create-skill` is
not part of this snapshot; use the skill-authoring workflow explicitly. Built-in
OMP and plugin commands have separate owners.

Keep human documentation outside `agent/commands/` so it cannot become an extra
file-backed command. Restart the launcher after adding or changing commands.
