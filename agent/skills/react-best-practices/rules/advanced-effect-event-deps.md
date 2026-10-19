---
title: Do Not Put Effect Events in Dependency Arrays
impact: LOW
impactDescription: keeps reactive dependencies explicit without resubscribing for effect events
tags: advanced, hooks, useEffectEvent, dependencies, effects
---

## Do Not Put Effect Events in Dependency Arrays

When the installed React version supports `useEffectEvent`, omit the returned Effect Event from an Effect's dependency array. Keep the actual reactive values as dependencies. An Effect Event is not a general-purpose stable callback and must not be used to hide genuine dependencies.

```tsx
import { useEffect, useEffectEvent } from 'react'

function ChatRoom({ roomId, onConnected }: {
  roomId: string
  onConnected: () => void
}) {
  const handleConnected = useEffectEvent(onConnected)

  useEffect(() => {
    const connection = createConnection(roomId)
    connection.on('connected', () => handleConnected())
    connection.connect()
    return () => connection.disconnect()
  }, [roomId])
}
```

Use Effect Events only for non-reactive logic called from Effects or callbacks established by those Effects, following the installed React and Hooks lint versions. Do not pass them as general callbacks to children, call them during rendering, or suppress lint errors. Do not upgrade React merely to apply this pattern; preserve the repository's supported alternative when this API is unavailable.

[React reference](https://react.dev/reference/react/useEffectEvent#effect-event-in-deps). Adapted from Vercel revision `063bee94c3f4df8453406c830b0a7df0f2860278` with explicit version and invocation boundaries.
