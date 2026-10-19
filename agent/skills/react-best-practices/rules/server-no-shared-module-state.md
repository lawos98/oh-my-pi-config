---
title: Avoid Shared Module State for Request Data
impact: HIGH
impactDescription: prevents concurrency bugs and cross-request data leaks
tags: server, rsc, ssr, concurrency, security, state
---

## Avoid Shared Module State for Request Data

Server module scope is shared across requests in a process. Never use a mutable module variable to hold the current user, tenant, request, or request-specific credentials. Concurrent renders can overwrite it and leak one request's data into another response. This applies to React Server Components and server-rendered client components.

Keep request data local and pass it through the render tree:

```tsx
export default async function Page() {
  const user = await auth()
  return <Dashboard user={user} />
}

function Dashboard({ user }: { user: User | null }) {
  return <div>{user?.name}</div>
}
```

Immutable configuration and static assets can be process-wide. Deliberately shared caches require correct tenant/user/authorization keys, expiration, and ownership; they are not request-local merely because access uses a helper. Use the repository's existing request context or supported framework cache semantics rather than introducing a new global store.

See [Hoist Static I/O](server-hoist-static-io.md) for genuinely static resources. Adapted from Vercel revision `063bee94c3f4df8453406c830b0a7df0f2860278`; local clarification covers tenant and authorization isolation.
