---
title: Parallel Nested Data Fetching
impact: HIGH
impactDescription: lets each independent item's dependent work start when ready
tags: server, rsc, parallel-fetching, promise-chaining
---

## Parallel Nested Data Fetching

For independent items, chain dependent work inside each item's promise instead of awaiting every first-stage result before beginning any second-stage work.

```typescript
const authors = await Promise.all(
  chatIds.map(id => getChat(id).then(chat => getUser(chat.author)))
)
```

Each author fetch starts when its own chat is ready. A slow chat does not block the others' author fetches. The dependency `getChat` then `getUser` remains sequential for each item.

Use this only when operations are independent across items. Preserve input/result ordering, authorization, error semantics, cancellation, and required side-effect ordering. For unbounded collections or constrained downstream services, retain the repository's batching or bounded-concurrency mechanism; do not start unlimited requests. Do not introduce partial-success behavior just to hide a failed request.

Adapted from Vercel revision `063bee94c3f4df8453406c830b0a7df0f2860278`; local adaptation adds concurrency and observable-contract safeguards.
