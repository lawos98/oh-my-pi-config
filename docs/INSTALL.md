# Install or update

This repository does not install OMP, authenticate providers, start services,
or install plugins. Review executable skills and third-party notices before use.

## Prerequisites

- OMP and Bun on `PATH`; the launcher imports source modules from the installed OMP package.
- Provider access for the selected model, or a configured LM Studio connection for `f2p`.
- A Nerd Font for the configured terminal symbols.
- Separate setup for the plugins and optional runtimes in [PACKAGES.md](PACKAGES.md).

The source launcher documentation records OMP 18.11.3 smoke runs. Internal OMP
APIs can change; inspect the exported setup with your installed version.

## Fresh installation

Clone and review the repository first:

```sh
git clone https://github.com/lawos98/oh-my-pi-config.git
cd oh-my-pi-config
```

Review `agent/config.yml` before copying it. It enables automatic tool approval,
project memory, and passive learning. No installation-specific QA consent is included.

The following copy is for a destination that does **not** already exist. If you
already use OMP, follow the update section instead.

```sh
(
  set -eu
  test ! -e "$HOME/.omp"
  test ! -L "$HOME/.omp"
  mkdir "$HOME/.omp"
  cp -a bin profiles agent plugins docs README.md THIRD_PARTY_NOTICES.md "$HOME/.omp/"
)
```

The copied plugin locks describe the snapshot; they do not install or register
plugins. Follow the [plugin guide](../plugins/README.md), and configure provider
connections locally. Keep credentials outside the checkout.

Create a launcher link only if the target is free and `~/.local/bin` is on `PATH`:

```sh
mkdir -p "$HOME/.local/bin"
ln -s "$HOME/.omp/bin/ohMyPi.mjs" "$HOME/.local/bin/ohMyPi"
```

`ln` refuses an existing destination. Do not replace an unrelated launcher.

## Update an existing setup

1. Stop OMP. Save a private backup of the files and directories you plan to replace.
   Backups may contain credentials and session data; never commit them.
2. Compare the current configuration with this checkout. Merge `agent/config.yml`
   and rule files deliberately; do not overwrite unrelated preferences.
3. Copy `bin/` and `profiles/`, the six command files, and the reviewed skill trees.
   Copy each included skill's complete support files, not only `SKILL.md`.
4. Merge the GitNexus entry from `agent/mcp.json` into local MCP configuration.
   Do not replace private connections with the public example.
5. Review plugin changes separately. Retired packages are not uninstalled by copying
   metadata, and a lock file is not the destination's installed-plugin registry.
6. Restart OMP and inspect the chosen model/profile.

### Retired paths

After backing up and updating any shell aliases, remove these old snapshot paths
from the installed setup if they still contain the repository's retired versions:

- `profiles/f2p.yml`, `p2w.yml`, `p2w-codex.yml`, and `p2w-codex-max.yml`:
  replaced by `profiles/profiles.yml` through `ohMyPi`.
- `agent/commands/self-review.md`: replaced by `/pr-review` without an argument.
- `agent/commands/create-skill.md`: no longer selected; request skill authoring explicitly.
- `agent/behavior-control/config.json` and `plugins/quotas.json`: retired plugin preferences.
- `agent/managed-skills/service-documentation/`: moved, with all support files, to
  `agent/skills/service-documentation/`. Reconcile any local edits before removing
  the old copy; do not leave duplicate skill entrypoints.

Do not remove unrelated or locally customized files. To undo a migration, stop
OMP and restore the backed-up paths, removing newly introduced paths as needed.
Configuration rollback does not undo external actions, model calls, or plugin installs.

## Verify discovery

```sh
ohMyPi -model=astra -type=research --inspect
```

Check warnings and the unavailable-resource lists. Missing optional MCP servers
are expected until you configure them. A successful inspection does not prove
provider authentication, executable helper availability, or a live MCP connection.

## Public-copy boundaries

- Private MCP definitions and organization-specific skill instructions are not exported.
- Private server selections are removed from the public profile catalog. Optional
  public/local integrations still require connection setup on the destination.
- Existing generic public skill adaptations may differ from local company guidance.
- Auth, histories, memories, databases, browser state, generated output, installed
  dependencies, and per-machine consent are excluded.
- Native memory settings are included; existing memory contents are not.

The root `.gitignore` is an allowlist, not a secret scanner. Review every proposed
publication, including text and assets inside allowed directories.
