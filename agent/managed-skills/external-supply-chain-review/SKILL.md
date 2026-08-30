---
name: external-supply-chain-review
description: "Use before adopting or installing an external repository, agent skill, plugin, MCP server, extension, CLI, package, installer, or marketplace into OMP or a project."
---

# External Supply-Chain Review

Review external additions before any install, execution, or configuration change. Treat README claims and popularity as leads, not evidence.

## Default posture

- Work read-only. Do not run installers, lifecycle scripts, downloaded binaries, hooks, extensions, MCP servers, or repository code during admission review.
- Pin findings to an immutable commit, release, package version, and digest where available. A floating branch or `latest` is not a reproducible source.
- Prefer a small passive adaptation over a new runtime. Reuse current OMP tools, skills, plugins, MCPs, and native security scanning before adding another component.
- Never expose local source, prompts, history, credentials, or production data to the candidate.

## Review sequence

### 1. Establish provenance

Record the owner, immutable revision, release/package relationship, license, maintenance activity, supported host versions, and whether generated or vendored files can be traced to source. Flag package/repository version drift and mutable marketplace sources.

### 2. Map the complete operational surface

Inspect manifests, lockfiles, entry points, installers, postinstall/preinstall scripts, hooks, extensions, commands, MCP definitions, update paths, telemetry, background services, generated configuration, and uninstall behavior. Follow each operational outbound link at least one hop. Inventory catalogs by category; audit shortlisted entries separately.

### 3. Trace authority and data flow

For every executable component, identify:

- files and directories it can read, write, rename, or delete;
- subprocesses, shells, package managers, and PATH-resolved binaries it can invoke;
- network destinations, listener bind addresses, authentication, CORS, redirects, and download verification;
- credentials, prompts, source, session history, tool results, and metadata it stores or transmits;
- persistence, auto-start, auto-update, scheduled work, hooks, and session-wide prompt injection.

Reject plaintext credential storage, unauthenticated non-loopback listeners, wildcard CORS over private data, incomplete secret redaction, unchecked archive members or symlinks, path traversal, shell interpolation, silent checksum bypass, and unpinned remote execution.

### 4. Test fit, not novelty

Compare the candidate with the current setup. Duplicate graph indexes, memory stores, LSPs, compaction hooks, global output styles, orchestrators, reviewers, or frontend authorities are costs unless a verified gap exists. Check license obligations and OMP API/version compatibility before considering source reuse.

### 5. Produce a decision

Use one verdict:

- **Adopt**: a pinned, maintained, compatible component with a necessary capability and acceptable authority.
- **Adapt selected parts**: only named passive rules, schemas, or bounded read-only logic are useful; exclude installers and runtime surfaces.
- **Reference only**: useful architecture or examples, but no current setup change.
- **Skip**: duplicate, irrelevant, opaque, unsafe, incompatible, or unjustifiably invasive.

Report evidence with immutable URLs and exact paths/lines. Separate verified facts from inference. Name the smallest proposed change, excluded components, data boundary, license/attribution, reload requirement, and focused verification. Make no change until the user explicitly approves it.

## Adoption gate

After approval, import only the reviewed subset. Preserve attribution, remove obsolete or conflicting paths, read the installed result back, and run the smallest behavior check that would fail if its trigger, safety boundary, or output contract were wrong.

## Sources

Clean-room procedure informed by these audited snapshots:

- NVIDIA SkillSpector, Apache-2.0: `1b875933a666b627c3ed1b695f066a21a6773dc4`
- Trail of Bits skills, CC BY-SA 4.0: `d1f1575cff97816e5cc08af66cd2506099c681d3`
- Vibe-Skills policy files: `eace1927e5cd7aed57501f81b5ef57ed3ea7008d`
- testzugang dependency-audit guidance, MIT: `417b40455f93da9c5c88dff36ba40cc4bb120a51`
