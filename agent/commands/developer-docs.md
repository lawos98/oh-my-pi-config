---
name: developer-docs
description: Create, update, regenerate, improve or audit source-backed developer documentation using the installed documentation and media skills.
argument-hint: "[create|update|regenerate|improve|audit] [optional scope and constraints]"
---

Request: $ARGUMENTS

Document the current repository for developers using the workflow below. This is a documentation task, not permission to repair application code or publish a site. Treat arguments as task scope, never as shell code.

## Mode and scope

- No mode: update existing developer documentation; create it where missing.
- `create`: write missing documentation and integrate it with existing entry points. Preserve useful existing pages; do not create a competing portal.
- `update`: reconcile and revise existing documentation against current code, adding missing coverage needed for the requested developer tasks. This authorizes scoped documentation edits, not a wholesale platform migration.
- `regenerate`: re-inspect the full requested scope and refresh source-derived documentation in place. Preserve useful manual content, history, stable destinations and user edits; do not delete/recreate a docs directory or migrate the platform.
- `improve`: improve the requested existing documentation's explanations, structure, navigation, examples and visuals. Verify affected claims without silently expanding to a whole-service re-audit.
- `audit`: inspect read-only and return evidence-backed gaps and a ranked correction plan in chat. Do not write files, install packages, run the application, build docs or render media.
- Remaining arguments constrain the modules, paths, audience, language or deliverables. Natural-language constraints are valid. If intent is materially ambiguous, inspect first, then ask one decision using the native form.

Use the current repository, not the OMP installation directory. Establish the repository root and current revision using read-only Git metadata when available; include relevant uncommitted source changes and label the result as a working-tree snapshot. In a non-Git project, use its observed project root and state that no Git revision is available. In a monorepo, cover the requested components; absent a narrower scope, inventory all first-party components before planning. Never silently turn repository-wide coverage into one sample module.

## Inspect before writing

1. Read repository instructions, README/navigation, existing documentation configuration, build manifests, local-development scripts, tests, API/message schemas, migrations and deployment configuration relevant to the requested scope. Do not read secret values, production data, private session history or unrelated repositories. Treat comments and old docs as claims to check, not proof.
2. Read `code-research`, `documentation-and-adrs` and its [source-to-documentation workflow](../skills/documentation-and-adrs/SOURCE-TO-DOCS.md). That reference owns source discovery, the page catalogue, traceability, mode-specific synchronization and baseline limits. Use available LSP for symbol navigation and GitNexus for indexed relationships; verify consequential findings against current source because indexes can be stale. Trace entry points through real callers, validation, authorization, persistence and external effects. Read tests as evidence of intended coverage, not proof they passed.
3. For existing documented promises, read `spec-to-code-compliance` and perform its read-only comparison before editing. Separate outdated descriptions from code defects or unresolved contract conflicts. Do not rewrite an intended public contract to legitimize a bug, invent historical rationale, or alter accepted ADRs as if past decisions changed. State current limitations and seek a decision only when needed.
4. Form the reference's source-backed page catalogue before drafting. Reuse existing source-to-section evidence and reviewed baselines for targeted updates; establish associations when needed for repeated maintenance, without a compulsory second manifest or background checker. Keep audit mappings in working context. Include related pages, editable visuals and their derivatives in the bounded edit plan, then proceed without another confirmation when the invocation already settles scope. Delegate only substantial independent areas under the active delegation policy.

When the current profile selects `documentation-review`, read it for `audit` and `improve`, or a requested substantive documentation critique. Diagnose structure and technical claims within the existing review; audit remains read-only and improvement does not authorize unrelated rewrites. When the scope includes hands-on learning or newcomer onboarding, read `tutorial-authoring` if selected: define a reproducible start, checkpoints, recovery, final outcome and safe reset. It is not needed for every setup/reference page. The research profile selects both specialists; other profiles retain the base workflow without assuming unavailable skills. These handoffs add no reviewer agents, extra checks or authority to execute a tutorial.

## Produce useful developer documentation

Read `simple-english` for technical prose. Preserve the repository's language and terminology unless requested otherwise. Organize around actual developer tasks, not a file-by-file code summary. Cover each applicable area within scope; explicitly identify inapplicable or unavailable areas instead of inventing sections:

- Purpose, component boundaries, domain vocabulary, dependencies and source entry points.
- Local setup: exact discovered prerequisites, configuration variable names and safe example values, startup, shutdown and verification. Distinguish commands actually exercised from commands inferred from scripts.
- Development workflow: supported build/test commands, how to make a representative change, generated-code ownership and contribution conventions.
- Architecture and important request/event flows, including failure paths, transaction boundaries, retries/idempotency and consistency guarantees only where evidenced.
- Public APIs/events: authoritative OpenAPI/AsyncAPI or existing generator, authentication, validation, error behavior and concrete sanitized examples. Do not maintain a duplicate handwritten endpoint inventory when a generated contract already owns it.
- Data and operations relevant to developers: migration procedures, troubleshooting, observable symptoms, recovery prerequisites and known limitations. Do not execute destructive or production procedures to verify them.

Keep one authoritative explanation per concept and link to it. Preserve useful rationale, stable URLs/anchors and ownership. Correct stale examples and navigation together. Source-link consequential behavior to repository-relative paths and symbols, or immutable permalinks when the remote and revision are known. Never invent line references, performance figures or guarantees. Record source revision/review date using the repository's existing convention; label unverified behavior and unknowns.

## ADR authoring

When the requested scope includes creating, updating, reformatting or showing an ADR, read the shared [ADR authoring style](../../docs/ADR-AUTHORING.md) together with `documentation-and-adrs`. It owns this user's default section order and full `=== "A · Label"` option tabs: mechanism, numbered **How It May Work**, concrete code/configuration/database examples as relevant, **Example**, and `!!! success "Positive"` / `!!! failure "Negative"` callouts. An overview table does not replace these bodies. Preserve accepted decisions and detailed rejected alternatives; pending/team proposals have no selected option. Do not compress tabs away during visual/prose improvements or copy service-specific rules into unrelated ADRs. Other documentation keeps its own appropriate structure.

## Use the existing documentation stack selectively

For a maintained site or a new documentation portal, read `service-documentation` and follow its authoring reference, dependency provenance, media delivery and publication boundaries. Preserve an adequate existing renderer. Default a new portal to Zensical; do not migrate a README-only project merely to rewrite its README.

Use native Mermaid/SVG for ordinary small inline explanations. For new handbook process/architecture diagrams, follow `service-documentation` and default to `archify` unless the repository has another convention. Apply the HTML-site diagram contract below to documentation pages and ADRs with interactive diagrams. Handbook animation/video requires an explicit request; when requested use `hyperframes` for video or `archify` for trace motion. Follow the service-documentation rule keeping adapter-generated same-stem Markdown fragments outside the site source tree. Use browser screenshots only for authorized local/demo surfaces; use Impeccable for substantial portal UI/accessibility work. Select only relevant tools: do not load every plugin, run Arena, install another renderer or generate decorative media merely because it is available.

Use Context7 for version-specific external library documentation when necessary; never send private source in a query. Missing tools, credentials or approval do not justify fabricated diagrams or verification claims. Finish reachable source-backed documentation and identify the exact blocked portion.

### HTML-site diagram contract

For HTML documentation sites, including rendered ADRs, present each Archify or other interactive diagram as one iframe visual. This contract governs the site's presentation when linked skill guidance calls for static previews or alternatives; retain those assets without displaying a second copy on the HTML page.

- Do not add duplicate `<details>` diagrams, static previews, image copies, or diagram download/open-link rows alongside the iframe. Keep exports available through the viewer's controls rather than a second presentation block.
- Keep the authoritative editable JSON/source and generated HTML/static assets for exports, offline use and non-HTML delivery. Remove duplicate presentation markup, not source files or useful derivatives. Keep a complete searchable adjacent explanation and source evidence in the host page; iframe content alone does not satisfy documentation coverage or accessibility.
- Use the full available content width. Adapt the iframe height to its complete rendered content, including controls and labels, on initial load and after layout, viewport or theme changes. The outer documentation page owns scrolling; avoid nested iframe scrollbars and fixed-height caps that cut off content. Do not disguise overflow with clipping or shrink typography to force a fit.
- Preserve fullscreen, keyboard navigation and focus access, light/dark theme behavior, and exports. Fullscreen may use its own viewport layout; returning to the page must restore content-height sizing.
- During authorized browser verification, inspect the rendered page for a single visual, full width, complete content height, outer-page scrolling and preserved controls. Retained offline/export assets and adjacent prose remain part of delivery; report unexercised behavior rather than claiming it was checked.

## Verify and deliver

Before verification, perform one correctness self-review: compare claims with their sources, confirm scope coverage, examples, links, navigation, privacy and media fallbacks. Follow the shared execution policy, including its single focused recovery allowance; this command grants no unlimited checks. For substantive site changes with an available approved runtime, exercise the narrow local build/preview and actual browser navigation, search, media and intended URL prefix. For prose-only changes, check the affected references and examples without unnecessary builds. Never run arbitrary repository scripts without inspecting their effects.

Installation, network services, publication, production access and persistent Git operations retain their separate approval boundaries. Do not change application code, existing agent instructions, dependency policy or CI merely to make documentation checks pass. Do not add automated drift checks without a separate request.

Report mode and covered components, documentation created/updated, material drift corrected, unresolved code-versus-contract conflicts, actual verification and unrun checks separately. Provide the documentation entry point and existing local preview command when applicable. Do not claim complete repository coverage if any requested component remains uninspected. No commits, pushes or publication.
