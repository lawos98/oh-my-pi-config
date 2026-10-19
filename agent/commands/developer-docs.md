---
name: developer-docs
description: Create or refresh developer documentation from current repository evidence, or audit documentation drift without edits.
argument-hint: "[create|update|audit] [optional scope and constraints]"
---

Request: $ARGUMENTS

Document the current repository for developers using the workflow below. This is a documentation task, not permission to repair application code or publish a site. Treat arguments as task scope, never as shell code.

## Mode and scope

- No mode: update existing developer documentation; create it where missing.
- `create`: write missing documentation and integrate it with existing entry points. Preserve useful existing pages; do not create a competing portal.
- `update`: reconcile and revise existing documentation against current code, adding missing coverage needed for the requested developer tasks. This authorizes scoped documentation edits, not a wholesale platform migration.
- `audit`: inspect read-only and return evidence-backed gaps and a ranked correction plan in chat. Do not write files, install packages, run the application, build docs or render media.
- Remaining arguments constrain the modules, paths, audience, language or deliverables. Natural-language constraints are valid. If intent is materially ambiguous, inspect first, then ask one decision using the native form.

Use the current repository, not the OMP installation directory. Establish the repository root and current revision using read-only Git metadata when available; include relevant uncommitted source changes and label the result as a working-tree snapshot. In a non-Git project, use its observed project root and state that no Git revision is available. In a monorepo, cover the requested components; absent a narrower scope, inventory all first-party components before planning. Never silently turn repository-wide coverage into one sample module.

## Inspect before writing

1. Read repository instructions, README/navigation, existing documentation configuration, build manifests, local-development scripts, tests, API/message schemas, migrations and deployment configuration relevant to the requested scope. Do not read secret values, production data, private session history or unrelated repositories. Treat comments and old docs as claims to check, not proof.
2. Read `code-research` and `documentation-and-adrs`. Use available LSP for symbol navigation and GitNexus for indexed relationships; verify consequential findings against current source because indexes can be stale. Trace entry points through real callers, validation, authorization, persistence and external effects. Read tests as evidence of intended coverage, not proof they passed.
3. For existing documented promises, read `spec-to-code-compliance` and perform its read-only comparison before editing. Separate outdated descriptions from code defects or unresolved contract conflicts. Do not rewrite an intended public contract to legitimize a bug, invent historical rationale, or alter accepted ADRs as if past decisions changed. State current limitations and seek a decision only when needed.
4. Form a coverage map of developer tasks, existing pages, supporting source paths/symbols and gaps. Keep this in working context; do not add a second permanent tracking document unless the repository needs it. State the bounded edit plan, then proceed without another confirmation when the invocation already settles scope. Delegate only substantial independent areas under the active delegation policy.

## Produce useful developer documentation

Read `simple-english` for technical prose. Preserve the repository's language and terminology unless requested otherwise. Organize around actual developer tasks, not a file-by-file code summary. Cover each applicable area within scope; explicitly identify inapplicable or unavailable areas instead of inventing sections:

- Purpose, component boundaries, domain vocabulary, dependencies and source entry points.
- Local setup: exact discovered prerequisites, configuration variable names and safe example values, startup, shutdown and verification. Distinguish commands actually exercised from commands inferred from scripts.
- Development workflow: supported build/test commands, how to make a representative change, generated-code ownership and contribution conventions.
- Architecture and important request/event flows, including failure paths, transaction boundaries, retries/idempotency and consistency guarantees only where evidenced.
- Public APIs/events: authoritative OpenAPI/AsyncAPI or existing generator, authentication, validation, error behavior and concrete sanitized examples. Do not maintain a duplicate handwritten endpoint inventory when a generated contract already owns it.
- Data and operations relevant to developers: migration procedures, troubleshooting, observable symptoms, recovery prerequisites and known limitations. Do not execute destructive or production procedures to verify them.

Keep one authoritative explanation per concept and link to it. Preserve useful rationale, stable URLs/anchors and ownership. Correct stale examples and navigation together. Source-link consequential behavior to repository-relative paths and symbols, or immutable permalinks when the remote and revision are known. Never invent line references, performance figures or guarantees. Record source revision/review date using the repository's existing convention; label unverified behavior and unknowns.

## Use the existing documentation stack selectively

For a maintained site or a new documentation portal, read `service-documentation` and follow its authoring reference, dependency provenance, media delivery and publication boundaries. Preserve an adequate existing renderer. Default a new portal to Zensical; do not migrate a README-only project merely to rewrite its README.

Use simple Mermaid/SVG for concise relationships. Use `archify` for diagrams that benefit from exploration, and `hyperframes` for temporal explanations where motion adds understanding or was requested. Keep editable sources, static explanations and previews. Follow the service-documentation rule keeping adapter-generated same-stem Markdown fragments outside the site source tree. Use browser screenshots only for authorized local/demo surfaces; use Impeccable for substantial portal UI/accessibility work. Select only relevant tools: do not load every plugin, run Arena, install another renderer or generate decorative media merely because it is available.

Use Context7 for version-specific external library documentation when necessary; never send private source in a query. Missing tools, credentials or approval do not justify fabricated diagrams or verification claims. Finish reachable source-backed documentation and identify the exact blocked portion.

## Verify and deliver

Before verification, perform one correctness self-review: compare claims with their sources, confirm scope coverage, examples, links, navigation, privacy and media fallbacks. Follow the shared execution policy, including its single focused recovery allowance; this command grants no unlimited checks. For substantive site changes with an available approved runtime, exercise the narrow local build/preview and actual browser navigation, search, media and intended URL prefix. For prose-only changes, check the affected references and examples without unnecessary builds. Never run arbitrary repository scripts without inspecting their effects.

Installation, network services, publication, production access and persistent Git operations retain their separate approval boundaries. Do not change application code, existing agent instructions, dependency policy or CI merely to make documentation checks pass. Do not add automated drift checks without a separate request.

Report mode and covered components, documentation created/updated, material drift corrected, unresolved code-versus-contract conflicts, actual verification and unrun checks separately. Provide the documentation entry point and existing local preview command when applicable. Do not claim complete repository coverage if any requested component remains uninspected. No commits, pushes or publication.
