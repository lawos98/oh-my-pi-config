---
name: deprecation-and-migration
description: "Plan or carry out a scoped replacement of an old API, library, feature, service, or data format. Use for 'replace the legacy system', 'plan a safe cutover', 'remove the old implementation', or 'migrate consumers without breaking them'. General migration safety complements framework-specific migration guidance; ordinary readability refactors use simplify."
license: MIT
metadata:
  source: https://github.com/addyosmani/agent-skills/blob/1401c8b8030e023baeebb31781a6653fe8e93026/skills/deprecation-and-migration/SKILL.md
  source_commit: 1401c8b8030e023baeebb31781a6653fe8e93026
  adaptation: OMP passive workflow; balanced change control; evidence-based recovery and clean cutover
---

# Deprecation and migration

Replace or retire a system without silently losing contracts, consumers, or data. Use normal natural-language intent; no command or external runtime is required.

## Scope and authority

- A clear, small implementation request can proceed within its named scope using the existing engineering workflow.
- A broad overhaul starts with a short ranked proposal: target, evidence, migration risk and smallest complete slice. Obtain agreement on the target before editing many files. A request for a plan or audit stays read-only.
- Planning does not authorize deployments, production access, destructive data operations, persistent Git operations, package installation, or tracker writes. Existing approval and failure-stop policies remain authoritative.

## Discover the real contract

1. Read the old implementation, proposed replacement, relevant callers, configuration, tests and governing documentation. Use LSP references when available; trace indirect registrations, serialization and persisted formats as well as direct references.
2. Map consumers and owners, required behavior, error/ordering/concurrency semantics, and old/new deployment combinations that must coexist. Distinguish observed consumers from unknown external usage. A local search is not proof of zero live usage.
3. State what changes and what must remain compatible. Record invariants such as identity, authorization, exact totals, uniqueness, ordering and data retention where relevant. Use framework-specific migration guidance rather than inventing version/API rules.

## Choose the smallest safe transition

- For controlled in-repository callers, prefer a clean cutover: migrate every affected caller and remove obsolete paths in the same coherent change.
- Use staged coexistence only when real consumer or rolling-deployment constraints require it. Name its owner, compatibility rules and removal condition; do not introduce speculative shims, adapters, feature flags or indefinite dual maintenance.
- For persisted-data changes, assess whether old and new code can read and write each intermediate shape. Use additive expansion, bounded backfill, switching reads/writes, and final contraction when coexistence is necessary. Additive changes can still lock storage or exceed resource limits; do not label them universally safe.
- Define backfill batching, resumability, failure handling, concurrent writes and consistency checks when relevant. Do not drop the old shape merely because the new field exists.
- Classify recovery honestly: reversible code/configuration, data-restorable, forward-fix/compensation, or irreversible. Reverting a deployment does not restore deleted or transformed data. Do not promise a down migration when information loss makes it impossible.

## Plan or implement

Provide a dependency-ordered plan containing the affected consumers/data, transition states, acceptance evidence, stop conditions, recovery strategy and old-path removal criteria. Keep it in the conversation/native todo unless a maintained artifact is requested.

After implementation is authorized, complete the selected slice end to end. Preserve unrelated user changes, migrate all affected consumers in scope, and update existing contracts/tests/docs where their behavior changes. Use the established framework, database and deployment conventions. Do not connect to live infrastructure just to gather migration evidence without permission.

## Removal and verification

Before deleting the old path, identify evidence that each known consumer has moved and that old readers/writers are no longer required. Report unknown external or live usage instead of assuming it is zero. Remove obsolete code, configuration, tests and notices made unnecessary by the cutover; retain genuine safety/history records required by repository policy.

Choose verification proportionally under the active execution policy. Do not run a test/build/format sweep after every consumer or phase. A failed authorized check stops validation and automatic repair; report its exact command and actual result. Distinguish plans, edits, static evidence, runtime observations and checks not run.

## Completion

Every known in-scope consumer and persisted contract has a migration decision; the selected behavior is complete; recovery limitations and unknown usage are explicit; and obsolete paths are removed or have an approved bounded reason to remain. No claim of production readiness or rollback safety rests on a source search alone.

## Source

Adapted from Addy Osmani's deprecation-and-migration skill at the pinned revision. See LICENSE and provenance.json. The OMP adaptation removes universal production/rollback assertions, default compatibility shims, unapproved operations, and repeated verification gates.
