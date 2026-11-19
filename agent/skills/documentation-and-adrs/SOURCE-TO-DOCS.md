# Generate and maintain documentation from code

Use for explicit requests to create, update, regenerate, improve, or audit current-system documentation from a repository. `/developer-docs` owns mode selection and permissions; this reference owns discovery, page planning, and source-to-document synchronization. Use [AUTHORING.md](AUTHORING.md) for writing quality and `service-documentation` for site/media delivery. This is not a separate runtime, installer, or background process.

## 1. Establish the repository and evidence boundary

Read repository instructions, current docs/navigation, and the relevant source, configuration, schemas, tests, build and development scripts. Establish the actual root and inspected revision or working-tree scope. Use existing LSP/GitNexus for navigation when available; inspect current source to confirm indexed claims. Do not send private source to external discovery or documentation services.

Identify all first-party components in the requested scope before selecting deep dives. Include non-code artifacts that change behavior: profiles, mappings, migrations, schemas, CI declarations, deployment configuration and background-task registration. Do not infer architecture from directory names or equate configured subscriptions, passing-looking tests, or an accepted historical ADR with effective deployed behavior.

## 2. Plan pages around questions and evidence

Build a source-backed page catalogue in working context, reusing the existing navigation and documentation ownership. Each planned page or substantial section identifies:

- the reader's question and intended audience;
- its existing destination path/anchor, or the smallest justified new destination;
- supporting source paths, symbols, schemas and relevant configuration;
- related pages and source dependencies outside the immediate module;
- important failure/empty/unmatched/partial-result paths;
- dependent diagram/chart sources and exports;
- evidence gaps and what remains outside scope.

For a service handbook, consider orientation/domain vocabulary, setup, HTTP/message contracts, major journeys, state/storage, integrations, background work, contributor workflows, operations and known contract discrepancies. Include only applicable content, but do not silently omit a requested component. Keep exact reference directly reachable from an overview.

Trace representative vertical paths, not just isolated files: entry point → mapping/validation/authorization → application/domain behavior → persistence/external effects → response or deferred work. Check collaborating paths and consumers that change the explanation. Draft cohesive mechanisms or leaf sections first, then synthesize their overview; recheck source for consequential parent claims instead of treating generated prose as independent evidence.

Use credible decision/history evidence for the rationale behind existing choices. A recurring code pattern alone supports a description of the mechanism, not an invented ADR or rejected alternative.

## 3. Preserve source-to-document traceability

Use the repository's existing evidence record or source links as the first source-to-document map. For repeated synchronization, retain relevant associations in that existing record. If it has no suitable location and persistent traceability is needed for the requested maintenance workflow, add a concise table to the owning documentation/evidence page, not a second tracking service or compulsory manifest.

A useful association contains:

| Field | Meaning |
| --- | --- |
| Destination | Page and section/anchor whose explanation depends on the source |
| Evidence | Source paths/symbols, configuration and contract owners |
| Baseline | Last actually reviewed revision, plus working-tree limits where relevant |
| Dependents | Related reference/journey pages and editable visuals/exports |
| Ownership | Human-authored prose versus explicitly designated generated regions |
| Review state | Inspected, partially inspected, unresolved, or not checked |

Keep source associations broad enough to include shared DTOs, routing, rules, configuration and consumer dependencies. A file glob is an investigation hint, not a complete semantic dependency graph. Do not introduce AUTOGEN markers into hand-written docs merely to make updates easier. Honor existing generated boundaries only after checking their generator and ownership.

## 4. Synchronize deliberately

For `update`, use a verified review baseline and read-only source-change metadata when available, including uncommitted/untracked relevant files. Follow changed and renamed/deleted source through its documented callers, contracts, configuration, related pages and visuals. Update affected explanations and their dependents together; leave unrelated content intact.

If the baseline is absent, invalid, or does not represent the inspected working tree, inspect the requested scope directly. Do not invent a commit, claim no changes from timestamps alone, or silently turn a scoped update into a repository-wide rewrite. Unchanged code does not prove unchanged documentation requirements, external contracts, configuration, or dependencies. Report exactly what was reviewed.

For `regenerate`, re-establish the full requested catalogue from current evidence and refresh its source-derived explanations in place. Regeneration is not directory deletion or permission to overwrite manual notes, accepted ADR rationale, specifications, unrelated pages or user edits. Preserve paths/anchors and canonical ownership where possible. Remove only content established to be obsolete within scope; explain unresolved historical/contract conflicts instead of erasing them. Render affected derivatives only with an available approved runtime.

For `improve`, improve navigation, layering, examples, explanations, accessibility and visual usefulness within the requested existing content. Check the evidence behind changed claims; do not broaden into a full source re-audit, application fix, platform migration or new behavior specification. Label unresolved accuracy gaps.

For `create`, write missing coverage using the catalogue without replacing useful existing docs. For `audit`, keep catalogue and mappings in working context and return gaps in chat: no documentation/map writes, renders, builds, installation or execution of application code.

Advance a review baseline only for coverage actually inspected. If the repository tracks a single whole-scope baseline, do not advance it after a partial update. Keep partial coverage visible rather than marking the entire handbook current.

## 5. Use the installed stack, not another wiki platform

Use `documentation-and-adrs` for durable explanations, significance-based ADR handling and evidence distinctions. Use `domain-modeling` when terminology needs resolution, `software-architecture` for necessary boundary analysis, and `spec-to-code-compliance` for documented-promise conflicts. Proposed specifications belong to `feature-design`, not inferred current-system docs.

Use `service-documentation` for an existing or requested portal and its Archify-first handbook policy. Keep complete searchable text, editable diagram sources, static previews and chart provenance; handbook motion/video requires an explicit request. Improve substantial portal usability with Impeccable, not a new UI framework by default.

Keep generated API references with their current owner. Reuse an existing OpenAPI/AsyncAPI artifact, Dokka reference, or test-generated HTTP snippets when present and relevant. A missing reference generator is a separately reviewed adoption decision, not permission to add dependencies, run application tests or manufacture a schema from guesses. Distinguish schema fields from actual handler/consumer behavior.

No upstream plugin runner, extra graph index, public wiki ingestion, model-provider setup, automatic CI, deployment workflow, or source-containing cache is added by this workflow. Missing tools do not justify placeholders or fabricated coverage: finish supported work and report the exact blocked portion.

## 6. Finish with bounded evidence

Use the command's correctness review and shared execution policy. Verify the actual approved delivery surface when site/media behavior changes. Report mode, covered components/pages, source revision and limits, changed explanations/assets, preserved manual/history content, unresolved discrepancies, checks actually exercised, and unreviewed scope. Never call an entire service documented when only selected modules were inspected.

## Research provenance

Locally authored guidance informed by these MIT-licensed source snapshots; no upstream executable, template, agent definition or instruction text is imported:

- [Microsoft Deep Wiki](https://github.com/microsoft/skills/tree/a779d00cf3749577a7777422ab6dee9e66dcb2e2/.github/plugins/deep-wiki): source-backed catalogue, page citations and related-page navigation. Excludes VitePress, diagram/length quotas, instruction-file generation and deployment.
- [natsu1211 DeepWiki skill](https://github.com/natsu1211/deepwiki-skill/tree/887304e68ff3711a964bcb4b3f33e47ad53c4405): explicit source-to-section associations and review baselines. Excludes installers, Python helpers, permission bypass, marker adoption, automated deletion and retry orchestration.
- [wshobson documentation-generation](https://github.com/wshobson/agents/tree/0874a27b17a22e2b7c2e2bcd725768e0803cad06/plugins/documentation-generation): reference/tutorial and API-coverage distinctions. Excludes additional agents, CI, linting and deployment automation.
- [FSoft CodeWiki](https://github.com/FSoft-AI4Code/CodeWiki/tree/03d0a294ad58f3c878bd8aeb0ef5e95a2ff8c3ca): leaf-first explanation followed by overview synthesis. Excludes its runtime, MCP, parser/index storage, provider configuration and automatic validation retries.

These are research references, not runtime dependencies, installation recommendations, or claims that generated output was tested. See [SOURCE-TO-DOCS.provenance.json](SOURCE-TO-DOCS.provenance.json) for the bounded integration record.
