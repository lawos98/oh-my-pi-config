---
name: software-architecture
description: "Use when designing, implementing, reviewing, or refactoring software structure, responsibilities, encapsulation, module or service boundaries, domain and infrastructure separation, data flow, public APIs, persistence, dependencies, or cross-cutting behavior."
---

# Software Architecture

Design the smallest architecture that satisfies the current requirement and remains easy to change. When the user asks to build or change software, implement the architecture; do not stop at a suggestion report unless the user asks for design only.

## Start with the running system

- Trace the relevant execution path end to end: entry point, callers, domain behavior, I/O, persistence, external systems, errors, and tests.
- Identify the current source of truth, public contracts, persisted formats, ownership boundaries, and deployment constraints.
- Reuse the repository's established architecture and vocabulary. Do not create a second pattern for the same concern.
- Preserve public API and persisted-data compatibility unless the request explicitly changes them.

## Choose the lightest boundary that works

Use this order:

1. Existing implementation or helper.
2. Standard library or language feature.
3. Framework or platform capability already used by the project.
4. Installed dependency already solving the problem.
5. A small local function or module.
6. A new abstraction only when a current second implementation, variation, or replaceable boundary requires it.

KISS, DRY, SOLID, size metrics, and complexity metrics are decision aids, not quotas. Repository conventions and observable behavior win. Do not split, extract, or introduce a pattern only to satisfy a line, argument, branch, coverage, dependency, or duplication count.

## Own each concept once

- Give every invariant, state transition, mapping, and business rule one authoritative owner.
- DRY means one owner for knowledge and policy, not one representation of similar syntax.
- Reuse or move a shared rule only when callers require the same behavior, invariant, and failure semantics. Two short blocks are better than a generic abstraction that hides different reasons to change.
- Avoid catch-all `utils`, `common`, `manager`, `handler`, `processor`, and base classes. Name modules after the domain concept they own.
- Keep exported surfaces small. A likely change should have one obvious home.

## Write code that explains itself

- Use specific, searchable domain names. Function names describe the observable outcome; names for commands and mutations make side effects clear.
- Keep a function cohesive and its success path easy to follow. Use guard clauses for exceptional cases, but do not fragment a clear flow into tiny functions to meet a size target.
- Keep one readable level of abstraction within a function. Extract a helper only when its name exposes a real concept or its contract is independently useful.
- Keep parameters explicit. Group them only when the group is a real domain concept or enforces an invariant; do not create a parameter object to satisfy an argument count.
- Prefer direct control flow over clever expressions, boolean-flag matrices, hidden callbacks, or comments that narrate mechanics.
- Comments explain reasons, constraints, provenance, or surprising tradeoffs. Delete stale comments and rewrite code that needs a comment merely to explain what it does.

## Separate policy from mechanism

- Keep business policy independent from transport, UI, database, framework, and vendor details when that separation protects a real rule or reuse boundary.
- Map request, document, SDK, and vendor representations at the edge. Do not let storage schemas or generated client types become the domain model by convenience.
- Encapsulate mutable state, representation, and infrastructure details behind the smallest operations that preserve the owner's invariants. Expose behavior and stable domain vocabulary rather than writable fields or raw persistence objects.
- Keep I/O and side effects at explicit edges. Construct infrastructure dependencies at the composition boundary instead of hiding them inside domain behavior.
- Adapters translate, invoke I/O, and persist; they do not own business decisions. Do not create pass-through layers or one-implementation interfaces for trivial CRUD or a fixed dependency.
- Dependencies point toward stable policy only across a real boundary. A direct concrete dependency is simpler when no replacement, isolation, or independent contract exists.

## Model behavior and data explicitly

- Make invalid states difficult to represent. Validate untrusted input once at the boundary, then use validated types internally.
- Define state ownership, lifecycle, concurrency, ordering, consistency, transaction, idempotency, timeout, cancellation, and retry behavior where relevant.
- Make failure semantics part of the contract. Preserve original causes, avoid silent fallback, and never expose secrets or internal details through public errors.
- For persistence changes, review query shape, indexes, uniqueness, nullability, migrations, rollback, and compatibility with existing data.
- For APIs, define request validation, authorization, structured errors, duplicate-request behavior, and consumer compatibility.

## Non-functional constraints

Address only constraints relevant to the actual path:

- **Security:** trust boundaries, least authority, secret handling, injection, data exposure.
- **Performance:** complexity, allocation, I/O count, batching, caching only with a demonstrated reuse pattern, and backpressure where applicable.
- **Reliability:** partial failure, atomicity, cleanup, restart behavior, and bounded retries.
- **Operability:** use existing logging, metrics, and tracing conventions; do not add a telemetry framework for one change.
- **Accessibility and UX:** for user-facing work, preserve semantic structure, keyboard use, responsive behavior, clear states, and consistent language.

## Implement as a clean cutover

- Build the smallest complete vertical change through every affected layer.
- Update every caller and consumer. Remove obsolete branches, aliases, wrappers, comments, and compatibility paths made unnecessary by the change.
- Add or update tests only for observable contracts, invariants, boundaries, transitions, and real failure modes.
- Run LSP diagnostics on edited source and the narrowest applicable project checks. Exercise the changed runtime path.

## Avoid architecture theater

Do not add speculative extension points, empty layers, one-implementation interfaces, factories for one product, generic event buses for direct calls, microservices without an independent deployment need, configuration for constants that do not vary, or comments that compensate for unclear code.

Do not finish with a list of possible improvements when the user requested implementation. Complete the requested work, verify it, and report only the changes, evidence, and remaining real constraints.
