# Visual and interaction review

Review the real exported board and its current native structure. Identify the exact target, dimensions, theme, fixture and revision. Missing screenshots or a disconnected canvas limits conclusions; do not infer visual quality from tool success or shape counts.

Assess these independently:

| Area | Evidence to inspect |
| --- | --- |
| Task clarity | Entry point, next action, content hierarchy, readable labels, recovery |
| Composition | Alignment, rhythm, spacing, balance, meaningful density, thumb reach |
| Type and copy | Hierarchy, line length, wrapping, actual labels, units, truncation |
| Identity | Coherent materials/art/icons, distinctive choices supported by the brief |
| Components | Consistent roles, token reuse, state coverage, instance behavior |
| Mobile | Narrow width, long/large text, safe areas, keyboard, touch spacing |
| Accessibility | Contrast on rendered surfaces, non-color cues, focus annotations, motion alternatives |
| Prototype | Working links, return paths, modal dismissal, pending/failure/empty branches |

Check text contrast with `scripts/contrast.py` when solid sRGB color pairs are known. Composite transparency and imagery first; a raw hex ratio does not prove the rendered result. WCAG text thresholds and platform touch recommendations are different criteria. Consult official guidance for the actual target platform; do not call a 44 px recommendation the WCAG AA minimum.

For each finding provide severity, board/object, observed evidence, user consequence and a concrete correction. Do not manufacture numeric usability or aesthetic scores. Separate visual defects from open product decisions. `review` is read-only; `polish` authorizes scoped fixes while preserving the chosen identity and behavior.

Build/inspect in meaningful batches: inspect representative screens, correct related defects together, then verify the affected outputs. Continue when there is an actual unresolved defect, rather than repeatedly changing acceptable details. Human usability testing remains separate from AI critique.

Primary references (accessed 2026-10-01):

- https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- https://developer.apple.com/design/human-interface-guidelines/accessibility
- https://m3.material.io/foundations/accessible-design/overview
- https://help.penpot.app/user-guide/prototyping/
