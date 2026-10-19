---
name: ktor-backend
description: Implement, review, or extend Kotlin Ktor backend services including routing, serialization, request validation, security, error contracts, persistence, coroutine boundaries, and tests. Use ktor-runtime-troubleshooting for plugin scope/order and request-context failures.
---

# Ktor Backend

Own ordinary Ktor service implementation and contract changes. Diagnose plugin lifecycle, route-scoping, authentication interception and coroutine-context failures with `ktor-runtime-troubleshooting`; do not invent a Spring proxy analogue.

## Establish the actual stack

Read the wrapper, builds/catalogs, application entry points/modules, configuration, engine, routes, serializer, authentication providers, persistence adapters and representative tests. Record the repository's Ktor, Kotlin, coroutine, serializer and JDK versions and version authority. Distinguish server and client plugins. Use version-matched official documentation via Context7; current docs may describe APIs unavailable in this repository. Do not upgrade the framework or adopt experimental authentication/DI APIs just to follow an example.

## Implement the request path

- Reuse module and route organization. Keep route handlers responsible for transport parsing, boundary validation, authorization, invoking application behavior and mapping the response. Keep business invariants in the existing service/domain layer; no mandatory architecture rewrite or one-use interface.
- Trace method, route nesting, path/query/header inputs, content type and accepted response types. Bound body size, pagination and collection inputs using existing controls. Define absent, null, malformed and unsupported-media behavior rather than silently coercing input.
- Configure the existing `ContentNegotiation` serializer at its actual scope. Preserve field names, null/default handling, enum/date representations and published DTO contracts. Do not mix serializer annotation families or add Jackson to a kotlinx.serialization service.
- Validate request DTOs at the receiving boundary using the service's installed Ktor validation mechanism. `RequestValidation` runs on typed `receive<T>()`; map its violations through the existing error handling and distinguish decoding failures from validation failures. If the service already integrates Jakarta Bean Validation, invoke its Validator explicitly, including nested validation; Spring's endpoint `@Valid` mechanism does not run automatically in Ktor. Do not add a validation library just to follow Spring conventions or move request validation into domain/service `require`/`check` guards. Validate path/query inputs at the route boundary too.
- Separate authentication from authorization. Use the existing provider and protected route structure; enforce resource/tenant ownership in the application operation, not only a route label. Keep anonymous/optional access deliberate. Preserve token validation, cookie security, CSRF protection where applicable and restricted CORS; never log credentials or full sensitive payloads.
- Use the repository's `StatusPages` or equivalent boundary mapping for malformed input, validation errors, authentication/authorization, not-found, conflict and internal errors. Return stable sanitized responses, not exception messages or stack traces. Do not swallow cancellation or turn cancellation into an ordinary 500 response.

## Persistence and concurrency

Keep the current datastore adapter, schema evolution, index/query, transaction and consistency conventions. Name the invariant protected by each transaction, conditional write, uniqueness constraint or optimistic version check. Handle concurrent updates and duplicate requests deliberately; do not add retries unless required and safe to repeat. Never hold a database transaction open over remote calls without an explicit existing design.

A suspending route does not make a blocking database or HTTP client nonblocking. Use an explicit repository-supported dispatcher boundary for blocking work and preserve cancellation, transaction and tracing context. Avoid `runBlocking` and detached/global jobs in handlers. Request work belongs to its request lifetime; durable background work needs the existing queue/job owner, not a retained `ApplicationCall`. Give clients finite deadlines and close managed resources through the established application lifecycle. Check engine/version support before asserting client-disconnect cancellation or shutdown semantics.

## Tests and delivery

Add focused tests with the repository's supported `testApplication` setup and actual module/plugin wiring. Cover changed success and failure contracts: malformed payload, invalid DTO, missing/invalid credentials, forbidden resource, serializer behavior and relevant conflict cases. Keep serializer configuration on test clients explicit. Use real datastore integration when behavior depends on query, transaction or wire semantics; do not claim a fake proves persistence correctness. Engine/disconnect behavior may require an existing engine integration test rather than the in-process harness.

Report changed behavior, compatibility impact, tests added/updated and unrun checks separately. Select a narrow repository command for the coordinator; no automatic builds, test runs, formatting or retry loops. Follow the session execution policy.

## Evidence

Original OMP guidance informed by official Ktor documentation, retrieved through Context7 and direct official pages on 2026-10-17. Research pages currently identify Ktor 3.6.0; that is evidence context, not a required application version. No upstream code examples copied.

- [Server plugins and route scope](https://ktor.io/docs/server-plugins.html)
- [Request validation and typed receive](https://ktor.io/docs/server-request-validation.html)
- [Custom plugins, call state and lifecycle](https://ktor.io/docs/server-custom-plugins.html)
- [Testing migration and testApplication](https://github.com/ktorio/ktor-documentation/blob/main/topics/migrating-3.md)
- [Request lifecycle version constraints](https://github.com/ktorio/ktor-documentation/blob/main/topics/whats-new-340.md)

See `provenance.json` for research scope and limitations.
