---
name: ktor-runtime-troubleshooting
description: Diagnose Ktor server plugins not running, hook order, merged or nested route scope, missing principals, authentication/authorization placement, consumed bodies, and lost coroutine/request context or cancellation. Use ktor-backend for general service implementation.
---

# Ktor Runtime Troubleshooting

Own Ktor request-pipeline mechanics. Ktor plugins and route hooks are not Spring AOP proxies: adding `open`, all-open or Spring annotations does not fix their execution.

## Gather existing evidence

Read the exact symptom and sanitized request/response, entry point/module loading, engine/version, plugin installations, route tree, provider configuration, custom hooks, coroutine launches/dispatcher transitions and relevant tests. Do not reproduce a user-reported failure just to confirm it. Distinguish absent execution from execution with wrong data or a response already committed.

Trace one affected request from engine through matched route, effective plugin configuration, hook/receive/authentication stages, handler and response transformation. Compare with a working sibling route when available. Report unknown ordering or context transitions as unknown, not inferred facts.

## Diagnose the mechanism

1. **Installation and scope:** Is the module actually loaded? Is this the server plugin, installed at application scope or on the selected route? Is route-scoped installation supported by this plugin/version? Inspect nested and merged route definitions. Official docs state route-specific configuration overrides global configuration, and same-route merged installations use the last configuration; do not assume every installation executes independently.
2. **Hook order:** Identify each hook's lifecycle phase and version-supported ordering contract. Source-code installation order alone is not a universal execution-order rule. Request decoding, validation, authentication, authorization and response transformation happen at different stages. Choose a supported lifecycle hook rather than randomly reordering installs.
3. **Authentication:** Match the configured provider name or version-supported scheme to the protected route. Check nested requirements, optional/anonymous behavior, challenge completion and principal type/provider lookup. A principal read too early can be absent even with correct credentials. `AuthenticationChecked` runs after credential checks; authorization must still handle absent principals and failed/optional authentication. Use newer route-validator or typed-auth APIs only if the repository version supports them. Never weaken authentication to make a route pass.
4. **Body and response flow:** Find earlier body consumers and transformations. Check the requested receive type, serializer and effective validation scope. Do not read a stream again for diagnostics or install body-replay plugins as an unexplained workaround. Check early responses and double responses before changing error mapping.
5. **Coroutine/request context:** Trace parent jobs, dispatcher changes, timeout/cancellation propagation, blocking calls and thread-local assumptions. Keep per-call state in the existing call/context mechanism, not mutable plugin-global variables or a captured call retained after completion. MDC, transactions and security thread-local state need their actual supported propagation; changing dispatcher does not guarantee it.
6. **Lifetime:** Separate request children, application-owned jobs and durable external work. No `GlobalScope`, detached jobs, or `runBlocking` as a repair. Preserve cancellation and resource cleanup. Client disconnect does not universally cancel work: engine, Ktor version and lifecycle configuration matter. Verify support before recommending `HttpRequestLifecycle` or any engine option. Close shared resources at the established application lifecycle boundary, not on each call.

## Repair and evidence

Fix only the evidenced route, hook, provider, scope or coroutine boundary. Do not add a custom plugin when the existing plugin or route structure can express the behavior. Keep general DTO, persistence and service design in `ktor-backend`.

Add a focused regression case through the real installed modules: affected and sibling/nested routes for scope issues, missing/invalid/valid credentials for auth, or explicit context/cancellation assertions for coroutine issues. Test application harnesses do not automatically prove engine disconnect behavior; use the repository's existing engine-level test when that is the claim. Do not add sleeps or retries to hide races.

Return the expected lifecycle, observed path, evidenced root cause, minimal fix, affected route/security/context boundary and one recommended check. No automatic reproduction, test/build/format commands or repeated Gradle checks; obey the coordinator's execution policy and stop after a failed check.

## Evidence

Original OMP guidance researched through Context7 and official pages on 2026-10-17. Current documentation included Ktor 3.6.0 and newer experimental APIs; these are not assumptions about the target application. No source snippets copied.

- [Plugin scope and merged routes](https://ktor.io/docs/server-plugins.html)
- [Hook stages, AuthenticationChecked and call attributes](https://ktor.io/docs/server-custom-plugins.html)
- [Typed receive and validation scope](https://ktor.io/docs/server-request-validation.html)
- [Engine-specific request cancellation introduced in 3.4.0](https://github.com/ktorio/ktor-documentation/blob/main/topics/whats-new-340.md)
- [Experimental authentication API context](https://github.com/ktorio/ktor-documentation/blob/main/topics/whats-new-360.md)

See `provenance.json` for research limitations. The smallest repair must match the repository's installed version, not the research site's latest examples.
