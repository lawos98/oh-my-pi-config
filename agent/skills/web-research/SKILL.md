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
- Questions requiring synthesis across independent sources

## When NOT to Use

- Single known-answer lookups (use `read` for a known source or Context7 directly for library documentation)
- Codebase-specific questions (use `code-research` skill instead)
- Questions answerable from code you've already read

## Available tools

| Tool | Best for |
|---|---|
| `web_search` | Current discovery when no source URL is known |
| `read` | Fetching known pages, documentation, and source files |
| Context7 MCP tools | Current official library documentation and examples |

Use Context7 directly for library documentation, read for known sources, and web_search for discovery. Delegate only substantial independent research slices under RULES.md, using an available, permitted agent. Keep source discovery and synthesis read-only.

## Research Protocol

### Phase 1: Frame (before any search)

Define clearly:
1. **Question**: What exactly am I trying to answer?
2. **Scope**: What's in/out of scope?
3. **Deliverable**: Decision memo? Comparison table? Summary?
4. **Freshness**: Does recency matter? (library versions = yes, design patterns = less so)
5. **Evidence needed**: identify the claims and uncertainties to resolve using the evidence-sufficiency guidance below.

### Phase 2: Map (plan search routes)

Choose search angles that address the question or add independent evidence:
- Official documentation / project sites
- Community discussions (GitHub issues, forums)
- Blog posts / tutorials with production experience
- Academic papers (if applicable)
- Competing/alternative projects for contrast

### Phase 3: Seed

Start with the sources suited to the question. Follow the delegation guidance above when independent slices justify it. Use:

- Context7 for official library documentation;
- `web_search` for broad discovery;
- `read` for known official pages and source files;
- official repositories for implementation and release evidence.

Apply the evidence-sufficiency guidance below; do not multiply tools when one primary source answers a simple question.

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
- **Best practice claims**: Seek independent corroboration and explain where the recommendation applies.
- **Deprecation claims**: Check official changelog/migration guides

Flag when:
- State when a consequential claim lacks independent corroboration. Distinguish an authoritative API contract from an uncorroborated empirical claim.
- Sources contradict each other → report the contradiction explicitly
- Source is >1 year old on fast-moving topic → mark as "possibly stale"

### Phase 6: Synthesize (produce output)

Match the requested deliverable. Use the following structure for a substantial research report; narrow answers need only the conclusion, citations, and relevant uncertainty.

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

## Evidence sufficiency

Choose research depth from the question and its consequences, not a source or tool count.

- For a narrow API or version fact, use the applicable official documentation or implementation and cite it.
- For consequential recommendations, disputed claims, or performance comparisons, seek independent corroboration and disclose material uncertainty.
- Multiple pages repeating the same upstream claim are not independent corroboration.
- Stop when the requested questions are answered and material contradictions are resolved or explicitly reported.
- A requested deep review still requires broad evidence coverage; do not substitute a single lookup for the requested comparison.

## Rules

1. **Search FIRST, answer SECOND** — never rely on internal knowledge for factual claims
2. **Evidence sufficiency** — follow the guidance above rather than a fixed source count.
3. **Cite everything** — every finding must link to its source
4. **Flag uncertainty** — explicitly state what you couldn't verify
5. **Freshness matters** — prefer recent sources for fast-moving topics
6. **Independent evidence** — use additional sources or tools when they add independent evidence or resolve a specific uncertainty.
7. **Stop when saturated** — if 2 consecutive searches yield no new information, stop
8. **No fabricated sources** — if you can't find a source, say so

## Academic research

Research academic questions directly or delegate under the guidance above. Require primary papers or official proceedings, publication dates, and explicit separation between paper claims and later interpretation.

## Anti-Patterns

- Presenting a single lookup as a completed multi-source comparison or deep review
- Presenting internal knowledge as researched fact without verification
- Ignoring contradicting sources
- Not checking source dates on time-sensitive topics
- Over-researching simple questions (quick effort = fine for most)
