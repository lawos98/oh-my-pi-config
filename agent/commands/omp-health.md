---
name: omp-health
description: Audit the active OMP configuration, plugins, skills, commands, MCP definitions, and stale cross-harness references without changing them.
---

Perform a concise, read-only OMP setup audit.

- Read `~/.omp/agent/config.yml`, `mcp.json`, `RULES.md`, skill metadata, commands, and plugin state.
- Run `omp plugin list` and verify configured local executables exist.
- Flag invalid JSON/YAML, duplicate skill names, missing referenced skills, unavailable agent names, stale cross-harness references, and unnecessary plugins or MCP servers.
- Do not read credential values, histories, logs, or session databases.
- Return at most five ranked findings. Make no configuration changes unless separately requested.
