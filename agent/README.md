# Agent configuration

OMP reads these files from `~/.omp/agent`. The launcher adds a temporary overlay;
it does not replace provider authentication or the global configuration.

| File | What it controls |
| --- | --- |
| `config.yml` | Models for plain `omp`, task concurrency, memory, UI, and tool approval |
| `RULES.md` | Engineering decisions, user questions, Git approvals, and verification limits |
| `coding-rules.md` | Kotlin, Spring, MongoDB, and Gradle review guidance |
| `response-rules-reminder.md` | Concise reporting and one decision at a time through native `ask` |
| `mcp.json` | Public GitNexus-only example; merge it with private connections locally |
| [commands](../docs/COMMANDS.md) | Named prompt workflows |
| [skills](skills/README.md) | Curated task guidance |
| [managed-skills](managed-skills/README.md) | Reviewed generated guidance |

## Settings to review first

- **Tool approval:** `yolo` approves tool calls without an interactive prompt.
- **Delegation:** up to four subagents; task isolation is disabled, so edits can share a working tree.
- **Memory:** per-project Mnemopi recall and retention are enabled. Launch from the intended repository.
- **Learning:** passive learning is enabled, but `autolearn.autoContinue` is false.
- **Models:** plain `omp` uses the base Luna mapping. `ohMyPi` supplies the selected
  preset's complete mapping instead. Provider access is not included.

Do not copy this directory wholesale from a live installation. Auth, databases,
sessions, memories, and caches are private runtime state. Installation-specific
QA consent is deliberately absent from this public configuration.

Restart OMP after changing configuration or instruction files.
