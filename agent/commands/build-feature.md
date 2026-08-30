---
name: build-feature
description: Implement a complete feature with the smallest maintainable architecture and end-to-end verification.
---

Implement the requested feature end to end. Do not return only architecture suggestions, a speculative roadmap, or a partial scaffold.

1. Read and apply `software-architecture`, `clean-code`, and the repository's relevant language, framework, database, API, security, and testing skills.
2. Inspect the current implementation, callers, consumers, configuration, tests, persisted formats, and external contracts. Use LSP references before changing exported symbols.
3. Trace the real execution and data path. Identify the source of truth, invariants, trust boundaries, failure semantics, concurrency, compatibility, and ownership.
4. Reuse an existing implementation, standard library, platform feature, or installed dependency before writing new code. Do not add a second pattern for an existing concern.
5. Implement the smallest complete vertical change. Give each rule one owner; consolidate duplicated behavior only when its contract and failure semantics are genuinely the same.
6. Do not add one-implementation interfaces, speculative factories, generic utility layers, placeholder compatibility paths, or configuration for values that do not vary.
7. Validate untrusted input at the boundary. Preserve structured errors, authorization, idempotency, transaction/consistency behavior, timeouts, cancellation, and data compatibility where relevant.
8. Migrate every affected caller and remove the obsolete code, alias, comment, and branch. Do not leave parallel old and new paths.
9. Add or update tests only for new or changed observable contracts and plausible regressions. Run LSP diagnostics on edited source and the narrowest applicable project checks, then exercise the changed runtime path.
10. Report the implementation and actual verification evidence. Do not append generic improvement suggestions.

Ask only when a material product or architecture choice cannot be resolved from the repository. Do not commit, push, change branches, or modify unrelated code.
