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
- **Public contract documentation:** externally consumed API behavior, compatibility, errors, and examples.
- **Runbooks:** operational procedures, prerequisites, recovery, and verification.
- **README or contributor guidance:** entry points and non-obvious workflows.
- **Inline comments:** local constraints, provenance, or surprising trade-offs.
- **Domain glossary:** use `domain-modeling`, not this skill.

Match the repository's existing location, format, naming, and level of detail. Read nearby documents and the code they describe before editing. Never introduce a second documentation convention.

## ADR gate

Create or offer an ADR only when all three conditions hold:

1. **Hard to reverse:** changing the decision later has meaningful cost.
2. **Surprising without context:** code and configuration do not explain why this choice exists.
3. **Real trade-off:** credible alternatives were considered and rejected for specific reasons.

If any condition is absent, use a smaller artifact or no documentation.

ADRs belong with the decision, not as retrospective justification for an unexplained implementation. Record the context, decision, reasons, rejected alternatives that may recur, and non-obvious consequences. Keep each fact in one authoritative place and link rather than duplicate.

If the repository has no ADR convention, use [ADR-FORMAT.md](./ADR-FORMAT.md).

## Documentation rules

- Describe observable contracts and durable constraints, not current internal mechanics.
- Explain why; let clear code and generated configuration show what.
- Include commands only when they are part of a maintained user or operator workflow.
- Make prerequisites, destructive steps, rollback, and verification explicit in runbooks.
- Keep examples executable or clearly illustrative; remove stale examples rather than preserving them as history.
- Update affected existing documentation during a permanent feature or public contract change.
- Do not document throwaway prototypes, obvious code, or speculative future behavior.

## Review

Before finishing, check the document against the implementation and repository convention. Confirm that links and named paths exist, public behavior is accurate, the intended audience can act on it, and no secret or environment-specific credential appears.
