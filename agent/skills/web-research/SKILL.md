---
name: web-research
description: "Multi-source web research with evidence tracking and cross-verification. Use when researching technologies, comparing options, investigating best practices, fact-checking claims, or any question requiring synthesis from multiple web sources. Triggers: research, investigate, compare options, what are best practices, find out about, deep dive, literature review, due diligence, fact check, verify claim, current state of."
---

# Web Research

Evidence-based web research protocol. Moves from broad discovery to cited synthesis with source tracking and cross-verification.

## When to Use

- Researching technologies, libraries, or architectural patterns
- Comparing multiple options/tools for a decision
- Fact-checking claims about APIs, versions, deprecations
- Investigating best practices or current state of a domain
- Any question requiring 3+ sources to answer well

## When NOT to Use

- Single known-answer lookups (use `read` for a known source or the `librarian` for library documentation)
- Codebase-specific questions (use `code-research` skill instead)
- Questions answerable from code you've already read

## Available tools

| Tool | Best for |
|---|---|
| `web_search` | Current discovery when no source URL is known |
| `read` | Fetching known pages, documentation, and source files |
| Context7 MCP tools | Current official library documentation and examples |
| `librarian` agent | Multi-source research, library documentation, and open-source comparisons |

Use the `librarian` for external factual research. Keep source discovery and synthesis read-only.

## Research Protocol

### Phase 1: Frame (before any search)

Define clearly:
1. **Question**: What exactly am I trying to answer?
2. **Scope**: What's in/out of scope?
3. **Deliverable**: Decision memo? Comparison table? Summary?
4. **Freshness**: Does recency matter? (library versions = yes, design patterns = less so)
5. **Effort level**: quick (2-3 sources) | standard (4-6 sources) | deep (7+ sources, 3+ source types)

### Phase 2: Map (plan search routes)

Identify 3-5 independent search angles:
- Official documentation / project sites
- Community discussions (GitHub issues, forums)
- Blog posts / tutorials with production experience
- Academic papers (if applicable)
- Competing/alternative projects for contrast

### Phase 3: Seed

Delegate independent search angles to the `librarian` in one batched `task` call. Use:

- Context7 for official library documentation;
- `web_search` for broad discovery;
- `read` for known official pages and source files;
- official repositories for implementation and release evidence.

Use at least two independent sources for consequential claims. Do not multiply tools when one primary source answers a simple question.

### Phase 4: Extract

For each promising source:

1. Fetch the full content with `read`.
2. Record the URL, publication or update date, author credibility, and relevant claims.
3. Mark whether it is primary evidence, such as official documentation, source, releases, or benchmarks.
4. Keep only evidence that answers the scoped question.

### Phase 5: Verify (cross-check)

Before reporting any finding as fact:
- **Version/API claims**: Verify against official docs (Context7 or official site)
- **Performance claims**: Look for independent benchmarks, not just author's claims
- **Best practice claims**: Check if 2+ independent sources agree
- **Deprecation claims**: Check official changelog/migration guides

Flag when:
- Only 1 source supports a claim → mark as "unverified"
- Sources contradict each other → report the contradiction explicitly
- Source is >1 year old on fast-moving topic → mark as "possibly stale"

### Phase 6: Synthesize (produce output)

Structure output as:

```markdown
## Research: [Topic]

### Summary
[2-3 sentence executive summary]

### Key Findings
1. [Finding] — [Source: URL]
2. [Finding] — [Source: URL]

### Comparison (if applicable)
| Criterion | Option A | Option B |
|-----------|----------|----------|
| ...       | ...      | ...      |

### Recommendation
[Evidence-backed recommendation with confidence level]

### Sources
- [URL] — [type: official/blog/benchmark/discussion] — [date]

### Uncertainties
- [What couldn't be verified or remains unclear]
```

## Effort Calibration

| Level | Sources | Search Tools | When |
|-------|---------|-------------|------|
| Quick | 2-3 | 1-2 | Low-risk, orientation |
| Standard | 4-6 | 2-3 | Normal researched answer |
| Deep | 7+ | 3+ | Decision with consequences, due diligence |

## Rules

1. **Search FIRST, answer SECOND** — never rely on internal knowledge for factual claims
2. **2+ sources minimum** — for any claim presented as fact
3. **Cite everything** — every finding must link to its source
4. **Flag uncertainty** — explicitly state what you couldn't verify
5. **Freshness matters** — prefer recent sources for fast-moving topics
6. **Source diversity** — use multiple search tools, not just one
7. **Stop when saturated** — if 2 consecutive searches yield no new information, stop
8. **No fabricated sources** — if you can't find a source, say so

## Academic research

Delegate academic research to the `librarian`. Require primary papers or official proceedings, publication dates, and explicit separation between paper claims and later interpretation.

## Anti-Patterns

- Searching once with one tool and calling it "research"
- Presenting internal knowledge as researched fact without verification
- Ignoring contradicting sources
- Not checking source dates on time-sensitive topics
- Over-researching simple questions (quick effort = fine for most)
