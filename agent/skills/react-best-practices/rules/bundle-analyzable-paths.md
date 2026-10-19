---
title: Prefer Statically Analyzable Paths
impact: HIGH
impactDescription: avoids accidental broad bundles and file traces
tags: bundle, nextjs, vite, webpack, rollup, esbuild, path
---

## Prefer Statically Analyzable Paths

When a bundler cannot determine an import target, it may include a broad file set or reject the import. Prefer literal imports behind an explicit map:

```typescript
const pageModules = {
  home: () => import('./pages/home'),
  settings: () => import('./pages/settings'),
}

async function loadPage(name: keyof typeof pageModules) {
  return pageModules[name]()
}
```

Putting path strings in a map and passing a computed string to `import()` does not necessarily make imports analyzable. Validate external names at the existing boundary; do not bypass typing with casts.

For server file tracing, keep the allowed final paths explicit when computed paths widen the traced file set:

```typescript
const directory = contentKind === 'blog'
  ? path.join(process.cwd(), 'content/blog')
  : path.join(process.cwd(), 'content/docs')
```

Apply this only where the installed build tool's behavior warrants it. Preserve supported targets and file-access restrictions. Verify actual bundle/tracing evidence under the global execution policy; do not claim improved size from source shape alone.

Sources: [Next.js output tracing](https://nextjs.org/docs/app/api-reference/config/next-config-js/output), [Vite features](https://vite.dev/guide/features.html). Adapted from Vercel revision `063bee94c3f4df8453406c830b0a7df0f2860278` with local typing and verification safeguards.
