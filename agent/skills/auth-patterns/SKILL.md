---
name: auth-patterns
description: Use when implementing, reviewing, testing, or debugging authentication, authorization, password storage, session or token flows, CSRF/CORS, API keys, or secret handling. Keep core guidance stack-neutral and inspect the framework before using integration examples.
---

# Authentication Patterns & Secrets Handling

## Scope and discovery

Authentication is a security boundary. Before changing it, identify the actual credential store, password-hashing library and policy, session or token transport, identity provider, authorization model, browser/API clients, proxy or gateway, and test setup. Read the repository's framework and library versions and follow their current, supported APIs. Do not copy a framework-specific example into a different stack.

The rules in this document are technology-neutral unless a section is explicitly marked conditional.

## Core rules

### Password storage and verification

- Never store or log plaintext passwords. Transmit passwords only over authenticated encrypted transport and compare them only inside the maintained verifier. Never use reversible encryption or a fast general-purpose digest such as MD5, SHA-1, or SHA-256 alone.
- Use a maintained password-hashing library with an adaptive work factor (CPU and, where applicable, memory), such as Argon2id, bcrypt, or PBKDF2 where supported. Choose the algorithm and parameters from the deployed library, current security policy, and measured capacity; this skill does not prescribe a fixed cost.
- Let the library generate a unique salt and store its algorithm and parameters in the encoded hash. Keep any separately managed pepper in a secret manager, not beside the user record.
- Verify through the library's password-verification function, not string equality. Handle unknown accounts and wrong passwords with the same externally visible result and, where needed, comparable verification work to reduce account enumeration and timing leakage.
- If an implementation uses a dummy verification for an unknown account, it must use a valid encoded hash produced by the same deployed algorithm and policy. Never invent or paste a placeholder hash into production code.
- Rehash after a successful login when the encoded parameters no longer meet the current policy. Do not silently truncate passwords; validate input limits without weakening the password policy.

### Login and account recovery

- Return a generic authentication failure for unknown users, wrong passwords, disabled accounts, and similar credential failures unless the product explicitly requires a different response and the disclosure is reviewed.
- Rate-limit and monitor login, password-reset, enrollment, and token endpoints. Use progressive delay or lockout carefully so attackers cannot cheaply deny service to other users.
- Make reset and enrollment tokens single-use, short-lived, scoped, and unguessable. Invalidate sessions or refresh tokens after password changes, recovery, or other credential compromise.
- Require recent or step-up authentication for sensitive changes. Do not send credentials or reset tokens in URLs or logs.

### Sessions, tokens, and API keys

- Choose a session or token design from the actual client and threat model. Server-side sessions should use unpredictable opaque identifiers, bounded lifetime, rotation after login/privilege changes, revocation, and secure storage.
- For browser cookies, set `Secure`, `HttpOnly`, and an intentional `SameSite` policy. Treat cookie-based authentication as ambient authority and pair it with CSRF protection.
- For bearer tokens, validate the signature and allowed algorithm, issuer, audience, time claims, and key identity using a maintained verifier. Keep access tokens short-lived and avoid sensitive data in their claims.
- Protect refresh tokens like credentials: rotate them, detect reuse where supported, revoke them on logout or compromise, and keep signing/encryption keys outside source control with a rotation plan.
- Treat API keys as bearer credentials: scope and expire them, display a secret only at creation when possible, store only a verifier or hash when lookup permits, and support rotation and revocation. Never put an API key in a URL.
- Do not rely on frontend token storage or route guards for security. Assess browser storage choices against XSS and CSRF threats rather than applying a universal rule.

### Authorization

- Enforce authorization on the server for every protected operation. Deny by default and grant the minimum roles, scopes, capabilities, and tenant access needed.
- Check ownership and object-level permissions after loading the target resource, not only at the route or UI boundary. Prevent cross-tenant and confused-deputy access.
- Keep authentication (who the caller is) separate from authorization (what that caller may do), and make privileged actions auditable. Never trust client-supplied roles, tenant IDs, or permission decisions.

### CSRF and CORS

- If authentication uses cookies or another ambient credential, use a framework/library CSRF defense appropriate to the request lifecycle. `SameSite` reduces exposure but is not the only defense for state-changing requests.
- If the API uses an explicit bearer header without ambient credentials, assess CSRF separately, but still protect tokens and state-changing endpoints.
- Configure CORS with an explicit allowlist of trusted origins and only the methods, headers, and credentials required. Never combine wildcard origins with credentials or reflect arbitrary `Origin` values.
- Test preflight, credentialed, rejected-origin, and state-changing requests at the actual boundary, including any gateway that can rewrite headers.

### Secrets and keys

- Keep passwords, signing keys, encryption keys, API keys, client secrets, and database credentials in the repository's supported secret manager or deployment secret mechanism. Never hardcode, commit, print, or put them in query parameters.
- Validate required secrets and key formats at startup without echoing their values. Use separate values per environment, identify active key versions, and document rotation and revocation.
- Redact authorization headers, cookies, credentials, tokens, reset links, and sensitive request bodies from application, access, error, trace, and audit logs. Scrub exception context before returning it to clients.

### Audit and incident evidence

- Record security-relevant events such as successful and failed authentication, recovery, MFA or credential changes, token revocation, authorization denials, and privileged policy changes.
- Include an event type, outcome, actor or subject identifier appropriate to the privacy policy, correlation/request ID, source context, and trustworthy timestamp. Do not record passwords, raw tokens, secret values, or unnecessary personal data.
- Make audit storage access-controlled and tamper-evident where the threat model requires it; define retention and incident-review procedures.

### Testing

- Test credential verification, generic failures, unknown-account behavior, rate limits, reset-token expiry and reuse, session rotation/revocation, token claim validation, key rotation, authorization boundaries, tenant isolation, CSRF/CORS behavior, cookie flags, and log redaction.
- Exercise the actual security boundary in integration tests; a unit test that mocks the verifier or authorization decision cannot prove the filter/middleware configuration.
- Use generated test secrets and isolated test accounts. Do not disable security globally just to make unrelated tests pass, and do not commit real credentials.

## Conditional: Spring Security integration

Use this subsection only after discovery confirms Spring Boot and Spring Security are present. Read the repository's actual Boot/Security version, servlet versus WebFlux starter, session versus resource-server mode, existing security beans, and test dependencies before adapting an example. Do not add a dependency solely to follow this section.

- For servlet MVC, use the component-based `SecurityFilterChain` bean supported by the discovered Spring Security version. For WebFlux, use the matching `SecurityWebFilterChain` and `ServerHttpSecurity` APIs. Keep request rules, CSRF, CORS, and exception handling in the chain that actually serves the boundary.
- Do not introduce the removed `WebSecurityConfigurerAdapter` or copy an API from a different major version. Preserve the repository's existing Kotlin DSL or Java-style configuration.
- Prefer the repository's configured `PasswordEncoder`. If the discovered version and policy support it, `PasswordEncoderFactories.createDelegatingPasswordEncoder()` can provide a delegating format for algorithm migration; select and tune the current policy deliberately rather than hardcoding a cost in application code.
- Use `@EnableMethodSecurity` and method-level authorization only when the repository's design uses it, and still perform object-level and tenant checks in the application/service boundary.
- For an OAuth2 resource server, use the supported framework decoder and issuer/JWK configuration, and validate the claims required by the identity provider. Do not parse or accept JWTs manually.
- For browser sessions, keep CSRF enabled and configure it for the actual cookie/request flow. For stateless bearer APIs, make the CSRF decision from the actual credential transport; do not disable it as a cargo-cult setting.

Servlet MVC example (only when that boundary and API version are present):

```kotlin
@Bean
fun securityFilterChain(http: HttpSecurity): SecurityFilterChain =
    http
        .authorizeHttpRequests { auth ->
            auth.anyRequest().authenticated()
        }
        .build()
```

WebFlux example (only when that boundary and API version are present):

```kotlin
@Bean
fun securityWebFilterChain(http: ServerHttpSecurity): SecurityWebFilterChain =
    http
        .authorizeExchange { auth ->
            auth.anyExchange().authenticated()
        }
        .build()
```

When the repository already includes Spring Security's test support, use the test client matching the boundary (`MockMvc` for servlet MVC or `WebTestClient` for WebFlux) and verify the real chain, CSRF/CORS behavior, authorization, and redaction. Keep framework test helpers as a supplement to end-to-end boundary tests, not a replacement.

## Red flags

- Plaintext, reversible, fast-digest, or fixed-policy password storage
- Password comparison with `==`, `===`, or another direct string comparison
- User-enumerating errors, unlimited credential attempts, or reset tokens that can be reused
- Tokens or secrets in source, URLs, logs, client-visible errors, or unmanaged configuration
- Frontend-only authorization, wildcard credentialed CORS, or cookie authentication without CSRF protection
- A security configuration copied from another framework or major version without checking the repository's actual stack
