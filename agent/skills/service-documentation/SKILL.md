---
name: service-documentation
description: "Create or maintain local-first service documentation sites with Zensical and optional GitHub Pages, combining source-backed explanations, API references, images, interactive diagrams and useful video. Use for a service-docs portal or reusable documentation workflow, not ordinary README edits, standalone diagrams or prose-only reviews."
---

# Service documentation

Build documentation for developers and operators from actual service evidence. For a new site, default to Zensical with project-local dependencies and optional GitHub Pages delivery. Preserve an adequate existing documentation system; this skill does not authorize migration, installation or publication by itself.

## Establish the source and scope

1. Inspect the selected repository's instructions, existing docs/configuration, build, authoritative API/message contracts and relevant implementation. Use available LSP/GitNexus for navigation, with current source as authority. Ask only for material audience/access/scope decisions that the repository cannot settle.
2. Read `skill://documentation-and-adrs` for contracts/runbooks and `skill://simple-english` for reader-facing technical prose. For new portal UI or substantial usability changes use `skill://impeccable`; do not import its runtime or add a second design authority automatically.
3. Separate implemented facts, intended contracts, illustrative examples and unknowns. Source-link consequential statements to the relevant version. An authored diagram or animation is not a measured trace. Never publish invented endpoints, timings, failure guarantees or a generic template as documentation of the service.

## Author the site

For new-site configuration, media/API patterns and optional deployment, read [references/authoring.md](references/authoring.md). Inspect [provenance.json](provenance.json) before using the pinned dependency set; it records admission and verification limits.

- Default workspace: `docs-site/` inside the selected service repository, unless its conventions say otherwise. Reuse an existing site rather than copying over it. The [templates](templates/) are a complete guide to this documentation workflow, not a service's content. Copy reviewed files without overwriting existing work, then replace the guide with real source-backed documentation before describing it as service documentation.
- Keep Zensical configuration, Markdown, the dependency lock and original media sources in the project. Install the reviewed [requirements.lock](templates/requirements.lock) only after permission, into that project's own virtual environment. No global Python installation or automatic upgrades. Re-review unsupported platforms/new versions rather than silently weakening pins.
- Organize around the reader's tasks: getting started, relevant architecture/flows, API/message reference and operational procedures. Do not create empty categories or placeholder pages merely to fill navigation.
- Preserve the existing OpenAPI/AsyncAPI owner/generator. Render a release artifact; don't maintain a second independent endpoint list. API renderer adoption is separate from Zensical adoption. Default to read-only reference; request execution requires an explicitly approved sandbox, not production credentials or a public proxy.

## Select media by the question

- Small relationship or layout: native Mermaid/SVG, without adding a runtime merely for decoration.
- Explorable architecture/sequence: read `skill://archify` and use its installed adapter. Keep editable JSON, interactive HTML, PNG preview and an adjacent text explanation. Link standalone HTML first; embed only when it improves the reader task and the actual host permits it. Preserve keyboard access and static fallback.
- UI procedure: existing browser capture against authorized local/demo data. Keep the capture scenario and service revision; a screenshot mask does not redact a trace or video.
- Temporal order/concurrency/state change: read `skill://hyperframes` and use its installed local adapter when motion adds understanding or the user requests it. Keep its composition/assets and complete static explanation alongside playback HTML, MP4 and poster. Explicit no-video requests win. No autoplay; narration requires reviewed captions and transcript, not an unapproved TTS service.
- Include media with page-relative URLs that work under both local hosting and a GitHub project subpath. Surround iframe/API content with searchable prose; do not assume the portal search indexes iframe internals. Generated HTML/PNG/MP4 are derivatives, not the only editable sources.

## Local preview and optional publication

Use the project virtual environment and explicit loopback preview. Inspect the authored configuration before executing: docs builds can load code, fetch assets and clean output directories. Keep outputs outside source and prohibit arbitrary remote assets/plugins in a private/local-only workflow.

The [GitHub Pages workflow](templates/github-pages.yml.example) is inert reference material. Copying it into `.github/workflows` and configuring Pages requires explicit publication approval. Keep manual dispatch and environment protection; do not push, enable deployments or publish automatically. A private repository does not make ordinary GitHub Pages private; restricted Pages requires eligible enterprise access controls. Review the entire static artifact, including search indexes, schemas and media, before sharing.

## Verify and deliver

Perform one final correctness review, then the narrow authorized check under OMP's shared execution policy. Verify the actual delivered surface, not just a successful build: navigation/search, source/example accuracy, keyboard operation, diagram/media controls, static fallbacks, asset URLs under the intended base path, and absence of unintended remote requests or secrets. Include API sandbox behavior only when that feature is authorized. For source/documented-contract differences use `skill://spec-to-code-compliance` within its read-only scope.

Deliver the site source, local start/build instructions, generated output when requested, and editable media sources. Separate checks actually exercised from unverified accessibility/offline/hosting claims. Existing global approval, supply-chain and bounded-recovery rules remain authoritative; neither the templates nor upstream commands grant extra permission.
