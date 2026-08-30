---
name: react-performance
description: "Use when implementing, reviewing, or debugging React or Next.js performance, including async waterfalls, bundles, server/client boundaries, hydration, or unnecessary rerenders."
---

# React Performance

Improve measured React or Next.js performance without replacing the repository's architecture, state model, data-fetching library, or styling system.

## Decision order

1. Reproduce the slow user journey and identify whether the cost is network, server work, JavaScript transfer, hydration, rendering, or repeated work.
2. Fix the earliest shared cause. Do not scatter memoization or loading states around a downstream symptom.
3. Prefer deletion, direct imports, server work, parallel work, and native platform behavior over new dependencies or abstractions.
4. Verify the same journey after the change with browser evidence.

## Async work

- Start independent work together and await it at the latest necessary boundary. Remove avoidable request waterfalls.
- Keep dependent requests sequential. Do not parallelize work that requires a prior result.
- Fetch at the server or route boundary when the data is shared or required before rendering. Do not duplicate the same request across child components.
- Stream or defer independent slow regions when the framework and existing application pattern support it.
- Preserve cancellation, error, empty, loading, retry, and duplicate-submission behavior.

## Bundle cost

- Import the exact module or component when a package's barrel entry pulls unnecessary code.
- Lazy-load heavy, optional, interaction-only UI. Do not lazy-load critical above-the-fold content merely to reduce a bundle report.
- Keep server-only libraries, secrets, and data clients out of client bundles.
- Remove duplicate libraries and dead compatibility paths before introducing custom chunking.
- Treat a package-size claim as evidence only after inspecting the actual build or bundle output.

## Server and client boundaries

- Keep components server-rendered by default where the repository and framework support it. Add a client boundary only for browser APIs, local interaction state, effects, or event handlers.
- Pass the smallest serializable data shape across the boundary. Do not pass large records when the client reads a few fields.
- Move stable static content outside client components when this reduces hydration work without fragmenting ownership.
- Use the repository's current caching and revalidation model. Confirm current Next.js or React behavior from official documentation before changing framework-specific caching.

## Rendering

- Keep state at its nearest real owner. Split rapidly changing context from rarely changing context when profiling shows broad consumer updates.
- Remove derived state and effect-driven synchronization when render-time derivation is sufficient.
- Use `memo`, `useMemo`, and `useCallback` only for measured expensive work or required referential stability. Their own comparisons, retained values, and complexity have a cost.
- Stabilize objects or callbacks at the source when identity churn is the demonstrated cause. Do not memoize every prop defensively.
- Use stable keys that represent item identity. Never use a changing value to force remounts as a performance fix.

## Browser and hydration

- Prevent server/client output mismatches. Isolate unavoidable browser-only values behind an existing client boundary.
- Defer non-critical third-party scripts and work until after the critical interaction path where product behavior permits.
- Preserve semantic HTML, keyboard operation, visible focus, reduced motion, and responsive behavior. Performance does not justify accessibility regressions.
- Give images intrinsic dimensions and use the repository's image optimization path. Prioritize only genuinely critical images.

## Verification

Exercise the changed journey in the browser. Inspect the network waterfall, failed requests, console, accessibility tree, and relevant React or browser performance evidence. For bundle changes, inspect the project's actual production build output. Report the observed before/after signal; do not claim a performance improvement from source shape alone.

Add a focused regression test only when the observable contract is otherwise unprotected. Do not add source-text tests for memoization or import style.

## Source

Narrow adaptation of Vercel's MIT-licensed React Best Practices at immutable revision `063bee94c3f4df8453406c830b0a7df0f2860278`. Deployment, Vercel CLI, token, and hosted optimization skills are intentionally excluded.
