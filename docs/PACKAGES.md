# Packages and integrations

This export contains configuration and skills, not a complete runtime installation. Review source pins and licenses before installing anything.

## Host and plugins

| Component | Recorded source | Purpose |
| --- | --- | --- |
| [OMP](https://github.com/can1357/oh-my-pi) | Install separately | Terminal agent, tools, sessions, plugin discovery, and native subagents |
| [Ponytail](https://github.com/DietrichGebert/ponytail/tree/2ed6c52c9d7e5e56942508591085fd45dea277d3) | `4.9.0`, Git revision `2ed6c52c9d7e5e56942508591085fd45dea277d3` | Minimal implementation and over-engineering review skills |
| [GitHub MCP definition](https://github.com/anthropics/claude-plugins-official/tree/ea10b213686c90bb1984b2016937310e05336cf3/external_plugins/github) | `0.0.0+ea10b213686c` | Repository, issue, and pull-request operations |
| [Context7 MCP definition](https://github.com/anthropics/claude-plugins-official/tree/ea10b213686c90bb1984b2016937310e05336cf3/external_plugins/context7) | `0.0.0+ea10b213686c` | Current library documentation |

All three plugins are enabled in the portable lockfile. Enabled does not mean installed, authenticated, or tested.

The [reviewed catalog](../plugins/reviewed-sources/.omp-plugin/marketplace.json) pins GitHub and Context7 definitions to official marketplace commit `ea10b213686c90bb1984b2016937310e05336cf3`. It does not pin remote service implementations. Register this catalog through OMP before installing its entries.

Ponytail is the sole owner of its skills. Its [preference snapshot](../plugins/ponytail.json) sets default mode to `off`, but does not remove skills from discovery. The snapshot is not loaded automatically. See [the plugin guide](../plugins/README.md) for configuration ownership.

## Launcher and skills

| Component | Role and prerequisite |
| --- | --- |
| [Launcher](../bin/README.md) | Combines model and role selections. Requires Bun, installed OMP, and compatible OMP source modules. |
| Impeccable | Default product-interface design and accessibility guidance. |
| Taste | Explicit Taste or art-directed marketing work. Asset searches and downloads require approval. |
| Archify | Interactive architecture and workflow diagrams with editable source and a static preview. |
| HyperFrames | Explanatory video when motion helps. Requires its separate local runtime; preserve a text or static alternative. |
| Service documentation | Local-first Zensical documentation sites. Runtime dependencies are separate from skill instructions. |

Skill provenance and license files record upstream revisions and local adaptations. Keep those files with the skills. Do not automatically load both Impeccable and Taste or install optional runtimes merely because a skill is present.

## Optional integrations

These integrations are not direct dependencies in `plugins/package.json`. Configure and authorize them separately.

- **Context7:** resolve a library, then query its documentation. Queries leave the machine; exclude secrets and unnecessary proprietary text.
- **GitHub:** authentication and permissions depend on the selected transport. Publishing reviews or changing remote state requires explicit authorization.
- **GitNexus:** repository graph search and impact analysis require an index. An index can be incomplete or stale; current source remains authoritative.
- **REA:** reverse-engineering tools require a separately configured server and any required native backends. Target execution and runtime access need explicit authorization.
- **Language servers:** navigation and diagnostics require separately installed servers. Bootstrap skills do not include server binaries.
- **Image and video tools:** configure runtimes separately. Model downloads, third-party nodes, paid generation, and private uploads are not authorized by selecting a role.
- **OMP Browser Relay:** optional access to existing browser tabs. Its extension can act in logged-in sessions; tab selection is not a permission sandbox. Keep its control endpoint on loopback and do not forward it. Consequential actions need explicit instructions.

## Portable setup boundary

Keep the manifest, lockfiles, reviewed catalog, and optional preference snapshot. Do not copy `installed_plugins.json`, caches, `node_modules`, authentication, or private MCP definitions from another machine.

Preserve the destination machine's native connection overrides. Update source pins only after review, then restart OMP. Neither this export nor launcher inspection proves authentication, rendering, or interactive behavior.

See [third-party notices](../THIRD_PARTY_NOTICES.md) for licensing and [OMP plugin documentation](https://github.com/can1357/oh-my-pi/blob/main/docs/plugin-manager-installer-plumbing.md) for host behavior.
