---
name: feature-design
description: Design features, substantial solutions, and behavior changes through evidence-backed architecture assessment and brainstorming. Use when boundaries, data and failure flows, consistency, concurrency, maintainability, requirements, or competing approaches need clarification before implementation.
license: MIT
metadata:
  domain: workflow
  role: specialist
  scope: design
  output-format: conversation
---

# Feature Design

Reach shared understanding before implementation when the requested behavior is materially ambiguous. Do not force a design workshop onto a small request whose intent and constraints are already clear.

## 1. Establish evidence

Inspect the repository before questioning the user. Read the relevant implementation, callers, configuration, tests, `CONTEXT.md` or `CONTEXT-MAP.md`, and applicable ADRs.

Facts are the agent's responsibility. Ask the user only for intent, priorities, preferences, trade-offs, and decisions that evidence cannot settle.

## 2. Map the decision tree

Treat the design as a dependency tree. The **frontier** is every unresolved decision whose prerequisites are already settled.

Cover only branches required by the feature:

- problem, actors, and intended outcome;
- current behavior and desired behavior;
- scope and explicit non-goals;
- domain vocabulary and invariants;
- user-visible flows and state transitions;
- failure, recovery, authorization, and data boundaries;
- compatibility, operational, and performance constraints;
- the smallest useful implementation slice;
- observable acceptance criteria.

### Substantial solution assessment

For work spanning components, persisted contracts, asynchronous flows or consequential operational behavior, assess the architecture before implementation. Keep this proportional to the change; a localized feature does not require a system redesign.

- Identify ownership and boundaries: the responsible modules/services, public contracts, trust boundaries and external systems. Reuse existing seams before proposing new services or layers.
- Trace data and control flow through the important success and failure paths. Identify persisted state, schema compatibility, error ownership, partial completion and recovery.
- State concurrency and consistency requirements: competing writers, ordering, atomicity, transaction boundaries, duplicate delivery, idempotency and cancellation where relevant. Do not add queues, retries, locks or distributed transactions without a demonstrated requirement.
- Compare meaningful alternatives only where a material choice exists, including the smallest change to the current design. Explain trade-offs in correctness, compatibility, failure handling, operating cost and six-month maintainability; avoid straw alternatives or a fixed option quota.
- Choose the simplest viable design that satisfies all acceptance criteria. Name its limits and any unresolved evidence rather than creating speculative abstractions or silently narrowing scope.
- Map the decision to the affected callers, data contracts and focused tests. Separate observed facts from assumptions that still need resolution.

Fold this assessment into the existing decision and confirmation flow. It does not mandate another review agent, architecture score, check run, approval round for already-confirmed choices, or unrelated repository redesign.

## 3. Ask frontier rounds

Ask the whole current frontier in one round. Use structured choices when they represent the real options, recommend one answer for every question, and explain the material trade-off concisely.

Do not ask a question whose answer depends on another unresolved question in the same round. Recompute the frontier after each response and continue until no material branch remains silently assumed.

For a complex or inherently visual decision, one focused question is acceptable. When prose cannot settle a concrete logic, state-model, or UI uncertainty, use the `prototype` skill under its approval and cleanup rules.

When discussion changes project-specific terminology, use `domain-modeling` and update the applicable glossary as terms become settled.

## 4. Confirm the design

Summarize:

- the problem and desired outcome;
- chosen behavior and rejected alternatives;
- scope and non-goals;
- important invariants and failure behavior;
- component and data ownership, material concurrency/consistency decisions, and why the simplest viable design was chosen;
- the smallest useful slice;
- acceptance criteria;
- unresolved risks, if any.

Ask the user to confirm that this is the shared understanding. Do not begin implementation while a material decision remains open.

## 5. Create only requested artifacts

The default output is the confirmed conversation. Create a specification, Jira issue, implementation plan, ADR, or repository document only when the user requests that artifact.

When a specification is requested, match the repository's existing convention. If none exists, include only the sections needed to preserve the confirmed behavior: outcome, scope, requirements, failure behavior, acceptance criteria, and non-goals. Do not add placeholders or implementation detail disguised as requirements.

When implementation follows, hand the confirmed decisions to the normal OMP implementation workflow; this skill does not create a second implementation process.
