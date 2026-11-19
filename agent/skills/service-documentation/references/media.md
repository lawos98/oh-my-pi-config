# Handbook diagrams and charts

Use for handbook media and portable diagrams/charts embedded in technical documentation. Preserve existing repository conventions. This reference does not admit a renderer, install dependencies, or authorize external uploads.

## Choose a form for the question

- **New service handbooks:** default process and architecture diagrams to Archify. Use its supported schema and installed adapter; do not invent schema fields. Keep diagrams still (`meta.animation: "none"`) with useful exploration controls.
- **Small inline explanations or existing conventions:** native Mermaid/SVG remains appropriate. Do not turn every relationship into a standalone interactive viewer or migrate established diagrams just for uniformity.
- **Qualitative comparisons:** use a table or a lightweight labelled plot. State that coordinates/rankings are judgments, define axes and ordering, and retain the accessible underlying list/table. Percent-positioned layout coordinates are not measured percentages or validated scores.
- **Measured data:** select the chart from the question and data. A table alone may be enough. For repeated statistical-chart needs, Vega-Lite is a candidate for a separate scoped admission review, not an installed default. Do not use Archify edges to simulate quantitative chart semantics.
- **Motion and video:** in handbooks, require an explicit user request. If requested, follow `archify` for trace motion or `hyperframes` for video, preserving complete still/text alternatives. Availability of a video skill does not authorize automatic use. A repository's no-video rule still wins.

Chat rendering is not repository rendering. OMP's table charts, Mermaid, and theme-aware SVG do not prove the same source works in GitHub Markdown, a site, PDF, or an offline checkout. Select and verify the intended delivery host; do not add a second visualization of the same information merely for decoration.

## Keep one editable source

For each authored diagram or chart, retain:

- the authoritative editable source and the paths of its derivatives;
- the relevant code revision or inspected working-tree scope, or data provenance and snapshot date;
- the renderer/version and necessary assets when generation is used;
- an adjacent searchable explanation, meaningful labels, and an adequate static or tabular alternative;
- links that work at the intended page depth and site path prefix.

Use existing metadata or adjacent prose; do not invent unsupported Archify JSON fields, create another permanent manifest, or install a tracking service just to record these facts. For Archify, JSON is authored; HTML/PNG are generated. Update source meaning and regenerate derivatives rather than editing their meaning independently. Adapter Markdown is a link fragment: follow the site's authoring reference to avoid same-stem output collisions.

Authored flows describe source relationships or explicitly labelled proposed behavior, not measured traffic, elapsed time, atomicity, or guaranteed delivery. Preserve important rejection, unmatched, and partial-failure branches. Keep evidence in the surrounding text so readers and site search do not depend on iframe internals.

## Make chart meaning reproducible

For quantitative charts, identify the source, date/version, units, population and time window, aggregation/filtering, missing-data handling, and axis scale or truncation that affects interpretation. Keep the reviewed input data or a safe reproducible derivation with the editable chart specification. Do not commit sensitive raw data merely for reproducibility.

Separate measurements, estimates, targets, and illustrative numbers. Verify plotted values and transformations against the underlying data/table. Do not manufacture realistic-looking values, error bars, causal claims, or a shared scale for incomparable populations.

## Privacy, accessibility, and verification

No public rendering endpoint, floating remote include, remote font/script, or remote chart data by default. Review required assets and approved dependencies before generation. Local-first is not an OS network-isolation guarantee. Never send private repository content to a candidate tool as part of evaluating it.

Use readable scaling and contrast, meaningful titles/descriptions and labels independent of color. Interactive controls need keyboard access; still/text/table alternatives carry the complete meaning. Do not copy chat-only theme variables into exported assets without verifying the target host supplies them.

During authorized verification, inspect the actual delivered surface: page-relative links, searchability, clipping, light/dark presentation, focus/search/routes where supported, full SVG/PNG exports, static fallback, and unintended remote requests. Follow the shared bounded execution policy and report only exercised checks. An export succeeding does not establish semantic accuracy, accessibility compliance, or offline behavior.

## References

These are conceptual/tool references, not installation approvals or copied templates:

- [Mermaid accessibility](https://mermaid.js.org/config/accessibility.html)
- [Vega-Lite data model](https://vega.github.io/vega-lite/docs/data.html)
- [Vega-Lite figure export](https://vega.github.io/vega-lite/tutorials/figures.html)
