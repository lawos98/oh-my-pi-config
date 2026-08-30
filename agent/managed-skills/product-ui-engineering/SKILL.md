---
name: product-ui-engineering
description: "Use when building or refactoring web UI, screens, user journeys, responsive layouts, design systems, frontend components, or frontend architecture."
---

# Product UI Engineering

Build web interfaces that work for the user, fit the product, remain responsive, and leave maintainable frontend code. Treat visual design, interaction design, accessibility, performance, and component architecture as one implementation problem.

When the user asks to build or change UI, implement it. Do not stop at a critique, wireframe, option list, or generic improvement report unless design-only output was requested.

## Start from the user's job

Before editing, establish from the repository and request:

- who uses the surface;
- the task they came to complete;
- the entry point and primary action;
- the information needed to decide or act;
- the successful outcome;
- likely failure, empty, and recovery paths.

Build the complete journey, not a screenshot of the happy state. Use real product language and realistic content from the domain. Do not invent metrics, testimonials, activity, social proof, notifications, or capabilities.

## Reuse the product's system

Inspect existing routes, components, tokens, typography, spacing, icons, forms, navigation, data hooks, state ownership, and responsive conventions. Reuse them before creating anything. Do not introduce another component library, CSS strategy, state store, form library, icon set, or design-token system for one screen.

Give each product concept one UI owner. Share a component only when multiple callers need the same visual and behavioral contract. Similar markup alone does not justify a generic component. Avoid catch-all components controlled by many boolean props, giant page components, and wrappers that only rename native elements.

## Make an intentional visual direction

Apply `frontend-design` for aesthetic direction. Derive hierarchy, typography, color, density, and the signature element from the product subject and audience.

Avoid default AI composition:

- interchangeable card grids for unrelated information;
- oversized hero text on application screens;
- arbitrary gradients, glow, glass, and heavy shadows;
- pills for every label or action;
- decorative charts, statistics, numbering, badges, and icons without product meaning;
- centered layouts where the task requires scanning or comparison;
- placeholder copy, fake data, and repeated marketing slogans;
- animation added only to make the page look elaborate.

These patterns are allowed only when the content and task require them. Spend visual emphasis on the primary user decision or action. Remove decoration that competes with it.

## Design responsive behavior, not scaled screenshots

- Implement narrow and wide layouts as first-class states. Use content-driven breakpoints and the repository's responsive primitives.
- Prevent horizontal overflow at supported widths. Let text and long unbroken values wrap, make tables scroll or transform intentionally, and keep controls reachable.
- Preserve readable line length, clear hierarchy, touch targets, and safe spacing at mobile widths. Account for device safe-area insets where controls or content meet viewport edges.
- Reflow navigation, filters, forms, actions, dense data, dialogs, and side panels deliberately. Do not merely shrink fonts and gaps.
- Account for long names, translated text, empty values, validation messages, browser zoom, and dynamic content. When the product supports right-to-left languages, use logical layout properties and verify bidirectional content.
- Keep the primary action available without covering content or relying on hover.

## Implement every interaction state

For each data and mutation path, implement the applicable states:

- initial loading;
- progressive or deferred loading;
- empty with a meaningful next action;
- partial data;
- validation error;
- request or permission failure with recovery;
- pending and disabled mutation state;
- success confirmation;
- stale or retry state.

Keep action names consistent through button, dialog, progress, result, and error text. Prevent duplicate submissions. Preserve user input after recoverable failures. Confirm destructive actions when their effects cannot be recovered. Do not use a skeleton when a stable layout, optimistic state, or small progress indicator communicates better.

## Keep frontend architecture honest

Apply `software-architecture`, `typescript-javascript-clean-code`, and `react-performance` where relevant.

- Keep server, URL, form, remote, and local interaction state distinct and at the nearest real owner.
- Do not mirror props into state or use effects for values that can be derived during render.
- Keep data fetching and mutations at established route or data boundaries. Avoid duplicate requests and async waterfalls.
- Keep server-only dependencies and secrets outside client bundles. Cross server/client boundaries with the smallest required serializable shape.
- Validate untrusted data before rendering or using it in navigation, HTML, styles, or commands.
- Prefer semantic HTML and native behavior. Use ARIA only when native semantics cannot express the interaction.
- Use stable domain keys. Do not force remounts to hide state bugs.
- Add memoization only for measured work or required identity stability.
- Reuse transformations and business rules from their authoritative domain owner; do not reimplement backend policy in multiple components.

## Accessibility is part of completion

Require semantic landmarks and headings, programmatic labels, full keyboard operation, logical focus order, visible focus, sufficient contrast, meaningful error association, screen-reader status for asynchronous results, reduced-motion support, and accessible names for icon-only controls.

Opening, closing, submitting, failing, and returning from dialogs, menus, drawers, and routes must move or restore focus intentionally. Sticky surfaces and overlays must not obscure the focused element. Color, position, animation, hover, and placeholder text must not be the only way information is communicated.

Use the correct input `type`, `inputmode`, and `autocomplete`. Do not disable paste or browser zoom. Stateful controls must expose their pressed, selected, expanded, or current state. Live regions must announce a complete useful message rather than a fragment.

Charts must distinguish values with labels, patterns, shapes, or line styles in addition to hue. Provide the underlying values and a concise interpretation as accessible text or a visible table. Do not make hover the only way to inspect data.

## Verify the real surface

After implementation:

1. Run LSP diagnostics on every edited source file and the repository's narrowest relevant checks.
2. Launch the actual application.
3. Exercise the complete changed journey with the browser at narrow and wide viewport sizes.
4. Inspect visual hierarchy, overflow, wrapping, keyboard behavior, focus, accessibility tree, console errors, failed network requests, duplicate requests, and mutation states.
5. Test representative long content, empty data, failure, pending, and success states when the application makes them reachable.
6. Fix observed defects and repeat the journey.

A source review, screenshot, unit test, or successful build alone does not prove the UI works. If the application cannot be launched, state that visual and interaction verification was not performed; never claim otherwise.

Finish with the implemented result and actual verification evidence. Do not append generic UX or code-quality suggestions, create design documents, or list speculative future improvements unless the user requests them.
