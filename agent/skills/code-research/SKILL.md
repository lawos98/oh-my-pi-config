---
name: code-research
description: "Systematic code research across local and remote codebases. Use when exploring unfamiliar code, understanding architecture, finding implementation patterns, investigating how a library works internally, or researching how other projects solve a specific problem. Triggers: how does this work, find implementation of, explore codebase, understand architecture, find examples of, how do other projects handle, codebase analysis, what calls this, trace the flow, find usage patterns."
---

# Code Research

Systematic protocol for understanding code — local codebase, remote repos, libraries, and open-source patterns.

## When to Use

- Understanding unfamiliar module or codebase architecture
- Finding how something is implemented (locally or in OSS)
- Tracing data/call flows across modules
- Researching how other projects solve a specific problem
- Investigating library internals or undocumented behavior
- Finding production-quality implementation examples

## When NOT to Use

- You already know the file and just need to read it (just use Read)
- Simple text search where grep suffices (just use Grep)
- Web research about concepts/practices (use `web-research` skill)

## Available Tools

### Local codebase

| Tool | Best for |
|---|---|
| `glob` | Find paths and map structure |
| `grep` | Fast regex content search |
| `lsp` | Definitions, references, symbols, diagnostics, and safe renames |
| `ast_edit` | Structural search and codemods |
| GitNexus MCP tools | Semantic search, symbol context, flows, and impact |
| `scout` agent | Parallel read-only exploration |

### Remote and external

| Tool | Best for |
|---|---|
| `read` | Known URLs and source files |
| `web_search` | Current discovery across the web |
| Context7 MCP tools | Current official library documentation and examples |
| `librarian` agent | Multi-source documentation and open-source research |

## Research Protocol

### Phase 1: Scope the Question

Before searching, classify what you need:

| Question type | Primary tools | Strategy |
|---|---|---|
| "What does X do?" | LSP definition → Read → GitNexus context | Follow the code |
| "What calls X?" | LSP references → GitNexus context | Trace callers up |
| "How does data flow through?" | LSP + GitNexus + Read | Trace entry to exit |
| "How do other projects do X?" | Librarian + web search | External research |
| "What's the architecture?" | GitNexus → glob → Read | Top-down |
| "Why does X behave this way?" | Read + repository history | Code and history |

### Phase 2: Local discovery

**Layer 1 — Structure:** use `glob`, workspace symbols, and targeted `grep`.

**Layer 2 — Semantics:** use `lsp` definitions, references, implementations, and type information. Use `ast_edit` only when structural matching is necessary.

**Layer 3 — Graph:** use GitNexus context, query, trace, and impact tools for cross-module flows.

**Layer 4 — Parallel breadth:** dispatch one batched `task` call with independent `scout` assignments. Keep searches read-only and give each scout a distinct target.

### Phase 3: External discovery

- Use Context7 through the `librarian` for current library documentation.
- Use `read` for known official URLs and source files.
- Use `web_search` for discovery when no known URL is available.
- Delegate multi-source or open-source comparison to the `librarian`.
- Prefer primary sources and verify version-sensitive claims before reporting them.

### Phase 4: Trace & Understand

For flow tracing, work in ONE direction systematically:

**Top-down** (entry point → internals):
1. Find the entry point (controller, handler, listener)
2. Follow each call one level deep
3. Read each implementation
4. Map the dependency tree

**Bottom-up** (implementation → callers):
1. Find the target function/class
2. Use `lsp` references to find all callers.
3. Trace callers up until you reach entry points
4. Map which paths reach this code

**Data flow** (input → output):
1. Find where data enters (API, message, event)
2. Trace transformations at each layer
3. Note where data is persisted, cached, or forwarded
4. Map the complete lifecycle

### Phase 5: Synthesize

Structure your findings:

```markdown
## Code Research: [Topic]

### Architecture Overview
[How components relate — 3-5 sentences]

### Key Components
- `path/to/File.kt` — [what it does]
- `path/to/Other.kt` — [what it does]

### Data/Call Flow
[Entry] → [Processing] → [Storage/Output]

### Patterns Used
- [Pattern name] — [where and why]

### Key Decisions / Trade-offs
- [Why was X chosen over Y?]

### External References (if applicable)
- [Library docs, GitHub examples found]
```

## Rules

1. **Structure before content** — understand file/module layout before reading code
2. **LSP over grep** — for symbol navigation, LSP is more accurate
3. **GitNexus for cross-module** — when tracing across module boundaries
4. **Parallel agents for breadth** — dispatch 2–3 independent `scout` assignments only when breadth justifies them.
5. **Context7 before guessing** — use the `librarian` for current library documentation.
6. **Primary sources for patterns** — prefer official repositories and maintained examples.
7. **Stop when sufficient** — don't over-explore; answer the question and stop
8. **Read, don't skim** — when you find the relevant file, read it properly

## Anti-Patterns

- Grepping randomly without understanding the module structure first
- Reading every file in a directory instead of using LSP to navigate
- Asking a reviewer about code you have not read yet
- Searching external repositories for project-specific behavior
- Using only one discovery method when the question spans multiple modules
- Spawning scouts for work a single targeted search can answer
