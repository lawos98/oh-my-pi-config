---
title: Defer Non-Critical Work with requestIdleCallback
impact: MEDIUM
impactDescription: avoids competing with interaction work when optional work can wait
tags: javascript, performance, idle, scheduling
---

## Defer Non-Critical Work with requestIdleCallback

Use idle scheduling only for work that can safely wait or never run, such as optional prefetching. Do not move required saves, authorization, billing, user-visible state transitions, or time-critical operations into idle callbacks.

Feature-detect the API in browser-only code and provide cancellation:

```typescript
function scheduleOptionalWork(work: () => void): () => void {
  if (typeof window.requestIdleCallback === 'function') {
    const id = window.requestIdleCallback(work, { timeout: 2000 })
    return () => window.cancelIdleCallback(id)
  }
  const id = window.setTimeout(work, 1)
  return () => window.clearTimeout(id)
}
```

The timeout requests scheduling; it is not a promise that work completes within two seconds. Busy main threads, background throttling, navigation, and process termination can delay or prevent execution. The timer fallback is not an idle period. Keep callbacks small and use existing cancellation on unmount or invalidation.

For large optional computations, process bounded chunks while `deadline.timeRemaining()` permits. Account for `deadline.didTimeout` with a bounded amount of progress rather than running the entire queue. Idle scheduling does not make a single expensive operation non-blocking; use an existing worker when needed. Do not defer DOM updates users are awaiting.

Never add telemetry as part of applying this rule. Preserve consent and data-handling policies for existing analytics.

Adapted from Vercel revision `063bee94c3f4df8453406c830b0a7df0f2860278`. Local adaptation removes the guaranteed-deadline claim and adds cancellation, browser support, and essential-work boundaries. [MDN reference](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestIdleCallback).
