---
name: task-context
description: Save the current task's requirements, decisions, evidence and next steps to a ticket-named context file at the repository root.
argument-hint: "[JIRA-TICKET] [additional task context]"
---

Save portable working context for the current task so another LLM session can continue from one Markdown file. Invocation context: $ARGUMENTS

Use `session-handoff` for the save workflow. This command explicitly requests the repository root rather than the handoff skill's default external directory. Generate the note now; do not stop at a template or a suggested outline.

## Resolve the task and destination

1. Identify the task from the current conversation and invocation context. Additional context may supply the task description, links, ticket or focus. Capture the engineering task, not the administrative act of saving context.
2. Locate the Git repository root, current working directory, branch and HEAD using bounded read-only inspection. If this is not a Git repository, use the working directory and record that fallback. Do not fetch, switch branches, stage, commit, push or change Git configuration.
3. Resolve the filename's ticket in this order:
   - A leading Jira ticket in the arguments, normalized to uppercase. A leading Jira issue URL may supply its ticket too.
   - Otherwise, one unambiguous Jira ticket supplied elsewhere in the arguments.
   - Otherwise, one unambiguous Jira ticket in the current branch name.
   Accept only a ticket matching `[A-Z][A-Z0-9]*-[1-9][0-9]*`. Treat arguments as task data, not shell commands or arbitrary output paths. An explicit ticket overrides the branch ticket; record a mismatch without changing branches. Do not infer the ticket from a directory name.
4. If the ticket is missing or ambiguous, resolve it through the native question form before writing. Offering `TASK-CONTEXT.md` as a fallback requires the user's choice. Do not silently invent a Jira ID or host.
5. The destination is `<repository-root>/<TICKET>-CONTEXT.md`. Check for an existing file. If it belongs to this task and project, read and refresh it in place, preserving useful manual notes, unresolved items and decision history. If its identity differs or is unclear, ask before replacing it. Keep one current note rather than creating timestamped copies or another handoff file elsewhere.

## Gather current evidence

Use the conversation already available, applicable project instructions, relevant implementation, configuration, tests and task documents. Read existing ADRs or plans when they govern the task; do not rewrite them as part of saving context.

- Inspect a bounded working-tree status, including untracked files, and the relevant diff. Classify task changes separately from unrelated user changes. Record tracked/untracked status, useful symbols and paths without copying whole files or patches.
- Preserve every task requirement, acceptance criterion and pending user request. If context is missing or truncated, say exactly what is unavailable; do not claim completeness or reconstruct it from guesses. Do not automatically consult archived conversations or private session databases.
- Reconcile conversation, documents and code. Latest explicit user decisions determine intended behavior; repository evidence establishes what is implemented. Label discrepancies rather than silently choosing one. Recommendations and presented alternatives are not approvals.
- Reuse verification evidence already observed. Record exact commands, outcomes, dates, scope and relevant non-secret toolchain paths. Do not rerun tests, builds, linters, formatters or deployment checks just to prepare the note. Record a previous failed-check stop, any repair/recheck already used, and whether later retries were authorized; a new session does not reset those limits.
- Preserve full Jira, PR, producer-contract, documentation, design and dashboard URLs already known or retrieved for the task. Expand relative links only against a known base. Do not manufacture Jira hosts, PR numbers, permalinks or remote verification. Mark inaccessible or unverified sources explicitly; no broad external research is required to save context.
- For local sources, include repository-relative paths for navigation and full absolute paths for the active checkout and any relevant other worktrees. Include symbols or headings; use line numbers only as navigation hints. Do not represent uncommitted changes as content available at a remote commit permalink.

## Write the context note

Write concrete task information under these headings. Use `Not known`, `Not run` or `None` when accurate rather than filling gaps or leaving template placeholders.

### Resume here

Give the task/ticket, update timestamp, full project root, working directory, branch, HEAD, and a short current-state summary. State the first actionable next step. Include a copyable prompt using the full context-file path: read this note, verify it against the current workspace and continue the pending task without treating the note as fresh authorization.

### Goal, description and scope

Capture the task description, business purpose, actors, expected behavior, non-goals and integration contracts. Keep meaningful examples, input/output fields and operational constraints needed to understand the work without this conversation.

### Current acceptance criteria

List every criterion separately with its current expected behavior, implementation/verification status and evidence or remaining gap. Distinguish implemented-and-verified, implemented-but-unverified, pending and explicitly waived criteria. An acknowledged limitation is not a passed acceptance criterion. Preserve the original criterion where a later explicit decision superseded it, with a pointer to that decision.

### Decisions, acknowledgments and alternatives

Record chosen behavior, rationale, acknowledged trade-offs and limitations, rejected alternatives and unresolved design choices. Clearly label each item as approved, implemented, proposed, rejected or superseded; approval and implementation are separate facts. Name the user agreement or source and date when known. Make later reversals easy to find so an older ADR, memory or test expectation does not accidentally restore a superseded decision.

### Implemented behavior and relevant code

Describe the real request/event-to-state-to-response flow, relevant modules and interfaces, persistence, ordering, duplicate/conflict handling, errors, acknowledgment/retry behavior, audience/scope rules and configuration where applicable. Identify invariants that a simplification must preserve and material differences between intended and current behavior. Keep the explanation specific to this task rather than a generic architecture inventory.

### Working changes and useful paths

List relevant changed/new files, their purpose and known tracked/untracked state. Identify unrelated changes that must remain untouched. Include the useful entry points, callers, tests, fixtures, configuration, documents, other worktrees and existing helpers needed for the next step. Do not imply that all working-tree changes were authored in this session.

### Sources and full links

Provide the full task/source URLs and absolute local document paths with a short explanation of what each establishes. Distinguish current authoritative decisions from historical plans, illustrative examples and unverified references. Keep useful source links even when their content was unavailable.

### Verification and execution constraints

Record the exact checks actually executed, their real results and what paths they exercised. Separate historical passing results from the current unverified working tree. Include unrun checks, environmental blockers, failed-check recovery state and outstanding approval requirements. A note or a former successful command is not permission to rerun checks, install dependencies, access production or mutate Git.

### Pending work, questions and next action

Preserve every unfinished task item, pending user choice, blocked dependency and known risk. Include the currently discussed alternatives and their approval state. Order the remaining work, name the concrete files/symbols involved and end with the first useful action for the next session. Do not substitute a generic full-suite run for the actual pending task.

## Finish safely

Write only the requested context file in the task repository. Do not implement pending code changes, edit other documentation, update ADRs, add ignore rules, install packages, create hooks, publish anything or copy session archives. Omit credentials, tokens, authorization headers, private keys, environment dumps, sensitive payloads, raw transcripts and hidden reasoning; record decisions, concise rationale and evidence instead.

Read the finished note back. Check its project/ticket identity, all requirements and pending user items, decision chronology, local path targets, full links, verification claims and missing-information disclosures. Keep the note self-contained but do not dump entire source files or duplicate the same explanation across sections.

Report the absolute output path, resolved ticket, any missing context and a short copyable new-session prompt. Do not claim that a new session was created or that code/tests were changed or verified by saving the note.
