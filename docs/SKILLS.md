# Skills

Describe the result you need in normal language. OMP uses the available skill descriptions to select relevant guidance.
You can also name a skill explicitly. When native skill commands are enabled, use `/skill:<name>`, such as `/skill:grill-me`.
`grill-me` is user-invoked, not an automatic interview mode.

This catalog lists 65 maintained definitions under `agent/skills`, plus six package-owned Ponytail skills below.
Names come from frontmatter, not directory names. The links account for the different shadcn, Supabase, and Taste directory names.

A catalog entry does not guarantee availability in your session. Launcher profile allowlists can hide skills.
[profiles.yml](../profiles/profiles.yml) owns exact memberships; [the profile guide](../profiles/README.md) explains selection.
Examples request a workflow; they do not bypass approval, execution, privacy, or installation rules.

## Research and decisions

| Skill | Purpose | Example request |
| --- | --- | --- |
| [code-research](../agent/skills/code-research/SKILL.md) | Trace implementations and call flows. | “Trace how this request reaches storage.” |
| [web-research](../agent/skills/web-research/SKILL.md) | Compare web sources and track evidence. | “Research these options using primary sources.” |
| [reverse-engineering](../agent/skills/reverse-engineering/SKILL.md) | Investigate authorized artifacts or behavior without source. | “Inspect this local package without running it.” |
| [media-knowledge](../agent/skills/media-knowledge/SKILL.md) | Turn TikTok and visual media into cited research. | “Summarize these clips with timestamped evidence.” |
| [feature-design](../agent/skills/feature-design/SKILL.md) | Clarify feature boundaries, trade-offs, and failure flows. | “Design this feature before implementation.” |
| [arena](../agent/skills/arena/SKILL.md) | Compare competing proposals on explicit request. | “Use Arena to compare implementation proposals.” |
| [prototype](../agent/skills/prototype/SKILL.md) | Build a throwaway experiment to resolve uncertainty. | “Prototype this state transition.” |
| [customer-evidence](../agent/skills/customer-evidence/SKILL.md) | Synthesize authorized, deidentified customer evidence. | “Find recurring needs in these anonymized interviews.” |
| [business-economics](../agent/skills/business-economics/SKILL.md) | Model pricing, unit economics, and runway. | “Compare these pricing scenarios and assumptions.” |

## Architecture and change

| Skill | Purpose | Example request |
| --- | --- | --- |
| [software-architecture](../agent/skills/software-architecture/SKILL.md) | Design responsibilities, boundaries, and dependencies. | “Review the boundaries between these services.” |
| [codebase-design](../agent/skills/codebase-design/SKILL.md) | Design small interfaces that hide useful complexity. | “Design a deeper module interface here.” |
| [improve-codebase-architecture](../agent/skills/improve-codebase-architecture/SKILL.md) | Survey architectural friction when requested. | “Survey this codebase for architectural friction.” |
| [domain-modeling](../agent/skills/domain-modeling/SKILL.md) | Clarify shared domain terms and context documents. | “Distinguish an order from a reservation.” |
| [api-design](../agent/skills/api-design/SKILL.md) | Design REST resources, contracts, and pagination. | “Design a paginated orders API.” |
| [api-robustness](../agent/skills/api-robustness/SKILL.md) | Protect input, error, and idempotency boundaries. | “Review this endpoint for unsafe input and duplicate effects.” |
| [deprecation-and-migration](../agent/skills/deprecation-and-migration/SKILL.md) | Plan or implement a scoped replacement and cutover. | “Plan migration away from this old API.” |
| [spec-to-code-compliance](../agent/skills/spec-to-code-compliance/SKILL.md) | Compare stated requirements with implementation evidence. | “Check this implementation against the acceptance criteria.” |
| [simplify](../agent/skills/simplify/SKILL.md) | Reduce code complexity while preserving behavior. | “Simplify this working function.” |
| [refactoring-specialist](../agent/skills/refactoring-specialist/SKILL.md) | Restructure scoped code without changing behavior. | “Refactor this module without changing its API.” |

## Review, debugging, and delivery

| Skill | Purpose | Example request |
| --- | --- | --- |
| [code-review](../agent/skills/code-review/SKILL.md) | Review changes or assess review feedback. | “Review this diff for correctness and maintainability.” |
| [systematic-debugging](../agent/skills/systematic-debugging/SKILL.md) | Find root causes before proposing fixes. | “Investigate this failure from the supplied logs.” |
| [testing](../agent/skills/testing/SKILL.md) | Design, add, and analyze relevant tests. | “Add tests for these error cases.” |
| [test-driven-development](../agent/skills/test-driven-development/SKILL.md) | Apply test-first development only when requested or required. | “Use TDD for this behavior change.” |
| [quick-pr-creator](../agent/skills/quick-pr-creator/SKILL.md) | Prepare branches, PR descriptions, and review submissions. | “Prepare a pull request for these changes.” |
| [resolving-merge-conflicts](../agent/skills/resolving-merge-conflicts/SKILL.md) | Resolve an existing conflict while preserving both intents. | “Resolve this in-progress merge conflict.” |
| [external-supply-chain-review](../agent/skills/external-supply-chain-review/SKILL.md) | Review external tools and packages before adoption. | “Review this plugin before installation.” |
| [infrastructure-review](../agent/skills/infrastructure-review/SKILL.md) | Review deployment, containers, infrastructure, and CI. | “Review this Dockerfile and deployment configuration.” |
| [observability-engineering](../agent/skills/observability-engineering/SKILL.md) | Design or debug logs, metrics, traces, and alerts. | “Review the metrics and alerts for this service.” |

## Kotlin and backend

| Skill | Purpose | Example request |
| --- | --- | --- |
| [kotlin-spring-backend](../agent/skills/kotlin-spring-backend/SKILL.md) | Implement and debug the repository’s Spring Boot stack. | “Add a validated Spring endpoint using existing patterns.” |
| [ktor-backend](../agent/skills/ktor-backend/SKILL.md) | Implement Ktor routes, contracts, persistence, and tests. | “Add a Ktor route with request validation.” |
| [ktor-runtime-troubleshooting](../agent/skills/ktor-runtime-troubleshooting/SKILL.md) | Diagnose Ktor plugin scope, ordering, and context. | “Find why this route has no authenticated principal.” |
| [kotlin-functional-style](../agent/skills/kotlin-functional-style/SKILL.md) | Write readable expression-oriented, null-safe Kotlin. | “Simplify these Kotlin collection transformations.” |
| [reactive-kotlin](../agent/skills/reactive-kotlin/SKILL.md) | Use coroutines, Flow, and structured concurrency. | “Review cancellation in this coroutine flow.” |
| [kotlin-quality-gates](../agent/skills/kotlin-quality-gates/SKILL.md) | Apply repository Kotlin quality rules and execution limits. | “Review this Kotlin change against our quality rules.” |
| [gradle-kotlin-dsl-doctor](../agent/skills/gradle-kotlin-dsl-doctor/SKILL.md) | Diagnose Gradle Kotlin DSL and dependency wiring. | “Diagnose this plugin-resolution error.” |
| [kotlin-spring-proxy-compatibility](../agent/skills/kotlin-spring-proxy-compatibility/SKILL.md) | Diagnose Spring interception and Kotlin proxy failures. | “Find why this transaction annotation is ignored.” |
| [jackson-kotlin-serialization-specialist](../agent/skills/jackson-kotlin-serialization-specialist/SKILL.md) | Diagnose Kotlin JSON mapping and compatibility. | “Explain missing versus null fields in this DTO.” |
| [omp-kotlin-lsp-bootstrap](../agent/skills/omp-kotlin-lsp-bootstrap/SKILL.md) | Set up or upgrade the official Kotlin LSP for OMP on Linux. | “Set up the official Kotlin language server for OMP.” |

## Data

| Skill | Purpose | Example request |
| --- | --- | --- |
| [database-architect](../agent/skills/database-architect/SKILL.md) | Design MongoDB documents, indexes, and data boundaries. | “Choose embedding or references for this MongoDB model.” |
| [mongodb-optimizer](../agent/skills/mongodb-optimizer/SKILL.md) | Optimize MongoDB queries, indexes, and pipelines. | “Analyze this slow MongoDB explain plan.” |
| [supabase-postgres-best-practices](../agent/skills/supabase-best-practices/SKILL.md) | Improve Postgres queries, schemas, and configuration. | “Review this Postgres query and its indexes.” |

## Frontend and design

| Skill | Purpose | Example request |
| --- | --- | --- |
| [product-ui-engineering](../agent/skills/product-ui-engineering/SKILL.md) | Build UI journeys, components, and frontend structure. | “Implement this responsive settings screen.” |
| [impeccable](../agent/skills/impeccable/SKILL.md) | Guide default product UI design and accessibility. | “Improve this dashboard’s layout and accessibility.” |
| [design-taste-frontend](../agent/skills/taste-skill/SKILL.md) | Art-direct explicitly requested Taste or marketing work. | “Use Taste for an art-directed campaign page.” |
| [ui-ux-pro-max](../agent/skills/ui-ux-pro-max/SKILL.md) | Find focused UI patterns, palettes, and UX guidance. | “Find suitable typography and chart guidance for this UI.” |
| [penpot-design-studio](../agent/skills/penpot-design-studio/SKILL.md) | Create editable Penpot designs and inspect design sources. | “Create an editable Penpot component library.” |
| [penpot-uiux-design](../agent/skills/penpot-uiux-design/SKILL.md) | Supply passive Penpot component and accessibility references. | “Use Penpot design-studio references for this component.” |
| [shadcn](../agent/skills/shadcn-best-practices/SKILL.md) | Compose, style, and debug shadcn/ui components. | “Build this form with the installed shadcn components.” |
| [react-best-practices](../agent/skills/react-best-practices/SKILL.md) | Improve React and Next.js performance patterns. | “Review this React page for rendering bottlenecks.” |
| [typescript-javascript-clean-code](../agent/skills/typescript-javascript-clean-code/SKILL.md) | Keep JavaScript and TypeScript readable and type-safe. | “Refactor this TypeScript module with safe boundaries.” |
| [frontend-testing-debugging](../agent/skills/frontend-testing-debugging/SKILL.md) | Investigate rendered UI and interaction failures. | “Debug this broken mobile menu in the browser.” |

## Documentation and agent guidance

| Skill | Purpose | Example request |
| --- | --- | --- |
| [documentation-and-adrs](../agent/skills/documentation-and-adrs/SKILL.md) | Document contracts, procedures, and consequential decisions. | “Record this architectural decision and its trade-offs.” |
| [service-documentation](../agent/skills/service-documentation/SKILL.md) | Build local-first Zensical service documentation sites. | “Create a source-backed service documentation portal.” |
| [archify](../agent/skills/archify/SKILL.md) | Create standalone interactive diagrams on request. | “Make this architecture explorable.” |
| [hyperframes](../agent/skills/hyperframes/SKILL.md) | Explain useful motion or sequences with local video. | “Use HyperFrames to explain this request lifecycle.” |
| [simple-english](../agent/skills/simple-english/SKILL.md) | Write clear, non-normative technical prose. | “Rewrite this runbook in simple English.” |
| [stop-slop](../agent/skills/stop-slop/SKILL.md) | Remove filler and formulaic prose without changing facts. | “Remove filler from this explanation.” |
| [humanizer](../agent/skills/humanizer/SKILL.md) | Humanize existing documentation only on explicit request. | “Humanize this documentation without changing its facts.” |
| [writing-for-agents](../agent/skills/writing-for-agents/SKILL.md) | Write or audit agent-facing rules and instructions. | “Audit these agent instructions for ambiguity.” |
| [skill-creator](../agent/skills/skill-creator/SKILL.md) | Create, revise, or explicitly evaluate OMP skills. | “Create a skill for this repeated workflow.” |

## Communication and continuity

| Skill | Purpose | Example request |
| --- | --- | --- |
| [i-have-adhd](../agent/skills/i-have-adhd/SKILL.md) | Keep replies answer-first, focused, and easy to follow. | “Explain this one step at a time.” |
| [caveman](../agent/skills/caveman/SKILL.md) | Compress wording while retaining technical substance. | “Use caveman mode for this explanation.” |
| [grill-me](../agent/skills/grill-me/SKILL.md) | Guide an explicit interview one decision at a time. | “Use grill-me to help me choose a design.” |
| [session-handoff](../agent/skills/session-handoff/SKILL.md) | Save or resume portable working context on request. | “Save where we are so I can resume tomorrow.” |
| [lesson-learned](../agent/skills/lesson-learned/SKILL.md) | Extract lessons supported by the current work. | “What did we learn from this fix?” |

## Plugin-owned Ponytail skills

These definitions belong to `@dietrichgebert/ponytail` 4.9.0, not `agent/skills`.
Links point to the pinned package source. See [Packages](PACKAGES.md) for installation and mode details.
Skill selection and the plugin’s persistent mode are separate controls.

### Selected globally by the launcher

| Skill | Purpose | Example request |
| --- | --- | --- |
| [ponytail](https://github.com/DietrichGebert/ponytail/blob/2ed6c52c9d7e5e56942508591085fd45dea277d3/skills/ponytail/SKILL.md) | Prefer the smallest implementation that meets the requirements. | “Use Ponytail for the simplest complete implementation.” |
| [ponytail-review](https://github.com/DietrichGebert/ponytail/blob/2ed6c52c9d7e5e56942508591085fd45dea277d3/skills/ponytail-review/SKILL.md) | Review a diff for unnecessary complexity, not general correctness. | “Review this diff for over-engineering.” |

### Defined by the package, not selected by launcher profiles

These require a session that exposes the package skill; the normal launcher allowlists do not select them.

| Skill | Purpose | Example request |
| --- | --- | --- |
| [ponytail-audit](https://github.com/DietrichGebert/ponytail/blob/2ed6c52c9d7e5e56942508591085fd45dea277d3/skills/ponytail-audit/SKILL.md) | Find unnecessary complexity across a repository. | “Use Ponytail to audit this repository for over-engineering.” |
| [ponytail-debt](https://github.com/DietrichGebert/ponytail/blob/2ed6c52c9d7e5e56942508591085fd45dea277d3/skills/ponytail-debt/SKILL.md) | Report existing ponytail comment markers as a debt ledger. | “Show the Ponytail debt markers in this repository.” |
| [ponytail-gain](https://github.com/DietrichGebert/ponytail/blob/2ed6c52c9d7e5e56942508591085fd45dea277d3/skills/ponytail-gain/SKILL.md) | Display package benchmark figures, not repository-specific savings. | “Show Ponytail’s benchmark scoreboard.” |
| [ponytail-help](https://github.com/DietrichGebert/ponytail/blob/2ed6c52c9d7e5e56942508591085fd45dea277d3/skills/ponytail-help/SKILL.md) | Explain the package’s modes and skills. | “Show Ponytail help.” |

Package guidance can describe other hosts. Follow OMP’s current commands and safety rules rather than copying host-specific setup commands.
