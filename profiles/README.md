# Models and profiles

`profiles.yml` is the launcher's single configuration file. It is not a native
OMP overlay: use `ohMyPi`, not `omp --config profiles/profiles.yml`.

```sh
ohMyPi -model=astra -type=research
ohMyPi --model luna --type backend --cwd /path/to/service
ohMyPi -model=sol -type=frontend --inspect
```

Defaults are `luna` and `backend`. Options accept `=value` or a separate value.
Use `--` before prompt text that resembles an option.

## Models

| Alias | Provider/model | Reasoning |
| --- | --- | --- |
| `luna` | `openai-codex/gpt-6-luna` | Varies by role |
| `astra` | `openai-codex/gpt-6-astra` | Low for every role |
| `sol` | `openai-codex/gpt-6.1-sol` | Low for every role |
| `f2p` | `lm-studio/qwen3.6-uncensored` | No reasoning suffix configured |

Every configured role uses its preset's model, including `task`, `smol`, `commit`,
and `tiny`. Explicit model overrides still win. These names do not guarantee
provider access, availability, pricing, or support for a reasoning level.

## Profiles

| Type | Intended work |
| --- | --- |
| `backend` | Kotlin, Spring, Ktor, APIs, Gradle, and databases |
| `frontend` | TypeScript, React, browser behavior, and interface implementation |
| `ux` | Product design, accessibility, and design tooling |
| `pm` | Requirements, customer evidence, and economics |
| `research` | Cited research, media analysis, and authorized reverse engineering |

Each type receives `global.skills`, `global.commands`, and `global.mcpServers`,
then adds its own lists. Duplicate names are removed. Model and type are independent.
See [commands](../docs/COMMANDS.md) for workflow behavior and availability.

## Editing the catalog

- Add model selectors under `models.<alias>.modelRoles`. Keep the full role map
  so native settings cannot supply a different model for an omitted role.
- Add skill names under `global.skills` or `types.<type>.skills`.
- Add command names to the corresponding `commands` list; keep command bodies
  in `agent/commands/*.md`.
- Add MCP names only after configuring their connections privately. The public
  snapshot includes a GitNexus example and pinned GitHub/Context7 plugin metadata.
  Other selected integrations are optional and require local setup.

`--inspect` performs native discovery without model requests or MCP connections.
Read `unavailableSkillPatterns`, `unavailableCommands`, `unavailableMcpServers`,
and `warnings`; a zero exit code alone does not mean every dependency is ready.

## Boundaries

The launcher adds a temporary configuration overlay and a status label. Skills
are filtered by resolved name; file commands and MCP servers use exact names.
Built-in and extension commands remain available. Profile selection is not a sandbox.

Extra native `--config` files load before the launcher overlay. Native role flags
can explicitly override model roles. The launcher rejects options that bypass
its model/resource selection, such as `--profile`, `--provider`, and `--extension`.
Use plain `omp` when you need those native modes.

Restart after changing catalogs, adding resources, or switching projects.
