# Behavior plus necessary design

Use when the user requests a specification. Follow the repository's existing format, location, terminology, and approval process. A specification describes intended behavior; it is not automatically an implementation request or an approved ADR.

## Establish the baseline

Inspect relevant current behavior, callers, schemas, tests, constraints, and accepted decisions. Separate the baseline from the requested change. Discover facts from available sources; ask the user one unresolved intent or trade-off question at a time. Do not turn implementation patterns into invented requirements.

Use a short orientation followed by precise relevant detail. Cover the entire requested scope. Select only useful sections from the fallback below; omit inapplicable sections rather than leaving placeholders.

## Proportional fallback structure

- **Outcome and scope:** the problem, actors, intended result, and explicit non-goals.
- **Current versus intended behavior:** what exists, what changes, and what remains compatible; identify the evidence for the baseline.
- **Requirements:** observable rules and their conditions, including input/output contracts, validation, authorization, defaults, and errors where relevant. Preserve normative strength; do not apply prose simplification to normative requirements.
- **State and failure behavior:** transitions, persistence boundaries, ordering, duplicate handling, partial completion, cancellation, recovery, and concurrency where material. State what is not guaranteed instead of inventing guarantees.
- **Necessary design:** component/data ownership, public and internal boundaries, interactions, contract changes, compatibility/migration constraints, and consequential design choices. Link an ADR for significant trade-offs. Keep incidental file names and task sequencing out of requirements.
- **Acceptance scenarios:** concrete preconditions, action/input, and expected observable outcomes. Include meaningful rejected, boundary, and failure cases, not only happy paths. Use requirement IDs when they improve traceability; do not impose a numbering scheme over repository conventions.
- **Open decisions and assumptions:** name each unresolved issue, its impact, and what evidence or decision resolves it. Do not present an unresolved choice as approved or fabricate an answer to fill a section.

## Separate durable intent from execution

Keep the behavioral contract and necessary design together, with clear headings separating requirements from design rationale. A file-by-file execution plan is a separately requested artifact, not a compulsory specification section. Link it rather than copying requirements into it.

A specification can document open questions, but an implementation handoff is not ready while a material behavior or safety decision remains unresolved. Finish all supported sections and explicitly identify the blocker. Do not implement merely because a specification was requested.

For diagrams in a handbook, follow `service-documentation`; for a standalone design discussion, use the existing visual conventions. Label proposed-state diagrams so readers cannot mistake them for the running system. Keep acceptance scenarios and requirements understandable without opening an interactive viewer.

## Review and handoff

Review the specification against the confirmed intent: every in-scope behavior has a defined outcome or a visible unresolved issue; acceptance scenarios exercise real boundaries; design does not silently add requirements; non-goals and compatibility are explicit where they affect the decision.

Use `documentation-and-adrs` for durable writing quality and consequential decisions. Use `spec-to-code-compliance` when asked to compare the specification with implementation; report that comparison separately from specification approval or passing runtime checks. Verification follows the shared execution policy, not an automatic test suite or model-review loop.
