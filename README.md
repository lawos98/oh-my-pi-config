# Oh My Pi configuration

This public repository contains a sanitized copy of my Oh My Pi configuration.

The source installation uses OMP `18.2.4`. The snapshot contains configuration, model overlays, global rules, commands, skills, and a GitNexus MCP definition with a read-only tool allowlist. It does not contain credentials, authenticated or organization-specific MCP servers, plugin runtime state, logs, sessions, databases, caches, or machine-specific paths.

## Important warning

The included `agent/config.yml` sets:

```yaml
tools:
  approvalMode: yolo
```

This mode approves tool calls without an interactive confirmation. Review the complete configuration before you install it. Use a stricter approval mode if you do not want this behavior.

The base configuration selects GitHub Copilot and OpenAI Codex models. Authenticate the required providers separately on each machine. Change model names if your account does not provide them.

The configuration disables local memory and automatic learning:

```yaml
memory:
  backend: "off"
autolearn:
  enabled: false
  autoContinue: false
```

If you enable these features, local memory can send saved session history to the configured remote model. Automatic learning can write durable lessons and managed skills.

The reusable configuration does not include automatic QA reporting consent. Each installation must make that decision separately.

## Repository layout

```text
.
├── agent/
│   ├── behavior-control/config.json
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
├── profiles/
│   ├── f2p.yml
│   ├── p2w.yml
│   ├── p2w-codex.yml
│   └── p2w-codex-astra.yml
├── .gitignore
├── README.md
└── THIRD_PARTY_NOTICES.md
```

OMP loads user skills from `~/.omp/agent/skills/<name>/SKILL.md`, managed skills from `~/.omp/agent/managed-skills/<name>/SKILL.md`, commands from `~/.omp/agent/commands/<name>.md`, and MCP definitions from `~/.omp/agent/mcp.json`.

## Prerequisites

Install these tools before you continue:

- Oh My Pi
- Git
- Provider accounts with access to the configured models
- Bash and GNU coreutils (`sha512sum` is needed by the GitNexus procedure)
- A Nerd Font configured in your terminal for the shared symbol and status-line settings

The GitNexus MCP requires GitNexus and Node.js `^22.18.0 || >=24.11.0`. Its documented install uses Bun, `curl`, and `sha512sum`. The `/pr-review` command requires an authenticated GitHub CLI. The related sections give exact commands.

Check OMP:

```bash
omp --version
```

Use OMP `18.2.4` to match the source installation. This snapshot does not pin provider-side model availability or reproduce credentials.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/lawos98/oh-my-pi-config.git
cd oh-my-pi-config
```

### 2. Back up the current OMP files

Run the following blocks in Bash, from this checkout. The copy steps overwrite matching files and remove two retired skills. They preserve unrelated skills and model overlays. Stop OMP before installing or restoring files.

The MCP copy replaces the destination MCP file with the public GitNexus-only definition. Back up private integrations and merge them locally afterward; never commit them here.

```bash
(
  set -eu
  umask 077
  test -n "$HOME"
  test ! -L "$HOME/.omp"
  if [ -e "$HOME/.omp/agent" ] || [ -L "$HOME/.omp/agent" ]; then
    test -d "$HOME/.omp/agent"
    test ! -L "$HOME/.omp/agent"
  fi
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
    behavior-control \
    commands \
    skills \
    managed-skills
  do
    if [ -e "$HOME/.omp/agent/$path" ] || [ -L "$HOME/.omp/agent/$path" ]; then
      cp -a "$HOME/.omp/agent/$path" "$backup/agent/"
    fi
  done
  mkdir "$backup/profiles"
  test ! -L "$HOME/.omp/profiles"
  for name in f2p p2w p2w-codex p2w-codex-astra; do
    if [ -e "$HOME/.omp/profiles/$name.yml" ] || [ -L "$HOME/.omp/profiles/$name.yml" ]; then
      cp -a "$HOME/.omp/profiles/$name.yml" "$backup/profiles/"
    fi
  done

  printf 'omp-config-v2\n' > "$backup/FORMAT"
  printf 'Backup: %s\n' "$backup"
)
```

### 3. Install the rules, commands, skills, and MCP definition

```bash
(
  set -euo pipefail
  test -n "$HOME"
  test ! -L "$HOME/.omp"
  mkdir -p "$HOME/.omp/agent"
  test -d "$HOME/.omp/agent"
  test ! -L "$HOME/.omp/agent"

  for path in commands skills managed-skills behavior-control; do
    mkdir -p "$HOME/.omp/agent/$path"
    test -d "$HOME/.omp/agent/$path"
    test ! -L "$HOME/.omp/agent/$path"
  done

  for source in \
    agent/RULES.md \
    agent/coding-rules.md \
    agent/response-rules-reminder.md \
    agent/mcp.json \
    agent/behavior-control/config.json \
    agent/commands/create-skill.md \
    agent/commands/pr-review.md \
    agent/commands/self-review.md \
    agent/commands/simplify-code.md
  do
    test -f "$source"
    test ! -L "$source"
    destination="$HOME/.omp/agent/${source#agent/}"
    rm -rf -- "$destination"
    cp "$source" "$destination"
  done

  for category in skills managed-skills; do
    git ls-files -z -- ":(glob)agent/$category/*/SKILL.md" |
      while IFS= read -r -d '' source; do
        test -f "$source"
        test ! -L "$source"
        destination="$HOME/.omp/agent/${source#agent/}"
        skill_dir="${destination%/SKILL.md}"
        rm -rf -- "$skill_dir"
        mkdir -p "$skill_dir"
        cp "$source" "$destination"
      done
  done
  rm -rf -- \
    "$HOME/.omp/agent/commands/build-feature.md" \
    "$HOME/.omp/agent/commands/build-ui.md" \
    "$HOME/.omp/agent/commands/gitnexus-analyze.md" \
    "$HOME/.omp/agent/commands/kotlin-quality.md" \
    "$HOME/.omp/agent/commands/omp-health.md" \
    "$HOME/.omp/agent/skills/auth-patterns" \
    "$HOME/.omp/agent/skills/kotlin-intellij-plugin-dev"

  chmod 600 "$HOME/.omp/agent/mcp.json"
  chmod 600 "$HOME/.omp/agent/behavior-control/config.json"
)
```

### 4. Install the configuration

Review `agent/config.yml` first. Pay special attention to model names, `approvalMode`, memory, and automatic learning.

```bash
(
  set -eu
  test -n "$HOME"
  test ! -L "$HOME/.omp"
  test -d "$HOME/.omp/agent"
  test ! -L "$HOME/.omp/agent"
  test -f agent/config.yml
  test ! -L agent/config.yml
  rm -rf -- "$HOME/.omp/agent/config.yml"
  cp agent/config.yml "$HOME/.omp/agent/config.yml"
  chmod 600 "$HOME/.omp/agent/config.yml"
  mkdir -p "$HOME/.omp/profiles"
  test ! -L "$HOME/.omp/profiles"
  for name in f2p p2w p2w-codex p2w-codex-astra; do
    test -f "profiles/$name.yml"
    test ! -L "profiles/$name.yml"
    rm -f -- "$HOME/.omp/profiles/$name.yml"
    cp "profiles/$name.yml" "$HOME/.omp/profiles/$name.yml"
    chmod 600 "$HOME/.omp/profiles/$name.yml"
  done
)
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

### Model overlays

These files contain model choices, not credentials. They are `--config` overlays, **not** OMP's isolated `--profile` directories.

| Overlay | Requirements |
|---|---|
| `p2w.yml` | GitHub Copilot access to the configured Luna models |
| `p2w-codex.yml` | OpenAI Codex access to the configured Luna models |
| `p2w-codex-astra.yml` | OpenAI Codex access to Astra and Luna models |
| `f2p.yml` | LM Studio running with the configured Qwen model loaded; configure its connection locally |

For example, select the Astra overlay after installation:

```bash
omp --config "$HOME/.omp/profiles/p2w-codex-astra.yml"
```

Or load both files without installing the base configuration:

```bash
omp --config "$PWD/agent/config.yml" --config "$PWD/profiles/p2w-codex-astra.yml"
```

Later overlays take precedence. Shell aliases are not copied. See [OMP configuration overlays](https://github.com/can1357/oh-my-pi/blob/main/docs/settings.md).

`agent/behavior-control/config.json` selects the behavior-control verifier model. It requires the optional `pi-behavior-control` plugin and OpenAI Codex access independently of the selected overlay.

## Verification

Run these checks from a normal writable OMP installation:

```bash
omp --version
omp read skill://infrastructure-review/SKILL.md
omp read skill://observability-engineering/SKILL.md
omp read skill://api-robustness/SKILL.md
gitnexus --version
```

Each `omp read` command must return the selected skill. If a skill is missing, check its directory name and `SKILL.md` frontmatter. Start a new OMP session and confirm that command completion lists `/self-review` and `/create-skill`.

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
| `async.maxJobs: 8` | Limits concurrent background jobs. |
| `task.eager: default` | Uses the default task eagerness. |
| `task.batch: true` | Enables batched subagent tasks. |
| `task.isolation.enabled: false` | Disables task isolation; delegated edits can share the working tree. |
| `task.isolation.merge: patch` | Selects patch merging when isolation is enabled. |
| `task.maxConcurrency: 4` | Limits concurrent delegated tasks. |
| `task.maxRecursionDepth: 1` | Limits nested task delegation. |
| `compaction.enabled` | Enables context compaction. |
| `compaction.midTurnEnabled` | Allows compaction during a turn. |
| `skills.enabled` | Enables native OMP skill discovery. |
| `modelRoles` | Selects default, fast, task, plan, and slow models. |
| `cycleOrder` | Defines the model-switch order. |
| `tools.approvalMode: yolo` | Approves tool calls without an interactive prompt. |
| `memory.backend: off` | Disables local memory. |
| `autolearn.enabled: false` | Disables automatic learning. |
| `autolearn.autoContinue: false` | Disables automatic continuation after learning writes. |
| `edit.mode: hashline` | Uses line-anchored hashline edits. |
| `security.enabled` | Enables OMP security features. |

## Commands

Files under `agent/commands/` become slash commands in a new OMP session.

| Command | Purpose | Extra requirement |
|---|---|---|
| `/create-skill` | Creates one validated managed skill without duplicating existing capabilities. | Automatic learning enabled |
| `/pr-review` | Reviews the current GitHub pull request and drafts line comments after approval. | GitHub CLI authentication |
| `/self-review` | Reviews every change since `main` for evidence-backed correctness, security, architecture, and maintainability defects. | A Git repository with local `main` or `origin/main` |
| `/simplify-code` | Removes accidental complexity while preserving observable behavior. | None |

Do not use `/self-review` or `/create-skill` from an untrusted repository or directory. OMP loads project instructions before it expands a slash command, so verifying the command cannot neutralize hostile project context. In a trusted repository, run the built-in `/extensions` inspector and require the active entry to show `Origin: via OMP (User)` with the exact path `~/.omp/agent/commands/<name>.md`; stop if it does not. A matching description is not proof of origin. See [OMP slash-command precedence](https://github.com/can1357/oh-my-pi/blob/main/docs/slash-command-internals.md#provider-specific-source-paths-and-local-precedence).

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
| `database-architect` | Designs MongoDB schemas, indexes, migrations, and data-layer boundaries. |
| `mongodb-optimizer` | Optimizes MongoDB queries, aggregation pipelines, indexes, and connection pools. |
| `kotlin-spring-backend` | Guides Kotlin Spring Boot implementation, testing, operations, clients, and persistence. |
| `reactive-kotlin` | Covers coroutines, Flow, WebFlux, cancellation, backpressure, and safe retries. |
| `kotlin-quality-gates` | Applies repository-specific ktlint, detekt, Gradle, and Kotlin quality checks. |
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
| `clean-code` | Keeps naming and design guidance available but hidden from automatic skill discovery. |
| `software-architecture` | Designs the smallest architecture that preserves contracts and clear boundaries. |
| `feature-design` | Converts product intent into requirements, acceptance criteria, and implementation plans. |
| `simplify` | Simplifies code without changing observable behavior. |
| `ponytail` | Selects the smallest working solution and rejects unnecessary abstractions or dependencies. |
| `ponytail-review` | Reviews only for over-engineering and identifies code that can be deleted. |
| `test-driven-development` | Applies strict Red-Green-Refactor only when the user or repository explicitly requires TDD. |
| `verification-before-completion` | Keeps verification guidance available but hidden from automatic skill discovery. |

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
| `documentation-and-adrs` | Records design decisions and maintains technical documentation. |
| `humanizer` | Rewrites selected documentation only on explicit request while preserving technical meaning. |

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

### Differences from the source machine

This snapshot reproduces the public configuration, not a complete workstation:

- Internal MCP servers, company skills, and custom company agents require separate private setup. The public MongoDB skill retains generic guidance instead of internal deployment assumptions.
- Provider authentication, installed LSP binaries, local model servers, and shell aliases are not transferred.
- The local manifest also lists `@latentminds/pi-quotas@0.5.0`. Its runtime is not copied or installed by these instructions; review it separately before adding it.
- New local skills with incomplete provenance are not included: `api-design`, `testing`, `caveman`, `codebase-design`, `domain-modeling`, `diagnosing-bugs`, `grill-me`, `grill-me-with-docs`, `ship`, `resolving-merge-conflicts`, and `kotlin-functional-style`. An MIT label alone does not establish the source and required copyright notice.
- The local migration skill contains machine-specific paths. The macOS LSP bootstrap skill currently targets OpenCode despite its name. Neither is included as an OMP setup procedure.
- `auth-patterns` and `kotlin-intellij-plugin-dev` are removed because they are absent from the source installation.

Review the pre-existing provenance concerns in `THIRD_PARTY_NOTICES.md` before further redistribution.

OpenCode-specific `simplify/README.md` and `simplify/codemap.md` are also excluded; the standalone `SKILL.md` does not reference them.

## Update the installed copy

Pull the repository, create a new backup, and repeat the copy steps:

```bash
(
  set -eu
  root="$(git rev-parse --show-toplevel)"
  status="$(git -C "$root" -c core.fsmonitor=false --no-pager status --porcelain=v1 --untracked-files=all --ignore-submodules=none)"
  test -z "$status"
  before="$(git -C "$root" rev-parse HEAD)"
  git -C "$root" pull --ff-only
  git -C "$root" -c core.fsmonitor=false --no-pager diff --no-relative --ignore-submodules=none --no-ext-diff --no-textconv --summary "$before" HEAD
  git -C "$root" -c core.fsmonitor=false --no-pager diff --no-relative --ignore-submodules=none --no-ext-diff --no-textconv "$before" HEAD
)
```

Review the complete pulled diff before you create a backup or overwrite the installed copy: commands, rules, configuration, MCP definitions, skills, file modes, and symlink targets. Stop if any source, intent, or change is unclear.

## Restore a backup

Replace `<backup>` with the path printed during installation. Restoration removes only the controlled paths listed below, then copies their saved versions. This also removes commands, skills, or MCP configuration that did not exist before installation.

This procedure accepts backups created by this revision (`omp-config-v2`). For an older `omp-config-v1` backup, use the restore procedure from the repository revision that created it.

```bash
(
  set -eu
  backup="<backup>"
  test -n "$HOME"
  test ! -L "$HOME/.omp"
  test "$(cat "$backup/FORMAT")" = "omp-config-v2"
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
    behavior-control \
    commands \
    skills \
    managed-skills
  do
    rm -rf -- "$HOME/.omp/agent/$path"
    if [ -e "$backup/agent/$path" ] || [ -L "$backup/agent/$path" ]; then
      cp -a "$backup/agent/$path" "$HOME/.omp/agent/"
    fi
  done
  test -d "$backup/profiles"
  test ! -L "$backup/profiles"
  mkdir -p "$HOME/.omp/profiles"
  test ! -L "$HOME/.omp/profiles"
  for name in f2p p2w p2w-codex p2w-codex-astra; do
    rm -f -- "$HOME/.omp/profiles/$name.yml"
    if [ -e "$backup/profiles/$name.yml" ] || [ -L "$backup/profiles/$name.yml" ]; then
      cp -a "$backup/profiles/$name.yml" "$HOME/.omp/profiles/"
    fi
  done
)
```

Restart OMP after restoration.

## Sources and licenses

This repository is public. It does not apply one blanket license to all files. Some skills adapt third-party guidance under different licenses.

Read [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). Preserve embedded source and license sections when you modify or redistribute a skill.
