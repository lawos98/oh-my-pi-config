---
name: spec-to-code-compliance
description: "Compare documented requirements, API contracts, design notes, or acceptance criteria with the implementation. Use for 'check the code matches the spec', 'verify the promised behavior', or 'find gaps between this design and the code'. Report requirement-level evidence and unchecked scope; do not replace general bug review or invent requirements from the implementation."
license: CC-BY-SA-4.0
metadata:
  source: https://github.com/trailofbits/skills/blob/d1f1575cff97816e5cc08af66cd2506099c681d3/plugins/spec-to-code-compliance/skills/spec-to-code-compliance/SKILL.md
  source_commit: d1f1575cff97816e5cc08af66cd2506099c681d3
  adaptation: OMP passive review; bounded coverage; no plugin command, scripts or compulsory verifier pipeline
---

# Requirements-to-code compliance

Check what the documents require against what the code enforces. A mismatch may need a code fix, a document correction, or clarification; do not assume the code is wrong merely because prose differs.

## Scope and authority

1. Identify the user-named documents, relevant implementation and intended version. Establish which documents are authoritative and distinguish mandatory requirements from recommendations, options, examples and future roadmap items. Resolve authority from evidence; ask only if a material conflict remains.
   - Distinguish current-system descriptions, intended specifications, proposed changes, and historical ADRs. A proposed specification is not automatically approved; a historical decision is not proof of current enforcement. For a requested new specification use `feature-design`; for ADR lifecycle and durable documentation use `documentation-and-adrs`. Report an unresolved authority conflict rather than silently rewriting either side.
2. If there is no statement of intended behavior, report that prerequisite. Do not infer a requirement from code and then compare the code against itself. Use general code review instead when the user wants bug hunting without a specification.
3. This review is read-only. Report findings before any proposed implementation. Explicitly authorized small fixes can use the normal engineering workflow; a broad overhaul needs agreement on a target and boundaries first. Do not create report trees, tickets, rules, commits, tools or commands by default.

## Evidence-led comparison

1. Break the selected scope into individually checkable requirements. Record each requirement's source location, exact condition/strength, and the behavior that would satisfy or contradict it.
2. Trace actual execution paths: entry points, registrations, callers, enforcement, callees, persistence and error paths. Use LSP for available symbol intelligence. In services, authorization may live in route registration/middleware and uniqueness in a database constraint, not the handler.
3. Assign an evidence-backed outcome:
   - **Implemented:** enforcement establishes the required behavior on the inspected in-scope paths.
   - **Partial:** some reachable paths enforce it, while others do not.
   - **Contradicted:** the code produces behavior the requirement rules out.
   - **Stronger than specified:** an additional enforced restriction or invariant lacks documentation.
   - **Absent in searched scope:** no enforcement was found after the relevant paths and mechanisms were inspected; include search bounds and patterns.
   - **Undecidable:** ambiguity, missing code/configuration, unavailable evidence or unexamined paths prevent a conclusion.
4. For every potential gap, inspect plausible alternative enforcement before reporting it. A similarly named function is not evidence, a test assertion is not proof of runtime enforcement, and a failed text search is not proof of absence.
5. Look in the reverse direction too: note consequential behavior in the inspected code that the documents do not mention. This is a bounded observation, not a claim to have found every undocumented behavior.

## Coverage and consequence

Track every in-scope requirement as checked, partially checked or not checked. Identify unreadable documents and unverified paths. Use existing read-only scouts only for genuinely independent areas; large scope does not justify pretending one context inspected every call chain. Do not claim independent refutation unless it actually occurred, and do not add a compulsory second review loop.

Severity follows concrete impact and reachability, not wording similarity or the number of reviewers. A different mechanism that satisfies the requirement is not a behavior defect. An undocumented restriction can affect compatibility and is not automatically harmless. For uncertain consequences, state the missing precondition rather than inventing an attack or impact figure.

## Report

Lead with actionable discrepancies, then provide a compact requirement table: source, required behavior, outcome, enforcement/path evidence and uncertainty. Separate code defects, document drift, ambiguous requirements, and recommendations. Include checked/not-checked scope and actual checks performed. If there is no supported discrepancy, say so; do not manufacture one to fill a quota.

Do not execute checks merely because this skill is a review. Follow OMP's shared execution policy, including its bounded recovery allowance, for any authorized check. Static reasoning, edits and runtime observations are different evidence.

## Completion

Every named requirement has an outcome or explicit coverage limitation, each reported discrepancy has source/path evidence and a defensible consequence, and the report does not promise the excluded upstream workflow's automation or coverage guarantees.

## Attribution and license

Adapted from Trail of Bits' spec-to-code-compliance skill, DIVERGENCE_RUBRIC.md and DOMAIN_NOTES.md at the immutable revision above. Modified for OMP's tools, natural-language routing, bounded read-only scope, balanced control and execution policy. No upstream scripts, commands, agents, report generator or runtime are included; no Trail of Bits endorsement is implied.

This adapted skill is licensed under Creative Commons Attribution-ShareAlike 4.0 International: https://creativecommons.org/licenses/by-sa/4.0/ . See LICENSE and provenance.json. Keep its attribution and share-alike terms when distributing an adaptation.
