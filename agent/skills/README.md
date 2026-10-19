# Skills

Skills add task-specific guidance. Read the selected `SKILL.md`, then load supporting references only when needed. Availability does not authorize commands, installs, network access, or publication.

## Groups

The [profile configuration](../../profiles/profiles.yml) owns exact membership. These are the main areas, not a second catalog:

| Area | Guidance |
| --- | --- |
| Shared work | Focused replies, research, decisions, handoffs, prose and supply-chain review |
| Backend | Kotlin, Spring, Ktor, Gradle, serialization, APIs, databases and operations |
| Frontend | TypeScript, React, shadcn, browser debugging and testing |
| UX | Impeccable, optional Taste, Penpot and UI design references |
| Product and research | Customer evidence, economics, media and authorized reverse engineering |
| Documentation | Contracts, ADRs, Archify diagrams and optional HyperFrames video |

Impeccable is the default interface-design authority. Taste is for explicit requests or art-directed marketing work; do not load both automatically. The `taste-skill` directory declares the skill name `design-taste-frontend`.

## Supporting files

Keep each skill's references, scripts, templates, assets and license files together. React's measurement workflow and rule files belong to `react-best-practices`. Ponytail is [plugin-owned](../../plugins/README.md), not copied here.

Archify includes its renderer source and editable example JSON. Generated example HTML is omitted. HyperFrames includes its adapter, illustrative composition and dependency lock, but not installed packages or browser state. Before approved use, install the locked runtime separately and set `CHROME_PATH` to an approved absolute Chromium executable path. Archify's PNG adapter uses that same runtime. No helper downloads a browser on your behalf. Taste also needs an approved existing browser for inspection.

Paths in examples assume installation under `$HOME/.omp`; adjust them for another installation root. Runtime helpers are optional capabilities, not automatic setup steps.

## Service documentation

[service-documentation](service-documentation/SKILL.md) is part of this catalog,
not a separate managed package. Use it for source-backed service documentation
sites. Its [authoring reference](service-documentation/references/authoring.md)
and templates cover Zensical, API pages, diagrams, video, and an inert Pages workflow.
Dependencies and publication require separate approval.

## Generated candidates

All maintained local skills live here. Native autolearning may create candidates
in `agent/managed-skills`; review and explicitly promote them into this catalog
before selecting them in a launcher profile. Plugin-owned skills stay in their
packages, without duplicate copies here.


## Public snapshot boundaries

- Company-only `jira-ticket-creator` and `kotlin-spring-hexagonal-service` are excluded. Generic Kotlin guidance remains; links to unavailable company-specific guidance are removed.
- The project-specific Penpot reference is excluded. The generic Penpot workflow and support assets remain.
- Obsolete `diagnosing-bugs`, `frontend-app-builder`, `omp-setup-maintenance` and `stripe-best-practices` are removed to match the current source inventory.
- General guidance formerly stored under `managed-skills` now lives here. React performance guidance is part of `react-best-practices`.
- Caches, installed dependencies, credentials, databases, generated renders and local acceptance reports are not included.

Provenance records describe upstream revisions and historical local reviews. They do not establish that this public export was executed or cleared for every use. See [third-party notices](../../THIRD_PARTY_NOTICES.md) for license limits and unresolved attribution issues.
