---
name: documentation-review
description: Review technical documentation for source accuracy, reader usability, example safety and appropriate structure; diagnose improvements before editing. Use for documentation audits, substantive page critiques or requested documentation improvements. Not general code review, trivial grammar fixes, agent-instruction audits or automatic second reviews.
license: CC-BY-4.0
metadata:
  adaptation: OMP diagnosis-first documentation review; read-only by default; no upstream commands or runtime
---

# Documentation review

Review whether a reader can trust and use the requested documentation. This is a specialist within the existing documentation workflow, not a second authoring framework. Read [provenance.json](provenance.json) and preserve [LICENSE.md](LICENSE.md) when redistributing this adaptation.

## Scope and permission

- A review, critique, strategy request or `/developer-docs audit` is read-only: return findings in chat. Do not edit docs, create a report file, build, render, install, post a review or run application code.
- An explicit improve/fix/edit request permits scoped documentation edits. It does not permit application repairs, platform migrations, commits, pushes or publication. A weak structure justifies a rewrite recommendation, not unrequested broad edits.
- Use repository evidence before asking questions. Ask only about unresolved consequential intent using the native decision form. Do not require a questionnaire or approval of each ordinary editorial correction.
- Do not spawn reviewer agents, run reader-model loops or add a second correctness review automatically. Use this rubric within the task's existing single review. All checks follow the shared execution policy.

## Diagnose before correcting

1. Identify the requested pages, reader, task and known prerequisites. Read the full relevant page sections, their canonical references and source evidence; a diff alone may omit essential context.
2. Identify the primary page job: explanation, tutorial/task, reference, troubleshooting, migration or decision guidance. A README/index or cohesive page may contain legitimate secondary reference or troubleshooting sections; evaluate those by their own job rather than forcing page splits.
3. Check in order: intent and audience; information shape and prerequisites; mechanisms and terminology; actionable steps and success criteria; example realism/safety; then repetition and wording. Do not polish a page whose structure prevents the reader from accomplishing its task.
4. Choose the smallest intervention: local maintenance for sound content; targeted improvement for weak framing/order/examples; scoped rewrite only when the page shape defeats its job; a proposed split only for unrelated competing jobs. Preserve accurate content, manual notes, historical rationale, paths and anchors.

## Check technical claims against authority

For consequential claims, use: **claim → authoritative evidence → discrepancy → reader impact → correction**.

- Follow source symbols, validation and error mapping, schemas, configuration and callers/consumers as relevant. Use available LSP/GitNexus for navigation but verify indexed findings against current source. Tests express expectations unless actually exercised; configuration is not proof of deployed behavior.
- Inspect parameters, required/optional fields, defaults, units, authentication/authorization boundaries, errors and side effects when those claims are in scope. A success response may only acknowledge deferred work. Distinguish acceptance, persistence, scheduling and completion.
- For event documentation, check producer/consumer ownership, payload meaning and evidenced handling of duplicates, order, replay and failures. Do not infer guarantees from broker names or from AsyncAPI rendering. State what is unknown instead of manufacturing completeness.
- Inspect examples as actions a reader may copy: paths and flags must exist; values must be sanitized; prerequisites and safe target environment must be clear; destructive steps need warnings before the action and evidenced recovery. Never invent a rollback command.
- When an example and schema appear inconsistent, identify the concrete field/type/constraint and evidence. Do not claim payload validation or compatibility testing unless exercised with the relevant approved tooling.
- Distinguish obsolete descriptions from implementation defects and intended-contract conflicts. Use `spec-to-code-compliance` for the bounded comparison; do not silently rewrite a promise to excuse a bug or accepted ADR history to justify current code.

## Report or improve

Return only actionable findings, ordered by reader risk: unsafe instructions or broken delivery, incorrect behavior/examples, missing prerequisites or blocked tasks, then structural/style problems with demonstrated impact. Each finding includes severity, page/section or verified line, evidence, consequence and a concrete correction. Do not invent line numbers.

Do not flag unsupported theoretical concerns, arbitrary style preferences, missing features outside scope or unchanged pre-existing defects as regressions. Note material out-of-scope issues separately without fixing them. If there are no findings, state that with the inspected scope and evidence limits; do not imply full-service validation.

When edits are requested, follow `documentation-and-adrs` for authoring/source-to-section synchronization, `tutorial-authoring` for learner journeys when available, and `service-documentation` for portal/media delivery. Apply the diagnosis inside the authorized scope and update affected links/examples/visuals together. Do not automatically escalate a local improvement to whole-service regeneration.

Report source inspection, actual checks, unrun checks and unreviewed scope separately. Successful rendering does not prove technical accuracy, and a reader model's answer does not prove factual correctness.

## Sources and adaptations

Adapted from Storybook's `docs-review` (MIT) and Cloudflare's documentation-review guidance (CC BY 4.0 conservatively for prose), at immutable revisions in provenance. The adaptation adds OMP routing, read-only review defaults, source/contract distinctions and shared execution boundaries. It removes Storybook-specific MDX rules, package-manager commands, automatic fixes/commits, GitHub review posting and iterative validation. No upstream scripts, agents, MCPs or network services are installed. No endorsement is implied.
