# Oh My Pi configuration

A portable copy of my OMP setup: a model/profile launcher, engineering rules,
commands, skills, and pinned plugin metadata. This is configuration, not an OMP fork.

```sh
ohMyPi -model=astra -type=research
```

Models: `luna`, `astra`, `sol`, `f2p`. Profiles: `backend`, `frontend`, `ux`, `pm`,
`research`. Each model preset keeps all configured roles on that model, including
lightweight subagents. Explicit model overrides still take precedence.

## Start here

1. Read the safety notes below.
2. Follow [installation and migration](docs/INSTALL.md).
3. Choose a [model and profile](profiles/README.md).

Find available workflows in the [quick reference](docs/README.md):
[commands](docs/COMMANDS.md), [skills](docs/SKILLS.md), and
[extensions and integrations](docs/EXTENSIONS.md).

## What lives where

| Component | Purpose |
| --- | --- |
| [bin](bin/README.md) | The `ohMyPi` launcher and its prerequisites |
| [profiles](profiles/README.md) | Model choices and per-profile skill, command, and MCP allowlists |
| [agent](agent/README.md) | Native settings and shared engineering rules |
| [commands](docs/COMMANDS.md) | Six named workflows such as PR review and developer documentation |
| [skills](agent/skills/README.md) | Task-specific guidance and supporting references |
| [plugins](plugins/README.md) | Plugin versions, source pins, and preference files |
| [packages](docs/PACKAGES.md) | Optional runtimes and external integrations |
| [third-party notices](THIRD_PARTY_NOTICES.md) | Sources, licenses, and redistribution limits |

## Safety and privacy

- `agent/config.yml` uses `tools.approvalMode: yolo`. Tool calls do not require
  interactive approval. Review this setting before installation.
- Project-scoped Mnemopi recall and retention are enabled. Passive learning is
  enabled; extra post-stop capture turns are disabled. Recalled text can enter
  a cloud model's context. Local storage does not mean offline processing.
- Profiles filter available resources. They are not permission sandboxes.
- Provider authentication, private MCP connections, local models, and executable
  dependencies need separate setup. Selecting a resource does not install it.
- This repository excludes credentials, histories, memories, databases, caches,
  browser profiles, machine-specific endpoints, and automatic QA consent.
  Never publish a complete `~/.omp` directory.

The public copy preserves portable behavior, not private workstation integrations.
See [installation](docs/INSTALL.md#public-copy-boundaries) for the differences.

## Updating this snapshot

Copy only reviewed configuration and complete portable skill support trees.
Keep the profile catalog and component guides in sync. Review licenses and scan
for private data before publishing; `.gitignore` cannot remove already tracked files.
