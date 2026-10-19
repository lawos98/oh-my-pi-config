# Extensions and integrations

A quick guide to what this export selects and how to ask for it. This is not an exhaustive OMP tool API reference.

**Configured does not mean installed, connected, authenticated, or tested.** Role selection does not grant access or authorize writes, spending, or installation. See [Packages and integrations](PACKAGES.md) for setup, source pins, versions, and licenses.

## Configured plugins

These are all three entries in the [plugin registry](../plugins/omp-plugins.lock.json). Only Ponytail is a direct dependency in [package.json](../plugins/package.json).

- **Ponytail (`@dietrichgebert/ponytail`)** — Minimal implementation and over-engineering review guidance. Ask: “Implement this with existing libraries” or “Review this diff for needless complexity.” Requires the installed package and visible skills. The portable preference snapshot sets default mode to off but is not loaded automatically. Mode off does not remove skills or their triggers. Safety and requested completeness still apply. [Setup](../plugins/README.md).
- **Context7 (`context7`)** — Current library documentation through MCP. Ask: “Check the current Spring Boot documentation for this API.” The agent resolves the library before querying its docs. Requires a working connection. Queries leave the machine, so exclude secrets and unnecessary proprietary text. [Setup](PACKAGES.md#host-and-plugins).
- **GitHub (`github`)** — Repository, issue, and pull-request operations through MCP. Ask: “Read this PR and summarize its review comments.” Requires transport-specific authentication and repository permissions. Native GitHub tools are a separate access path. Publishing or changing remote state needs authorization. [Setup](PACKAGES.md#host-and-plugins).

### Ponytail controls

The installed source used to prepare this guide documents `/ponytail [lite|full|ultra|off]`. For example, `/ponytail lite` selects lighter guidance. Command visibility depends on the host and role filters, so natural-language requests are the safest starting point.

The package also documents these controls, which are not guaranteed to appear in every launcher role:

- `/ponytail-review [target]` — Review a diff or target for over-engineering.
- `/ponytail-audit [target]` — Audit a broader target for simplification opportunities.
- `/ponytail-debt` — Collect `ponytail:` shortcut comments into a report.
- `/ponytail-gain` — Show upstream benchmark results, not measured savings for your repository.
- `/ponytail-help` — Show the package reference.

The launcher globally selects `ponytail` and `ponytail-review`, not all six skills. See the pinned source linked in [Packages](PACKAGES.md#host-and-plugins) for the package's `after-install.md` and skill instructions. This export does not include installed package files.

## Local extensions

- **Launcher status extension** — Shows the selected model alias and role, such as `luna - backend`. Start with `ohMyPi -model=luna -type=backend`. The launcher creates a temporary extension and removes it on exit. It can also add the selected model profile's instructions. Requires the launcher prerequisites in [bin/README.md](../bin/README.md). It is not a separate plugin or a permission sandbox. [Implementation](../bin/ohMyPi.mjs).
- **OMP Browser Relay** — Optional access to existing browser tabs, including signed-in sessions. Ask: “Use Browser Relay to inspect the tab I specify, without submitting anything.” Requires a separately installed and loaded relay extension and an available tab. Keep relay access on loopback, never forward it, and authorize consequential actions explicitly. Tab selection is not a per-tab permission sandbox. The browser extension and browser profile are not included in this export. [Setup boundary](PACKAGES.md#optional-integrations).

## Selected MCP integrations

[profiles.yml](../profiles/profiles.yml) selects server names, not connection setup or credentials. These are all public selections. PM adds no servers beyond the two global selections.

| Integration / configured ID | Purpose and example request | Prerequisite and boundary |
| --- | --- | --- |
| Context7 — `context7:context7` | Library docs. “Check the current documentation for this API.” All roles. | Working MCP connection. Queries leave the machine. |
| GitHub — `github:github` | Repositories and PRs. “Summarize this PR's review comments.” All roles. | Authentication and repository access. Remote changes need authorization. |
| GitNexus — `gitnexus` | Graph search and impact. “Find callers affected by this change.” Backend, frontend, research. | Installed server and suitable index. Check freshness against current source. |
| JetBrains IDE — `jetbrains-ide` | IDE integration. “Use the available IDE tools to inspect this project.” Backend, frontend. | Separately configured IDE connection and open project. Operations depend on the mounted server. |
| Penpot — `penpot` | Editable designs. “Inspect this page and propose accessible layout changes.” Frontend, UX. | Separate connection and file access. Editing, publishing, and sharing need authorization. [Setup](../agent/skills/penpot-uiux-design/references/setup-troubleshooting.md). |
| Comfy local — `comfy-local` | ComfyUI workflows and images. “Inspect available workflows before proposing generation.” Frontend, UX. | Separate server and suitable models. Downloads, third-party nodes, and paid generation need authorization. |
| REA — `rea` | Authorized reverse engineering. “Inspect this local binary without executing it.” Research. | Separate server and required native backends. Runtime access, target execution, and device changes need explicit scope. |

The public [MCP manifest](../agent/mcp.json) contains only the GitNexus definition, with read-only mode requested. GitHub and Context7 definitions come from their plugins. Other selected servers need separate local configuration. Selection does not force-enable a disabled server or install missing dependencies. See [integration boundaries](PACKAGES.md#optional-integrations).

## Native supporting features — not extra plugins

These belong to OMP or its native configuration, not the three-plugin inventory.

- **LSP** — Symbol navigation, references, and diagnostics. Ask: “Find this symbol's references with LSP.” Requires a compatible language server and project configuration. Bootstrap skills are instructions, not installed server binaries.
- **Mnemopi memory** — Per-project recall and retention, with passive autolearning configured. Ask: “Recall our decision about this service” or “Remember this verified project constraint.” Requires the native memory backend. Do not retain credentials or treat recalled facts as stronger than current evidence. Automatic post-stop continuation is disabled. This export contains settings, not another machine's memories.
- **Bundled subagents** — Delegate independent investigation, implementation, or review. Ask: “Use a scout to locate the relevant implementation.” Requires an available bundled agent and model access. The supplied settings disable task isolation, so delegation is not a filesystem sandbox. Keep one writer per shared file.

The [native settings](../agent/config.yml) describe configuration intent, not runtime health. This guide adds no connections or permissions and makes no authentication or execution claims.
