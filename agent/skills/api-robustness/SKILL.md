---
name: api-robustness
description: >-
  Use when returning errors from APIs. Use when exposing internal errors.
  Use when accepting user input. Use when handling request data.
  Use when trusting external data without validation.
  Use when creating mutation endpoints. Use when trusting frontend to prevent duplicates.
  Use when payments or critical operations can be repeated.
  Use when error responses lack structure.
---

# API Robustness

Three pillars of robust API design: validate input, structure errors, protect mutations.

---

## 1. Input Validation — Trust Nothing

**Iron Rule:** NEVER use external input without explicit validation.

### Detection: Trust Smell
- `val x = request.body.x` without validation
- No schema/type validation at controller boundary
- "The frontend validates it" or "internal API only"

### Correct Pattern (Kotlin/Spring)

```kotlin
// ✅ Validate at boundary with JSR 380
data class CreatePaymentRequest(
    @field:NotNull val userId: String,
    @field:Positive val amount: BigDecimal,
    @field:Size(min = 3, max = 3) val currency: String
)

@PostMapping("/payments")
fun create(@Valid @RequestBody request: CreatePaymentRequest): ResponseEntity<*> { ... }
```

### What to Validate

| Input Type | Validate |
|------------|----------|
| Email | Format, length, required |
| ID | Format (UUID), exists in DB |
| Number | Type, range, precision |
| String | Length, pattern, sanitize |
| Array | Max size, item validation |
| Enum | Member of allowed set |

---

## 2. Error Responses — Expose Nothing

**Iron Rule:** NEVER expose raw error messages or stack traces to clients.

### Detection: Leak Smell
- `throw ResponseStatusException(500, exception.message)` — leaks internals
- Stack traces in HTTP responses
- SQL/Mongo queries in error messages
- Internal IPs or file paths exposed

### Correct Pattern (Kotlin/Spring)

```kotlin
// ✅ Structured error response
data class ErrorResponse(
    val code: String,        // Machine-readable: "VALIDATION_ERROR"
    val message: String,     // Human-readable: "Validation failed"
    val details: Any? = null,
    val requestId: String? = null
)

@RestControllerAdvice
class GlobalExceptionHandler {
    @ExceptionHandler(NotFoundException::class)
    fun handleNotFound(ex: NotFoundException) =
        ResponseEntity.status(404).body(ErrorResponse("NOT_FOUND", ex.message ?: "Not found"))

    @ExceptionHandler(Exception::class)
    fun handleUnknown(ex: Exception): ResponseEntity<ErrorResponse> {
        log.error("Unhandled error", ex)  // Log full details internally
        return ResponseEntity.status(500)
            .body(ErrorResponse("INTERNAL_ERROR", "An unexpected error occurred"))
    }
}
```

### HTTP Status Codes

| Code | When |
|------|------|
| 400 | Bad request, validation errors |
| 401 | Not authenticated |
| 403 | Authenticated but not authorized |
| 404 | Resource not found |
| 409 | Conflict (duplicate, state issue) |
| 429 | Rate limited |
| 500 | Server error (hide details!) |

---

## 3. Idempotency — Safe to Retry

**Iron Rule:** NEVER rely on the frontend or a check-then-save sequence to prevent duplicate
side effects.

### Detection: Duplicate Risk
- Payment, order, message, or account mutations without a server-enforced idempotency key
- Read-before-write duplicate checks that race under concurrency
- Network, client, proxy, queue, or worker retries that can repeat a side effect
- The same key accepted with a different request payload

### Required contract

For each protected operation:

1. Validate and normalize the key, authenticate the caller, and scope the key to the caller and
   operation.
2. Compute a versioned fingerprint from the canonical fields that define the request. Do not
   include transport noise or secrets.
3. Atomically claim `(scope, key)` in storage with a unique constraint or equivalent
   compare-and-set operation. A separate `find` followed by `save` is not atomic.
4. Record the fingerprint, an explicit `IN_PROGRESS` state, lease/expiry information, and the
   owner needed for recovery.
5. For a duplicate:
   - same fingerprint plus `COMPLETED` or terminal failure: replay the stored HTTP status,
     response body, and approved response headers
   - same fingerprint plus `IN_PROGRESS`: return the documented conflict/pending response and
     retry guidance; do not run the operation again
   - different fingerprint: reject the key reuse as a conflict
6. Commit the business effect and terminal idempotency result in one atomic boundary when the
   datastore permits it. Otherwise use the downstream provider's idempotency key plus an
   outbox, saga, or reconciliation record that closes the ambiguous-failure window.
7. Keep terminal results for the documented retry window. Do not use a universal TTL.

```kotlin
when (val claim = idempotencyStore.claim(scope, key, fingerprint)) {
    is Claim.Acquired -> {
        val result = paymentService.process(request, downstreamIdempotencyKey = key)
        val stored = StoredResponse(status = 201, body = result)
        idempotencyStore.complete(claim, stored)
        ResponseEntity.status(stored.status).body(stored.body)
    }
    is Claim.Completed ->
        ResponseEntity.status(claim.response.status).body(claim.response.body)
    is Claim.InProgress ->
        ResponseEntity.status(409).header("Retry-After", claim.retryAfterSeconds.toString()).build()
    is Claim.FingerprintMismatch ->
        ResponseEntity.status(409).build()
}
```

The store operation in this example represents an atomic claim backed by a uniqueness
guarantee. If the process loses ownership after a side effect but before completion, do not
delete the claim and retry blindly. Reconcile the downstream result, renew or take over an
expired lease through a defined policy, then store the terminal response.

### What Needs Idempotency

| Operation | Risk | Protection |
|-----------|------|------------|
| Payments | Double charge | Atomic claim plus downstream idempotency or reconciliation |
| Order creation | Duplicate orders | Atomic claim plus unique business invariant |
| Email/message sending | Duplicate delivery | Outbox/deduplication key and provider semantics |
| Account creation | Duplicate accounts | Unique constraint plus idempotency result |

---

## Quick Reference: All 3 Pillars

| Smell | Pillar Violated | Fix |
|-------|----------------|-----|
| No validation on request body | **Input Validation** | Schema/annotation validation at boundary |
| "Frontend validates" | **Input Validation** | Backend validates regardless |
| Stack trace in HTTP response | **Error Responses** | Log internally, return safe error |
| `exception.message` in response | **Error Responses** | Structured ErrorResponse with safe code |
| Payment endpoint without idempotency | **Idempotency** | Atomic claim, fingerprint, and stored response |
| "Button is disabled" | **Idempotency** | Server-enforced duplicate protection |
| Different error formats per endpoint | **Error Responses** | Global `@RestControllerAdvice` |
