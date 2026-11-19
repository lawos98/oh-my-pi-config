# Layered technical documentation

Use this reference for substantial documentation creation or revision. Preserve the repository's conventions and cover the requested scope completely; a small README correction does not require a handbook.

## Start from the reader's task

Identify the audience, question, scope, and authoritative source before drafting. Inspect available evidence rather than asking the user for facts the repository can provide. Ask only about unresolved intent or consequential trade-offs.

Choose the form that serves the reader:

- A tutorial guides learning through one concrete, safe path with expected outcomes.
- A how-to guide solves a task, including prerequisites, unsafe steps, recovery, and verification where relevant.
- Reference provides exact contracts, fields, constraints, defaults, and errors, following the authoritative schema or implementation structure.
- Explanation develops understanding of ownership, mechanisms, reasoning, and trade-offs.

These distinctions are informed by [Diátaxis](https://diataxis.fr/). Use them to improve real pages, not to impose four directories, empty sections, or a new approval ceremony.

## Layer the detail

Lead with the answer and the condition that changes it. Give newcomers an orientation and a route into mechanisms; keep exact reference directly reachable without completing a lesson. Link to one canonical explanation instead of duplicating contracts across tours, troubleshooting, and examples.

For an in-scope service handbook, cover relevant ownership and vocabulary, setup, architecture and flows, API/message contracts, data and consistency, development, operations, and troubleshooting. Make a coverage map in working context. Identify unavailable evidence rather than silently dropping a component or filling gaps with generic text.

Explain the mechanism at the level needed to change or operate it safely. Include important branches: unmatched inputs, rejection, empty results, duplicate or out-of-order work, partial completion, and recovery. Include only branches supported by evidence or explicitly specified as intended behavior; do not invent retry, atomicity, or delivery guarantees.

Use concrete examples to resolve ambiguity. Preserve identifiers, units, qualifiers, and uncertainty when revising prose. Examples are either supported contracts or clearly labelled illustrations; neither a plausible payload nor a test fixture proves deployed behavior.

## Keep evidence and intent distinct

Use the repository's existing evidence convention. When none exists, distinguish:

- **Implementation:** behavior supported by inspected source under stated conditions.
- **Configuration:** declared settings, not necessarily effective deployed values.
- **Test expectation:** an inspected assertion, not an executed passing result.
- **Historical decision:** recorded reasoning, not proof of current enforcement.
- **Illustration:** an authored scenario or visual, not a measured trace.
- **Inference:** a reasoned but unexercised consequence.
- **Proposal or specification:** intended behavior, not an implemented guarantee.

Source-link consequential claims to actual paths/symbols or verified revision permalinks. Record the inspected revision or working-tree scope using repository conventions. Never invent line anchors or infer historical intent from a recurring code pattern. Keep answer-changing limitations beside the affected claim, not only on a distant caveats page.

When sources disagree, describe the discrepancy and its consequence. Do not rewrite an intended contract to excuse a defect, or rewrite an accepted ADR to pretend the current code was always the decision. Use `spec-to-code-compliance` for a requested or necessary bounded comparison; it does not authorize application fixes.

## Maintain and verify

Update affected explanations, examples, navigation, and dependent visuals with the relevant behavior change. Preserve stable paths and anchors where possible. Use `/developer-docs audit` for an invoked read-only review of current-system documentation, not a background job. Do not add CI, drift services, or a checker as a side effect of authoring.

Review source accuracy, scope coverage, links, examples, privacy, and reader usability. For site and media work, follow `service-documentation` and its [media contract](../service-documentation/references/media.md). Report source inspection, exercised checks, and remaining uncertainty separately. A successful build is not proof that an explanation or service behavior is correct.
