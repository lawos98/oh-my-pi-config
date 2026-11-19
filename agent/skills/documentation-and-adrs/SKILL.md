---
name: documentation-and-adrs
description: Create or update durable technical documentation and architecture decision records. Use for public contracts, operating procedures, non-obvious constraints, and consequential technical decisions; domain vocabulary belongs to domain-modeling.
license: MIT
metadata:
  source: https://github.com/addyosmani/agent-skills/blob/0d52faf08da5a706616e7b1ae05226940c387ad1/skills/documentation-and-adrs/SKILL.md
  source_commit: 0d52faf08da5a706616e7b1ae05226940c387ad1
  upstream_license: MIT
---

# Documentation and ADRs

Document information that future engineers cannot cheaply reconstruct from code, configuration, tests, or generated references. Do not create documentation merely because code changed.

## Choose the right artifact

- **ADRs:** consequential technical decisions and their reasoning.
- **Specifications:** intended behavior and necessary design; use `feature-design` to resolve intent and its specification reference to draft the requested artifact. Keep execution plans separate.
- **Public contract documentation:** externally consumed API behavior, compatibility, errors, and examples.
- **Runbooks:** operational procedures, prerequisites, recovery, and verification.
- **README or contributor guidance:** entry points and non-obvious workflows.
- **Inline comments:** local constraints, provenance, or surprising trade-offs.
- **Domain glossary:** use `domain-modeling`, not this skill.

Match the repository's existing location, format, naming, and level of detail. Read nearby documents and the code they describe before editing. Never introduce a second documentation convention.

For substantial documentation, read [AUTHORING.md](./AUTHORING.md). Use layered, thorough explanations: orientation first, then complete relevant contracts, mechanisms, failure cases, examples, and evidence. A small correction does not require a handbook. For a portal use `service-documentation`; for agent-facing rules use `writing-for-agents` with `skill-creator` when changing skills.

For generating or synchronizing current-system docs from code, read [SOURCE-TO-DOCS.md](./SOURCE-TO-DOCS.md): source-backed page catalogues, vertical-path discovery, review baselines and dependent-page/visual updates. `/developer-docs` provides create, update, regenerate, improve and read-only audit modes. This is not a new wiki runtime or a specification inferred from implementation.

When available, use `tutorial-authoring` for hands-on learner journeys and `documentation-review` for requested substantive audits/critiques or diagnosis before documentation improvements. They own learner checkpoints and review diagnosis respectively, not a new renderer or evidence tracker. Do not add a second reviewer pass or execute a tutorial merely because a specialist is available.

## ADR gate

Create or offer an ADR for a consequential choice affecting architecture, contracts, quality attributes, dependencies, or operating constraints when preserving its reasoning will help future work. Consider scope of impact, non-obvious trade-offs, and reversal cost; being hard to reverse is a signal, not a mandatory condition.

Exclude routine implementation choices, formatting, and decisions already covered by an accepted record. Describe credible alternatives and their actual rejection reasons; do not invent alternatives or historical intent to justify current code. Use a smaller artifact when no significant decision needs preserving.

ADRs belong with the decision, not as retrospective justification for an unexplained implementation. Record the context, decision, reasons, rejected alternatives that may recur, and non-obvious consequences. Keep each fact in one authoritative place and link rather than duplicate.

If the repository has no ADR convention, use [ADR-FORMAT.md](./ADR-FORMAT.md).

## Consult and maintain decisions

- Before architecture-affecting work, consult relevant accepted ADRs and related contracts. An absent status is not proof of approval. Surface conflicts between source, intended contracts, and historical records; do not silently privilege one or rewrite history.
- Draft new records as proposed unless the decision has actually been approved. Follow repository status conventions; distinguish rejected, deprecated, and superseded decisions from active accepted ones.
- When a decision changes, link the replacement and replaced record in both directions and update an existing index. Preserve the original rationale; status/link updates do not authorize retrospective rewriting.
- Add confirmation criteria or revisit conditions only when useful: how implementation/compliance will be established, and which changing assumption warrants reconsideration. Do not turn an ADR into a mandatory implementation plan.
- Keep current scoped agent rules and temporary execution plans separate, linked to the ADR rather than replacing its context and trade-offs.

## Documentation rules

- Describe observable contracts, durable constraints, and the mechanisms needed to understand or safely change the system. Avoid file-by-file narration of cheaply reconstructible internals.
- Explain why; use relevant source-backed flows and examples to explain how without duplicating generated reference.
- Include commands only when they are part of a maintained user or operator workflow.
- Make prerequisites, destructive steps, rollback, and verification explicit in runbooks.
- Keep examples executable or clearly illustrative; remove stale examples rather than preserving them as history.
- Update affected explanations, examples, navigation, and dependent visuals with the relevant permanent behavior or public contract change. Use invoked audits for broader drift review; do not add background automation or CI as an authoring side effect.
- Do not document obvious code or throwaway prototypes as durable system behavior. Clearly label requested specifications and proposals rather than presenting intended behavior as implemented.

## Review

Before finishing, check the document against the implementation and repository convention. Confirm that links and named paths exist, public behavior is accurate, the intended audience can act on it, and no secret or environment-specific credential appears.
