# Oh My Pi configuration

This private repository contains a sanitized copy of my Oh My Pi configuration.

The snapshot was tested with OMP `18.0.11`. It contains configuration, global rules, commands, skills, and a GitNexus MCP definition with a read-only tool allowlist. It does not contain credentials, authenticated or organization-specific MCP servers, plugin runtime state, logs, sessions, databases, caches, or machine-specific paths.

## Important warning

The included `agent/config.yml` sets:

```yaml
tools:
  approvalMode: yolo
```

This mode approves tool calls without an interactive confirmation. Review the complete configuration before you install it. Use a stricter approval mode if you do not want this behavior.

The configuration also selects OpenAI Codex model names. Change these names if your account does not provide the same models.

The configuration enables local memory and automatic learning:

```yaml
memory:
  backend: local
autolearn:
  enabled: true
  autoContinue: true
```

Local memory can summarize saved session history with the configured remote model. Automatic learning can write durable lessons and managed skills. Set `memory.backend` to `off` and both `autolearn` values to `false` if session history must not be processed.

The reusable configuration does not include automatic QA reporting consent. Each installation must make that decision separately.

## Repository layout

```text
.
├── agent/
│   ├── commands/
│   │   └── <command>.md
│   ├── managed-skills/
│   │   └── <skill-name>/SKILL.md
│   ├── skills/
│   │   └── <skill-name>/SKILL.md
│   ├── config.yml
│   ├── mcp.json
│   ├── RULES.md
│   ├── coding-rules.md
│   └── response-rules-reminder.md
├── .gitignore
├── README.md
└── THIRD_PARTY_NOTICES.md
```

OMP loads user skills from `~/.omp/agent/skills/<name>/SKILL.md`, managed skills from `~/.omp/agent/managed-skills/<name>/SKILL.md`, commands from `~/.omp/agent/commands/<name>.md`, and MCP definitions from `~/.omp/agent/mcp.json`.

## Prerequisites

Install these tools before you continue:

- Oh My Pi
- Git
- An authenticated GitHub account that can read this private repository

The GitNexus MCP and `/gitnexus-analyze` command also require GitNexus and Node.js `^22.18.0 || >=24.11.0`. Its documented install uses Bun, `curl`, and `sha512sum`. The `/pr-review` command requires an authenticated GitHub CLI. The related sections give exact commands.

Check OMP:

```bash
omp --version
```

This snapshot uses OMP `18.0.11`. Other versions are not verified by this repository.

## Installation

### 1. Clone the repository

```bash
git clone git@github.com:lawos98/oh-my-pi-config.git
cd oh-my-pi-config
```

### 2. Back up the current OMP files

The copy steps overwrite files with the same names. They do not delete other skills.

```bash
(
  set -eu
  umask 077
  test -n "$HOME"
  backup="$HOME/.omp-backups/omp-$(date +%Y%m%d-%H%M%S)"
  mkdir -p "$HOME/.omp-backups"
  mkdir "$backup"
  mkdir "$backup/agent"

  for path in \
    config.yml \
    mcp.json \
    RULES.md \
    coding-rules.md \
    response-rules-reminder.md \
    commands \
    skills \
    managed-skills
  do
    if [ -e "$HOME/.omp/agent/$path" ]; then
      cp -a "$HOME/.omp/agent/$path" "$backup/agent/"
    fi
  done

  printf 'omp-config-v1\n' > "$backup/FORMAT"
  printf 'Backup: %s\n' "$backup"
)
```

### 3. Install the rules, commands, skills, and MCP definition

```bash
mkdir -p "$HOME/.omp/agent/commands"
mkdir -p "$HOME/.omp/agent/skills"
mkdir -p "$HOME/.omp/agent/managed-skills"

cp agent/RULES.md "$HOME/.omp/agent/RULES.md"
cp agent/coding-rules.md "$HOME/.omp/agent/coding-rules.md"
cp agent/response-rules-reminder.md "$HOME/.omp/agent/response-rules-reminder.md"
cp agent/mcp.json "$HOME/.omp/agent/mcp.json"
cp -a agent/commands/. "$HOME/.omp/agent/commands/"
cp -a agent/skills/. "$HOME/.omp/agent/skills/"
cp -a agent/managed-skills/. "$HOME/.omp/agent/managed-skills/"
chmod 600 "$HOME/.omp/agent/mcp.json"
```

### 4. Install the configuration

Review `agent/config.yml` first. Pay special attention to model names, `approvalMode`, memory, and automatic learning.

```bash
cp agent/config.yml "$HOME/.omp/agent/config.yml"
chmod 600 "$HOME/.omp/agent/config.yml"
```

If you do not want the shared configuration, skip this step.

You can also test the configuration as a process-only overlay:

```bash
omp --config "$PWD/agent/config.yml"
```

### 5. Start a new OMP session

Start a new process after you copy the files. A new process reloads commands, skills, rules, MCP servers, and configuration.

```bash
omp
```

## Verification

Run these checks from a normal writable OMP installation:

```bash
omp --version
omp read skill://infrastructure-review/SKILL.md
omp read skill://observability-engineering/SKILL.md
omp read skill://api-robustness/SKILL.md
gitnexus --version
```

Each `omp read` command must return the selected skill. If a skill is missing, check its directory name and `SKILL.md` frontmatter. Start OMP and run `/omp-health` to inspect command, skill, plugin, and MCP discovery without changing the installation.

## Optional plugins

Plugins are separate from this repository snapshot. Plugin code runs inside OMP and can execute installation lifecycle steps. Review every source before installation.

The source setup used these versioned package plugins:

```bash
omp plugin install @dietrichgebert/ponytail@4.9.0
omp plugin install pi-behavior-control@0.1.9
omp plugin install @plannotator/pi-extension@0.27.9
```

It also used three plugins from the audited Anthropic marketplace commit `ed404106fcd80ba98ecb7c851e531dcb626d13b7`:

```bash
(
  set -eu
  marketplace="$HOME/.local/share/omp-marketplaces/claude-plugins-official-ed404106"
  test ! -e "$marketplace"
  git clone https://github.com/anthropics/claude-plugins-official.git "$marketplace"
  git -C "$marketplace" checkout ed404106fcd80ba98ecb7c851e531dcb626d13b7
  test "$(git -C "$marketplace" rev-parse HEAD)" = "ed404106fcd80ba98ecb7c851e531dcb626d13b7"
  omp plugin marketplace add "$marketplace"
  omp plugin install --scope user context7@claude-plugins-official
  omp plugin install --scope user github@claude-plugins-official
  omp plugin install --scope user frontend-design@claude-plugins-official
)
```

The catalog and these three plugin manifests do not declare versions. OMP therefore records the documented fallback version `0.0.0`; the checked-out commit, not that fallback value, binds the installed source. Do not pull or update this marketplace without reviewing and recording the new commit first.

| Plugin | Purpose |
|---|---|
| `ponytail` | Prefers the smallest solution and rejects unnecessary code or dependencies. |
| `pi-behavior-control` | Adds response, review, and verification guardrails. |
| `Plannotator` | Provides guided plan and code-review annotation tools. |
| `context7` | Retrieves current library and framework documentation. |
| `github` | Adds GitHub issue, pull-request, and repository integration. |
| `frontend-design` | Adds visual design guidance for frontend work. |

Package plugins are installed under `~/.omp/plugins/node_modules/` and recorded in OMP's package and lock files. Marketplace plugins use `~/.omp/marketplaces.json`, `~/.omp/plugins/installed_plugins.json`, a shared cache, a generated symlink, and the plugin lock file. These paths are mutable installation state, not source configuration, so this repository excludes them.

The local `~/.omp/vendor/ponytail/` directory is a stale, duplicate multi-harness source copy. The active OMP plugin loads the installed `@dietrichgebert/ponytail@4.9.0` package instead. Do not copy `vendor/` into this repository or into another OMP installation.

Check plugin state without applying fixes:

```bash
omp plugin list --json
omp plugin doctor
```

Use `/reload-plugins` after a skill, command, agent, or MCP-only plugin change. Restart OMP after an install or upgrade that adds or changes executable tools, hooks, or extensions; the active extension runner is not rebuilt in place.

## Configuration reference

| Setting | Purpose |
|---|---|
| `async.enabled` | Enables background work. |
| `async.maxJobs: 4` | Limits concurrent background jobs. |
| `task.eager: preferred` | Prefers early task execution. |
| `task.batch: true` | Enables batched subagent tasks. |
| `task.isolation.mode: rcopy` | Uses repository-copy isolation for delegated work. |
| `task.isolation.merge: patch` | Applies isolated changes as patches. |
| `task.maxRecursionDepth: 3` | Limits nested task delegation. |
| `compaction.enabled` | Enables context compaction. |
| `compaction.midTurnEnabled` | Allows compaction during a turn. |
| `skills.enabled` | Enables native OMP skill discovery. |
| `modelRoles` | Selects default, fast, task, plan, and slow models. |
| `cycleOrder` | Defines the model-switch order. |
| `tools.approvalMode: yolo` | Approves tool calls without an interactive prompt. |
| `memory.backend: local` | Stores memory locally but can send saved session history to a configured remote model for summarization. |
| `autolearn.enabled` | Enables durable learning that can write lessons and managed skills. |
| `autolearn.autoContinue` | Continues automatically after a learning write. |
| `edit.mode: hashline` | Uses line-anchored hashline edits. |
| `security.enabled` | Enables OMP security features. |

## Commands

Files under `agent/commands/` become slash commands in a new OMP session.

| Command | Purpose | Extra requirement |
|---|---|---|
| `/build-feature` | Implements a complete feature with the smallest repository-compatible design and end-to-end verification. | None |
| `/build-ui` | Implements and browser-verifies a complete accessible UI. | The optional `frontend-design` plugin improves visual guidance. |
| `/gitnexus-analyze` | Creates a local, index-only GitNexus graph and reports status. | GitNexus |
| `/kotlin-quality` | Runs the repository's existing narrowest ktlint and detekt Gradle tasks for changed Kotlin. | A Kotlin Gradle repository |
| `/omp-health` | Audits the active OMP configuration without changing it or reading credentials. | None |
| `/pr-review` | Reviews the current GitHub pull request and drafts line comments after approval. | GitHub CLI authentication |
| `/simplify-code` | Removes accidental complexity while preserving observable behavior. | None |

## GitNexus MCP

`agent/mcp.json` starts `gitnexus mcp` through `PATH`. It contains no server endpoint, token, account, or absolute path. `GITNEXUS_MCP_READ_ONLY=1` excludes GitNexus mutation tools such as rename, Cypher, and group synchronization. `DO_NOT_TRACK=1` and `SCARF_ANALYTICS=false` disable Scarf analytics.

Install the reviewed package tarball with Bun:

```bash
(
  set -eu
  package_dir="$HOME/.local/share/omp-packages"
  archive="$package_dir/gitnexus-1.6.10.tgz"
  partial="$archive.part"
  mkdir -p "$package_dir"
  test -d "$package_dir"
  test ! -L "$package_dir"
  test ! -e "$archive"
  test ! -e "$partial"
  trap 'rm -f "$partial"' EXIT
  curl --proto '=https' --tlsv1.2 --fail --location \
    https://registry.npmjs.org/gitnexus/-/gitnexus-1.6.10.tgz \
    --output "$partial"
  printf '%s  %s\n' \
    9afe7eceb01a1272e62f7e267d7b0a395ae163d99a9fe98747c662cda4291dab89a317de1e40979deeb6c84633724e78d3f1e70e09a002ad92373411f1bce917 \
    "$partial" | sha512sum --check
  mv "$partial" "$archive"
  trap - EXIT
  DO_NOT_TRACK=1 SCARF_ANALYTICS=false bun add --global "$archive"
  test "$(gitnexus --version)" = "1.6.10"
)
```

The digest matches the npm registry integrity for GitNexus `1.6.10`. Bun records the local archive path, so keep this verified, versioned archive while GitNexus is installed. The package declares Node.js `^22.18.0 || >=24.11.0`, uses the PolyForm Noncommercial 1.0.0 license, and runs a post-install script. Review that license, the package, its lock resolution, and lifecycle scripts before installation.

Create an index from the repository that you want to inspect:

```bash
(
  set -eu
  test ! -e .gitnexusrc
  test -z "${GITNEXUS_EMBEDDING_URL+x}${GITNEXUS_EMBEDDING_MODEL+x}${GITNEXUS_EMBEDDING_API_KEY+x}"
  DO_NOT_TRACK=1 SCARF_ANALYTICS=false GITNEXUS_LBUG_EXTENSION_INSTALL=load-only \
    gitnexus analyze --index-only
  gitnexus status
)
```

Indexing creates local generated state under `.gitnexus/`, updates the global registry under `~/.gitnexus/registry.json`, and can add a local Git exclude entry. Do not commit the index. The MCP server uses the local index and does not require authentication; its recovery path can repair local index sidecars. Run `/mcp reload` after you install GitNexus or change `agent/mcp.json`.

## Global rule files

| File | Purpose |
|---|---|
| `agent/RULES.md` | Defines global engineering, verification, delegation, LSP, and Git safety rules. |
| `agent/coding-rules.md` | Adds Kotlin, Spring Boot, MongoDB, and Gradle review rules. |
| `agent/response-rules-reminder.md` | Requires concise, evidence-based responses with exact verification results. |

## Skills

### Backend, Kotlin, and data

| Skill | Purpose |
|---|---|
| `api-robustness` | Validates API input, protects internal errors, and defines atomic idempotency behavior. |
| `auth-patterns` | Covers authentication, authorization, password storage, sessions, tokens, CSRF, CORS, and secrets. |
| `database-architect` | Designs MongoDB schemas, indexes, migrations, and data-layer boundaries. |
| `mongodb-optimizer` | Optimizes MongoDB queries, aggregation pipelines, indexes, and connection pools. |
| `kotlin-spring-backend` | Guides Kotlin Spring Boot implementation, testing, operations, clients, and persistence. |
| `reactive-kotlin` | Covers coroutines, Flow, WebFlux, cancellation, backpressure, and safe retries. |
| `kotlin-quality-gates` | Applies repository-specific ktlint, detekt, Gradle, and Kotlin quality checks. |
| `kotlin-intellij-plugin-dev` | Guides IntelliJ Platform plugin development with Kotlin and JetBrains APIs. |
| `omp-kotlin-lsp-bootstrap` | Installs and verifies the official JetBrains Kotlin LSP for OMP. |

### TypeScript, React, and UI

| Skill | Purpose |
|---|---|
| `typescript-javascript-clean-code` | Enforces readable TypeScript and JavaScript with safe boundaries and types. |
| `product-ui-engineering` | Designs and implements web UI, user journeys, responsive layouts, and frontend architecture. |
| `react-performance` | Reviews React performance, rendering, data flow, and bundle behavior. |

### Architecture and code quality

| Skill | Purpose |
|---|---|
| `clean-code` | Guides naming, cohesion, dependencies, errors, tests, and practical SOLID decisions. |
| `software-architecture` | Designs the smallest architecture that preserves contracts and clear boundaries. |
| `feature-design` | Converts product intent into requirements, acceptance criteria, and implementation plans. |
| `simplify` | Simplifies code without changing observable behavior. |
| `ponytail` | Selects the smallest working solution and rejects unnecessary abstractions or dependencies. |
| `ponytail-review` | Reviews only for over-engineering and identifies code that can be deleted. |
| `test-driven-development` | Applies a Red-Green-Refactor workflow when lasting behavior needs regression protection. |
| `verification-before-completion` | Requires fresh verification evidence before completion claims. |

### Research, review, and debugging

| Skill | Purpose |
|---|---|
| `code-research` | Traces unfamiliar local or remote codebases and implementation patterns. |
| `web-research` | Performs multi-source web research with source tracking and cross-verification. |
| `code-review` | Reviews correctness, security, performance, maintainability, and test coverage. |
| `systematic-debugging` | Uses reproduction, evidence, hypotheses, root-cause fixes, and focused verification. |
| `external-supply-chain-review` | Audits external repositories, plugins, skills, packages, installers, and MCP servers before adoption. |

### Infrastructure, observability, and writing

| Skill | Purpose |
|---|---|
| `infrastructure-review` | Reviews Docker, Terraform, Kubernetes, Helm, CI/CD, secrets, and deployment safety. |
| `observability-engineering` | Guides metrics, logs, traces, OpenTelemetry, cardinality, alerts, and dashboards. |
| `simple-english` | Writes clear technical documentation with a pragmatic Simplified Technical English subset. |

### GitHub workflow

| Skill | Purpose |
|---|---|
| `quick-pr-creator` | Prepares GitHub pull requests and requires approval before push or PR creation. |

## Intentionally excluded

The repository excludes these items:

- authentication and credential state
- authenticated, internal, and organization-specific MCP servers
- Jira and organization-specific skills
- plugin caches, registries, package state, generated lock files, and duplicate `vendor/` source trees
- GitNexus indexes and its global registry
- logs, sessions, databases, histories, memories, blobs, and terminal state
- local IDE metadata and hardware cache files
- absolute machine paths and timestamps
- installation-specific automatic QA reporting consent

Do not copy your complete `~/.omp` directory into Git. Use an explicit allowlist.

## Update the installed copy

Pull the repository, create a new backup, and repeat the copy steps:

```bash
git pull --ff-only
```

Review changed skills before you overwrite the installed copy.

## Restore a backup

Replace `<backup>` with the path printed during installation. Restoration removes only the controlled paths listed below, then copies their saved versions. This also removes commands, skills, or MCP configuration that did not exist before installation.

```bash
(
  set -eu
  backup="<backup>"
  test -n "$HOME"
  test "$(cat "$backup/FORMAT")" = "omp-config-v1"
  test -d "$backup/agent"
  test ! -L "$backup/agent"
  test -d "$HOME/.omp/agent"
  test ! -L "$HOME/.omp/agent"
  for path in \
    config.yml \
    mcp.json \
    RULES.md \
    coding-rules.md \
    response-rules-reminder.md \
    commands \
    skills \
    managed-skills
  do
    rm -rf -- "$HOME/.omp/agent/$path"
    if [ -e "$backup/agent/$path" ] || [ -L "$backup/agent/$path" ]; then
      cp -a "$backup/agent/$path" "$HOME/.omp/agent/"
    fi
  done
)
```

Restart OMP after restoration.

## Sources and licenses

This repository is a private configuration backup. It does not apply one blanket license to all files. Some skills adapt third-party guidance under different licenses.

Read [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). Preserve embedded source and license sections when you modify or redistribute a skill.
