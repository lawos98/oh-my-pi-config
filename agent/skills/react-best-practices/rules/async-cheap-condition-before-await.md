---
title: Check Cheap Conditions Before Async Flags
impact: HIGH
impactDescription: avoids unnecessary async work when a synchronous guard already fails
tags: async, await, feature-flags, short-circuit, conditional
---

## Check Cheap Conditions Before Async Flags

Evaluate a cheap synchronous condition before starting asynchronous work that is needed only when that condition holds.

```typescript
if (someCondition) {
  const enabled = await getFlag()
  if (enabled) {
    performEnabledAction()
  }
}
```

Unlike fetching the flag before the `if`, this avoids the request when the local condition is false. See [Defer Await Until Needed](async-defer-await.md).

Preserve the original order when the condition depends on the result, the call has required side effects, or evaluation order is part of the observable contract. Do not skip authorization, audit events, or required validation merely to save work. This rule is not permission to suppress an error that callers must receive.

Adapted from Vercel React Best Practices, revision `063bee94c3f4df8453406c830b0a7df0f2860278`; local addition clarifies required side effects and authorization boundaries.
