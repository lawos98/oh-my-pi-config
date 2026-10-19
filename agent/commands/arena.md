---
name: arena
description: Use Arena to compare approaches for a selected command and prompt, then follow that command's execution boundaries.
argument-hint: "<command> <prompt and command arguments>"
---

Run Arena for this request: $ARGUMENTS

## Resolve the request

Treat the first whitespace-delimited token as the selected OMP command name, with or without a leading `/`. Treat everything remaining as its prompt and arguments, preserving it verbatim. This is not a shell command: never execute, evaluate or interpolate the input as shell code.

Discover the selected command in the current session's available command catalog and read its complete definition before proceeding. Use native command discovery and the selected definition's source, not a guessed path or a same-named skill. Only use commands available in the current role; do not bypass selection or disabled entries. Reject `arena` itself to prevent recursion. Built-in or extension commands without an accessible prompt workflow cannot be wrapped; explain that limit rather than pretending to invoke them.

If the command or prompt is missing, show `/arena <command> <prompt>` and a relevant example, then stop without spawning workers. If the command is unknown, unavailable, or the request conflicts with its argument contract, explain the issue and stop. Where the selected definition has argument placeholders, use the remaining text as its arguments; retain the same text as the user's task scope even if that definition has no placeholder. Never reinterpret prose as a PR identifier or relax the selected command's validation.

## Compare, then carry out the selected workflow

Read `skill://arena` and follow its bounded proposal, single critique exchange, and main-agent synthesis workflow. This invocation explicitly opts into Arena for this request. Do not recursively dispatch the selected command or let workers run its actions.

The shared brief must include the selected command's full workflow, the supplied prompt, acceptance criteria, argument contract, output requirements, approval gates and non-goals. Compare approaches to completing that exact task, not a different or expanded task. Use the skill's default five approaches unless the user explicitly requests fewer. Announce the selected approaches before dispatch and respect the four-worker concurrency limit.

Workers are proposal/critique-only: they may read evidence and write assigned `local://` artifacts, but must not edit project files, run checks, execute candidate code, persist memories, install packages or publish anything. Shared factual discovery belongs to the main agent; do not repeat side-effecting workflow steps for each candidate.

After synthesis, the main agent performs the selected command's workflow once, within its original scope and the shared execution policy. A read-only command stays read-only. A comparison-only request does not authorize implementation. An editing command permits only its specified edits; required approval gates still apply. Never multiply checks across candidates, change model/permission settings, or claim a complete comparison when a proposal or critique is missing. Follow the Arena skill's incomplete-run handling.

Preserve the selected command's required deliverables and output format. Add a concise recommendation, decisive tradeoffs and actual verification limits where that format permits. Distinguish proposal evidence from verified execution results.
