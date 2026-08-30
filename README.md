# Oh My Pi configuration

This private repository contains a sanitized copy of my Oh My Pi configuration.

The snapshot was tested with OMP `18.0.11`. It contains configuration, global rules, and skills. It does not contain credentials, MCP servers, commands, plugin runtime state, logs, sessions, databases, caches, or machine-specific paths.

## Important warning

The included `agent/config.yml` sets:

```yaml
tools:
  approvalMode: yolo
```

This mode approves tool calls without an interactive confirmation. Review the complete configuration before you install it. Use a stricter approval mode if you do not want this behavior.

The configuration also selects OpenAI Codex model names. Change these names if your account does not provide the same models.

The configuration enables local memory and automatic learning. Local memory can summarize saved session history by calling the configured remote model. Automatic learning can write durable lessons and managed skills. Disable both features before installation if session history must not be processed:

```yaml
memory:
  backend: off
autolearn:
  enabled: false
  autoContinue: false
```

The reusable configuration does not include automatic QA reporting consent. Each installation must make that decision separately.

## Repository layout

```text
.
├── agent/
│   ├── config.yml
│   ├── RULES.md
│   ├── coding-rules.md
│   ├── response-rules-reminder.md
│   ├── skills/
│   │   └── <skill-name>/SKILL.md
│   └── managed-skills/
│       └── <skill-name>/SKILL.md
├── .gitignore
├── README.md
└── THIRD_PARTY_NOTICES.md
```

OMP loads user skills from `~/.omp/agent/skills/<name>/SKILL.md`. Managed skills use `~/.omp/agent/managed-skills/<name>/SKILL.md`.

## Prerequisites

Install these tools before you continue:

- Oh My Pi
- Git
- An authenticated GitHub account that can read this private repository

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
umask 077
backup="$HOME/.omp-backups/omp-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup/agent"

for path in \
  config.yml \
  RULES.md \
  coding-rules.md \
  response-rules-reminder.md \
  skills \
  managed-skills
do
  if [ -e "$HOME/.omp/agent/$path" ]; then
    cp -a "$HOME/.omp/agent/$path" "$backup/agent/"
  fi
done

printf 'Backup: %s\n' "$backup"
```

### 3. Install the rules and skills

This step does not change commands or MCP configuration.

```bash
mkdir -p "$HOME/.omp/agent/skills"
mkdir -p "$HOME/.omp/agent/managed-skills"

cp agent/RULES.md "$HOME/.omp/agent/RULES.md"
cp agent/coding-rules.md "$HOME/.omp/agent/coding-rules.md"
cp agent/response-rules-reminder.md "$HOME/.omp/agent/response-rules-reminder.md"
cp -a agent/skills/. "$HOME/.omp/agent/skills/"
cp -a agent/managed-skills/. "$HOME/.omp/agent/managed-skills/"
```

### 4. Install the configuration

Review `agent/config.yml` first. Pay special attention to model names, `approvalMode`, memory, and automatic learning.

```bash
cp agent/config.yml "$HOME/.omp/agent/config.yml"
chmod 600 "$HOME/.omp/agent/config.yml"
```

If you only want the skills and rules, skip this step.

You can also test the configuration as a process-only overlay:

```bash
omp --config "$PWD/agent/config.yml"
```

### 5. Start a new OMP session

Start a new process after you copy the files. A new process reloads skills, rules, and configuration.

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
```

Each `omp read` command must return the selected skill. If a skill is missing, check its directory name and `SKILL.md` frontmatter.

## Optional plugins

This repository does not store plugin caches, generated lock files, marketplace state, or installed plugin registries. Plugin code runs inside OMP and can execute installation lifecycle steps. Review every source before installation.

The source setup used these versioned packages:

```bash
omp plugin install --scope user @dietrichgebert/ponytail@4.9.0
omp plugin install --scope user pi-behavior-control@0.1.9
omp plugin install --scope user @plannotator/pi-extension@0.27.9
```

The source setup also used `context7`, `github`, and `frontend-design` from Anthropic's plugin marketplace. These packages reported version `0.0.0`, and the marketplace source is mutable. They are inventory only. This repository does not provide runnable install commands without an audited immutable revision and per-plugin digest.

| Plugin | Purpose |
|---|---|
| `ponytail` | Prefers the smallest solution and rejects unnecessary code or dependencies. |
| `pi-behavior-control` | Adds response, review, and verification guardrails. |
| `Plannotator` | Provides guided plan and code-review annotation tools. |
| `context7` | Retrieves current library and framework documentation. |
| `github` | Adds GitHub issue, pull-request, and repository integration. |
| `frontend-design` | Adds visual design guidance for frontend work. |

Check plugin state without applying fixes:

```bash
omp plugin list --json
omp plugin doctor
```

Use `/reload-plugins` in an active OMP session after a skill-only plugin change. Restart OMP after a tool, hook, or extension change.

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

- `agent/mcp.json`
- all OMP commands
- authentication and credential state
- Jira and organization-specific skills
- plugin caches, registries, package state, and generated lock files
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

Replace `<backup>` with the path printed during installation:

```bash
cp -a <backup>/agent/. "$HOME/.omp/agent/"
```

Restart OMP after restoration.

## Sources and licenses

This repository is a private configuration backup. It does not apply one blanket license to all files. Some skills adapt third-party guidance under different licenses.

Read [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). Preserve embedded source and license sections when you modify or redistribute a skill.
