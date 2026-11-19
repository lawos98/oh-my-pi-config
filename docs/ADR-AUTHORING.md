# ADR authoring style

Use this reference when creating, updating, reformatting or showing an architecture decision record through any OhMyPi command, skill or ordinary conversation. It defines the user's ADR presentation preference; `documentation-and-adrs` still owns significance, evidence, decision lifecycle and documentation quality. It is not a new command, skill, approval policy or documentation generator.

## Default structure

Keep these headings in this relative order:

1. `## Context and Problem Statement`
2. `## Decision Drivers`
3. `## Considered Options`
4. `## Decision Outcome`
5. `## Pros and Cons of the Options`
6. `## More Information`

Keep needed shared contracts, state transitions, scope, examples and acceptance/evidence sections rather than deleting them to force this outline. They can be subsections of context or placed after the option comparison and before More Information. Preserve existing stable anchors where practical. Do not copy a service-specific risk policy, identifier or process into unrelated ADRs.

A current explicit user format or binding repository constraint overrides this default. If the renderer cannot support tabs, explain that limitation and retain the complete option bodies as individually headed sections; do not silently flatten them into a comparison table. Do not install a renderer or dependency just to obtain tabs without approval.

## Options are full tabs, not summary rows

For Markdown sites supporting Material/Zensical-style tabs, use literal `=== "A · Short label"` blocks. Indent every line of a tab's body by four spaces, including fences and admonitions; nested bodies need another indentation level. Match existing renderer syntax and verify actual tab switching when browser verification is authorized.

A compact Considered Options table may orient the reader, but is not a replacement for the detailed tabs. Each credible alternative keeps:

- A concise mechanism: what changes and where the rule/data/responsibility lives.
- **How It May Work**: numbered steps explaining enough of the implementation path to evaluate it, including relevant callers, mapping, guards, mutations, persistence, consumers and failure handling. Do not turn this into a compulsory file-by-file delivery plan.
- Source-backed code or configuration, or clearly labelled proposed/illustrative snippets, when they make the mechanism concrete. Include relevant persistence representation or a statement that storage is unchanged. Use valid Kotlin/YAML/JSON appropriate to the repository; do not fabricate existing fields, endpoints or guarantees.
- **Example**: a concrete scenario showing the option's externally meaningful behavior and relevant boundary or transition. Reuse shared business assumptions rather than changing behavior between options accidentally.
- `!!! success "Positive"` and `!!! failure "Negative"` callouts with substantive benefits, costs, risks, compatibility concerns and scope limits.
- The option's actual outcome when known: selected, rejected or still a candidate, with the real reasons. Do not invent a rejection to fill the template.

Keep material details from existing tabs: numbered steps, code/YAML/JSON, examples and trade-offs must not disappear during a request to simplify prose, add visuals or improve layout. Move common facts to one shared section and link when useful; retain the distinct mechanism and consequences in each tab. Do not impose a fixed option count, manufacture straw alternatives or generalize solely to create a comparison.

## Decision status is independent of formatting

- A new/team-discussion ADR stays **Proposed / Pending team discussion**, with no option selected unless approval actually occurred.
- Do not use a literal `TODO` as the decision outcome. Write a useful pending statement and identify what the team needs to decide.
- If a decision was accepted, preserve it and its reasons while restoring the detailed rejected alternatives. Reformatting does not reopen approval or make every option a fresh candidate.
- Recommendations, if requested or otherwise warranted, are recommendations—not approval. Remove a preferred option when the user explicitly requests a neutral comparison.
- Accepted design is not proof of implementation, deployment or passed tests. Keep current behavior, proposal, illustration and observed verification distinct.

## Concrete context and visual explanations

When the problem concerns backend process creation, show the actual relevant controller/command entry points and trace request → enrichment/guard or admission → actions → persistence/scheduled effects as supported by inspected source. Distinguish those backend entry points from frontend button/link configuration; do not broaden a backend restriction into a UI change by terminology alone.

Use diagrams to explain genuine structure, flow, lifecycle or storage/view boundaries—not as decorations or replacements for important reasoning. Follow the selected documentation stack's existing diagram, accessibility, theme and export rules. In HTML sites, follow `/developer-docs`' single-iframe presentation contract. Keep a complete searchable explanation outside iframes. Preserve editable sources and export assets without duplicating visuals on the page.

For data changes, show representative valid entity/document excerpts that match inspected serialization. Label partial documents and omitted metadata. Put proposed fields/statuses only inside the option that introduces them; never imply they already exist. For unchanged storage, refer to the common example rather than inventing a second persisted flag.

## Template

This illustrates presentation, not a requirement to invent a second option or unverified technical facts. Add one tab per real alternative with meaningful content.

````markdown
# Short decision title

## Context and Problem Statement

Describe the concrete problem, current relevant flow and intended outcome. Include
source-backed entry points, a useful diagram or a storage example where relevant.

## Decision Drivers

- State the actual constraints and qualities that distinguish the alternatives.

## Considered Options

| Option | Mechanism | Status |
|---|---|---|
| A — Short label | Where this approach puts the responsibility | Candidate |

## Decision Outcome

**Pending team discussion. No option is selected or accepted.**

Record the actual selection and reasons here only after approval.

## Pros and Cons of the Options

=== "A · Short label"

    **State the mechanism in one sentence.**

    **How It May Work**

    1. Describe the affected boundary and the first meaningful change.
    2. Trace the relevant data/action path and consumer or failure consequences.

    **Code / Configuration / Database**

    Include a source-backed or explicitly illustrative fenced example in the
    appropriate language when it helps evaluate this option. If storage is
    unchanged, say so and refer to the common entity example.

    **Example**

    Describe a concrete input/state, resulting behavior and material boundary.

    !!! success "Positive"
        - Explain a real benefit tied to the decision drivers.

    !!! failure "Negative"
        - Explain a real cost, risk or compatibility consequence.

## More Information

Include useful source links, lifecycle metadata, known limitations and the
necessary implementation/acceptance evidence without claiming unrun checks passed.
````

## Completion check

Before delivery, confirm that every substantive alternative is still present, each tab follows the requested structure, examples and decision status are preserved, and all source/configuration claims are labelled accurately. When authorized and relevant, check the rendered tabs—including non-default tabs—and diagram/code rendering under the shared execution policy. Report actual verification and uncompiled illustrative snippets separately.
