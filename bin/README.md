# Launcher

`ohMyPi.mjs` selects a model and role from [profiles/profiles.yml](../profiles/profiles.yml), then starts installed OMP.

```sh
bun bin/ohMyPi.mjs -model=luna -type=backend
bun bin/ohMyPi.mjs -model=luna -type=backend --inspect
```

Run these examples from the setup root. If you create an `ohMyPi` executable link on your PATH, use that name instead.

## Prerequisites

- Bun and `omp` on PATH.
- The configured model provider and its private authentication.
- Skills, plugins, and MCP integrations selected by the profile.
- A compatible OMP installation: the launcher imports source modules from the installed package.

## Behavior

The launcher combines global and role-specific skill, command, and MCP names. Command bodies live in `agent/commands/*.md`; connection definitions and credentials stay private.

Each launch uses temporary settings and a status extension. The launcher removes these temporary files on exit. Plain `omp` does not apply this launcher's role filtering.

`--inspect` reports resource discovery without connecting MCP servers or starting a model session. It does not test authentication or interactive behavior. `--cwd` selects the project; `--config` adds a settings overlay. Use `--` before a prompt that resembles an option.

## Limits

Filtering is not a security sandbox, a per-tool permission boundary, or an agent-roster filter. Built-in and extension commands remain available. Restart after adding resources or changing projects because exclusions are startup snapshots.

Explicit extension, profile, and skill overrides are rejected; use plain `omp` for those. See [the profile guide](../profiles/README.md) for selections and precedence.
