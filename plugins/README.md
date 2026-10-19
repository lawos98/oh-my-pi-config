# Plugins

Portable package metadata for Ponytail, GitHub, and Context7. These files do not install or authenticate plugins.

| File | Purpose |
| --- | --- |
| `package.json` and `bun.lock` | Ponytail dependency, immutable Git revision, and integrity metadata |
| `omp-plugins.lock.json` | Enabled plugins and feature settings |
| `reviewed-sources/.omp-plugin/marketplace.json` | GitHub and Context7 definitions pinned to an official marketplace commit |
| `ponytail.json` | Optional preference snapshot with default mode `off` |

Ponytail supplies minimal implementation and over-engineering review skills. GitHub supplies repository operations through MCP. Context7 supplies current library documentation through MCP.

## Setup and safety

- Use an installed OMP host and Bun. Review pins and licenses before approving installation.
- Register the reviewed catalog through OMP before installing its GitHub or Context7 entries. This export does not register it automatically.
- Keep authentication and machine-specific MCP connections outside this repository. Preserve existing native connection overrides.
- The Ponytail snapshot is not loaded automatically here. Its active preference uses `~/.config/ponytail/config.json`; `PONYTAIL_DEFAULT_MODE` can override the default.
- Default mode `off` does not remove Ponytail skills from discovery. Global safety rules still apply.
- Restart OMP after plugin changes. Enabled state does not prove that a connection works.

Installed registries, `node_modules`, and caches are intentionally absent. Source pins do not pin remote service implementations. Update a catalog SHA and its version together after review.

See [Packages and integrations](../docs/PACKAGES.md) for upstream links and optional components, and [third-party notices](../THIRD_PARTY_NOTICES.md) for licensing.
