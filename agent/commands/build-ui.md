---
name: build-ui
description: Build or refine a complete, distinctive, accessible UI and verify the real browser experience.
---

Implement the requested UI directly. Do not stop at mockups, suggestions, or a design critique when the request is actionable.

1. Read and apply `product-ui-engineering`, `typescript-javascript-clean-code`, and `react-performance`. Apply `frontend-design` when that optional plugin skill is installed, and apply the repository's framework-specific skill when available.
2. Inspect the existing surface, routes, components, tokens, content, data flow, and nearby visual conventions before editing. Reuse the current design system; do not add a second component or styling system.
3. Choose one subject-specific visual direction internally. Avoid generic AI layouts, arbitrary gradients, decorative numbering, placeholder copy, and repeated card grids unless the product genuinely calls for them.
4. Implement the full journey: layout, typography, responsive behavior, semantic structure, keyboard operation, visible focus, reduced motion, loading, empty, error, disabled, success, and retry states.
5. Keep state at its real owner. Use native controls and platform behavior first. Prevent duplicate mutations and avoid speculative memoization or dependencies.
6. Run LSP diagnostics on every edited source file and the repository's narrowest relevant checks.
7. Launch the actual application and exercise the changed journey with the browser at the repository's desktop and mobile breakpoints. If none are defined, use approximately `1280x800` and `390x844`. Inspect appearance, overflow, accessibility tree, keyboard and focus behavior, console, failed network requests, and the relevant performance path. Fix observed defects before finishing.
8. Report the implemented result and verification evidence. Label browser checks `Ran` or `Skipped`; give the reason for every skipped check. Do not append a generic list of future improvements.

Do not commit, push, change branches, or modify unrelated screens.
