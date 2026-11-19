---
name: tutorial-authoring
description: Write or improve hands-on developer tutorials and service onboarding journeys with a reproducible start, one concrete outcome, observable checkpoints, recovery and safe reset. Use when readers must learn by doing. Not ordinary setup reference, API inventories, architecture explanation alone, operational incident runbooks or automated tutorial execution.
license: CC-BY-SA-4.0
metadata:
  source: https://github.com/jrajasekera/diataxis-documentation/tree/7345aa8ae02f7aa5e26eaf071e5d4b5c2dbb3de2
  source_commit: 7345aa8ae02f7aa5e26eaf071e5d4b5c2dbb3de2
  adaptation: OMP learner-journey authoring; no runtime, mandatory execution or retry loops
---

# Tutorial authoring

Help a specific reader complete one meaningful learning task, not merely read an inventory of components. Use `documentation-and-adrs` for source evidence and writing conventions, and `service-documentation` for portal/media delivery. This skill owns the learner journey, not another site or synchronization tracker.

## Establish the learner contract

Inspect repository instructions, existing setup docs, manifests/scripts, local profiles, sanitized examples, relevant handlers/actions and tests. Infer prerequisites and audience from that evidence where possible; ask through the native decision form only when an unresolved choice materially changes the journey.

Define in working context:

- Reader role, prior knowledge and concrete task.
- Supported tool/service versions and a reproducible starting state.
- Required local dependencies, safe data, access and environment boundaries.
- One visible final outcome and what it does and does not prove.
- Actions that modify state, plus safe repetition/reset and any cleanup limits.

Choose the repository's existing safe local/demo workflow. A tutorial request does not authorize installs, production access, external account creation, deployment or destructive operations. Do not turn an experienced-user lookup/how-to into a mandatory beginner tutorial.

## Build one grounded path

Use this page shape as a guide, not compulsory empty headings:

1. **Outcome:** what the learner will accomplish, with a brief concrete motivation and links to exact reference when needed.
2. **Before starting:** necessary knowledge, versions, configuration names, access and sanitized seed state. Put prerequisites before the first action, not halfway through the path.
3. **Readiness:** a supported non-destructive way to recognize the expected starting state.
4. **Actions and checkpoints:** give the exact sourced action, the observable result, what to notice and what that observation proves. Add nearby recovery for likely evidenced failures. Keep one successful route; link alternatives and long explanations elsewhere.
5. **Final proof:** a visible outcome that distinguishes success from merely starting a process or receiving an acknowledgement. For asynchronous work, distinguish accepted/scheduled/running/completed only where the service exposes that distinction.
6. **Reset and next steps:** identify created resources and a safe supported reset so the task can be repeated; link to deeper explanation, how-to guidance and authoritative reference.

For a service journey, connect the learner's request or event to the actual resulting state/effect. Preserve validation, authorization and background-processing boundaries that affect the outcome. Do not infer a runnable scenario from a diagram, fixture or plausible sample request.

Use representative safe inputs and only paths, flags, variables and defaults supported by inspected evidence. Do not publish invented timings, health endpoints, credentials, owner contacts or migration/rollback commands. Never read real secret values to populate an example. Explain what remains unsupported rather than filling the page with placeholders.

## Keep outcomes honest

- Record whether each important expected result comes from an observed run, an inspected contract/test assertion or an explicitly labelled illustration. Never present authored output as terminal capture or claim a clean-start walkthrough occurred when it did not.
- Where execution is unavailable or unauthorized, complete source-supported instructions and state that the walkthrough was not exercised, including the specific environment/evidence limitation. Do not invent completion evidence.
- Keep warnings before risky actions. Offer only evidenced safe recovery/reset steps; do not promise reversibility, idempotence, rollback or data restoration without support.
- Show the signal the learner should notice. A bare successful exit, HTTP acceptance or running process may not prove the intended business outcome.
- Keep conceptual detail reachable, but do not interrupt every action with a subsystem essay. Preserve intentional secondary reference/troubleshooting sections when they help the journey.

## Maintain and verify within existing policy

Use the existing source-to-section map and reviewed baseline from `documentation-and-adrs` for dependencies, examples and editable visuals. Do not create a parallel tutorial manifest. A changed request schema, local profile, action rule or initialization path may invalidate a learner step even if its destination page did not change.

Perform the task's single correctness self-review. An end-to-end walkthrough is useful only with an available approved environment and within the shared check allowance: follow only the written steps, compare observations with checkpoints, record hidden prerequisites and verify the final outcome and safe reset. Inspect commands before running them. This skill grants no extra checks, installation, production access, automatic cleanups, mandatory test suite, formatter or repair loop.

If the request is read-only audit, return findings only: do not execute the journey, write a draft, render media or reset resources. Use `documentation-review` when available for a requested substantive critique, not an automatic second reviewer or reader-model loop.

Deliver the real page and navigation changes when authorized. Report source revision/scope, observed versus contract-derived examples, actual walkthrough/check outcome, unrun steps and unresolved gaps separately. A passing docs build or reader-model answer does not establish that the service journey works.

## Attribution and adaptations

Adapted from [jrajasekera/diataxis-documentation](https://github.com/jrajasekera/diataxis-documentation/tree/7345aa8ae02f7aa5e26eaf071e5d4b5c2dbb3de2), especially its tutorial template and document-testing guidance. That work operationalizes [Diátaxis by Daniele Procida](https://diataxis.fr/), [source repository](https://github.com/evildmp/diataxis-documentation-framework).

This adaptation is licensed CC BY-SA 4.0. Preserve [LICENSE.md](LICENSE.md) and [provenance.json](provenance.json). No endorsement is implied. Changes replace broad documentation classification with a narrow learner-journey skill, preserve OMP evidence and approval rules, remove fictional runnable-example claims, compulsory execution and repeated checks, and exclude all upstream helpers/installers. This file's license does not declare a license for the whole OMP setup or automatically assign a license to independently authored service documentation.
