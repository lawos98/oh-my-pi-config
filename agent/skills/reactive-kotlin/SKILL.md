---
name: reactive-kotlin
description: >-
  Use when working with Kotlin Coroutines, Flow, or reactive programming. Use when
  writing coroutine code with structured concurrency. Use when implementing Spring
  WebFlux endpoints or Ktor coroutines. Use when working with Flow operators,
  backpressure, StateFlow, SharedFlow. Use when handling reactive streams, Mono,
  Flux. Use when refactoring blocking code to coroutines. Triggers: reactive,
  coroutines, flow, webflux, mono, flux, backpressure, structured concurrency,
  coroutine scope, suspend function, kotlin async.
---

# Reactive Kotlin — Coroutines, Flow & WebFlux

## Overview

Patterns for reactive/async Kotlin: coroutines with structured concurrency, Flow for reactive streams, and Spring WebFlux/Ktor integration. This skill covers the reactive paradigm — NOT DDD/hexagonal (see kotlin-spring-hexagonal-service) or IntelliJ APIs (see kotlin-intellij-plugin-dev).

## When to Use

- Writing or reviewing `suspend` functions, `Flow`, `StateFlow`, `SharedFlow`
- Implementing Spring WebFlux endpoints (`Mono`, `Flux`, `WebClient`)
- Designing coroutine scope hierarchies
- Handling backpressure in streaming pipelines
- Refactoring blocking code to non-blocking coroutines
- Debugging coroutine cancellation or lifecycle issues

## Quick Reference

| Concept | Use | Avoid |
|---------|-----|-------|
| Scope | `coroutineScope { }`, `supervisorScope { }` | `GlobalScope.launch` |
| Concurrency | `async { }` + `awaitAll()` | Fire-and-forget `launch` without join |
| Blocking bridge | `runBlocking` (main/test only) | `runBlocking` inside coroutines |
| Thread switch | `withContext(Dispatchers.IO)` | `Thread.sleep()`, blocking I/O on Default |
| Flow terminal | `collect`, `toList()`, `first()` | Ignoring backpressure |
| State | `MutableStateFlow(initial)` | Mutable shared variables |
| Events | `MutableSharedFlow()` | `Channel` for broadcast (use SharedFlow) |

## 1. Flow Operators

### Transformations

```kotlin
flow.map { it.toDto() }
    .filter { it.isActive }
    .flatMapConcat { loadDetails(it.id) }  // Sequential inner flows
    .flatMapMerge(concurrency = 4) { fetch(it) }  // Parallel inner flows
```

### Combining Flows

```kotlin
// Combine latest values from multiple flows
combine(flowA, flowB, flowC) { a, b, c -> merge(a, b, c) }

// Zip pairs elements 1:1
flowA.zip(flowB) { a, b -> Pair(a, b) }
```

### Sharing & State

```kotlin
// Hot flow from cold — shares upstream among collectors
val shared: SharedFlow<Event> = coldFlow
    .shareIn(scope, SharingStarted.WhileSubscribed(5000), replay = 0)

// State holder — always has current value
val state: StateFlow<UiState> = coldFlow
    .stateIn(scope, SharingStarted.WhileSubscribed(5000), UiState.Loading)
```

## 2. Coroutine Scope Management

### Hierarchy Rules

- **`coroutineScope { }`** — Fails fast: any child failure cancels all siblings
- **`supervisorScope { }`** — Isolates failures: one child failure doesn't cancel others
- **`viewModelScope`** / **`lifecycleScope`** — Android; auto-cancelled on lifecycle end
- **Custom scope**: `CoroutineScope(SupervisorJob() + Dispatchers.Default)` — must cancel manually

```kotlin
// Structured concurrency — parent waits for all children
suspend fun loadDashboard(): Dashboard = coroutineScope {
    val user = async { userService.getUser() }
    val orders = async { orderService.getRecent() }
    Dashboard(user.await(), orders.await())
}

// Supervisor — failures are isolated, but cancellation still propagates
suspend fun notifyAll(users: List<User>) = supervisorScope {
    users.map { user ->
        launch {
            try {
                notificationService.send(user)
            } catch (cancelled: CancellationException) {
                throw cancelled
            } catch (failure: Exception) {
                logger.warn("Notification failed for user {}", user.id, failure)
            }
        }
    }.joinAll()
}
```

### Cancellation

```kotlin
// Cooperative cancellation — check isActive or use yield()
suspend fun processLargeFile(file: File) {
    file.useLines { lines ->
        lines.forEach { line ->
            ensureActive()  // Throws CancellationException if cancelled
            process(line)
        }
    }
}
```

## 3. Error Handling in Reactive Streams

### Flow Error Handling

Retry must be upstream of fallback handling. A `catch` that emits a fallback completes normally,
so a downstream `retry` cannot observe the original failure.

```kotlin
sourceFlow()
    .retry(retries = 3) { failure ->
        isClassifiedTransientFailure(failure) && operationIsSafeToRepeat
    }
    .catch { failure ->
        if (failure is CancellationException) throw failure
        logger.error("Stream failed", failure)
        emit(fallbackValue) // Only when fallback is part of the public contract
    }
    .onCompletion { cause ->
        if (cause != null && cause !is CancellationException) {
            logger.warn("Stream completed with an error", cause)
        }
    }
    .collect { process(it) }
```

- Retry only classified transient failures, with bounded attempts and the repository's backoff
  policy.
- Never retry cancellation.
- Do not retry a non-idempotent side effect unless an idempotency key, atomic claim, or equivalent
  deduplication contract makes repetition safe.
- Put retry around the failing upstream operation, not around unrelated downstream processing.
- Use `catch` only for an intentional fallback or error translation. Logging and rethrowing is
  preferable when callers own recovery.

### CoroutineExceptionHandler

```kotlin
// Top-level handler for uncaught exceptions in launch (NOT async)
val handler = CoroutineExceptionHandler { _, e ->
    logger.error("Uncaught coroutine exception", e)
}
val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default + handler)
```

### supervisorScope for Isolation

```kotlin
// Each item is isolated, but parent cancellation still stops the batch
suspend fun processBatch(items: List<Item>): List<Result<Unit>> = supervisorScope {
    items.map { item ->
        async {
            try {
                process(item)
                Result.success(Unit)
            } catch (cancelled: CancellationException) {
                throw cancelled
            } catch (failure: Exception) {
                logger.error("Processing failed for item {}", item.id, failure)
                Result.failure(failure)
            }
        }
    }.awaitAll()
}
```

Do not use `runCatching` around suspending work unless cancellation is explicitly rethrown;
`runCatching` catches `CancellationException`.

## 4. Backpressure Strategies

```kotlin
// Buffer — decouple producer/consumer speeds
flow.buffer(capacity = 64, onBufferOverflow = BufferOverflow.SUSPEND)

// Conflate — drop intermediate values, keep latest
flow.conflate()

// collectLatest — cancel slow collector on new emission
flow.collectLatest { value ->
    val result = heavyComputation(value)  // Cancelled if new value arrives
    updateUi(result)
}

// Sample — emit at fixed intervals
flow.sample(periodMillis = 300)
```

## 5. Spring WebFlux Integration

### Reactive Endpoints (Coroutine Style)

```kotlin
@RestController
class OrderController(private val orderService: OrderService) {

    @GetMapping("/orders/{id}")
    suspend fun getOrder(@PathVariable id: String): OrderDto =
        orderService.findById(id) ?: throw ResponseStatusException(HttpStatus.NOT_FOUND)

    @GetMapping("/orders", produces = [MediaType.APPLICATION_NDJSON_VALUE])
    fun streamOrders(): Flow<OrderDto> = orderService.streamAll().map { it.toDto() }
}
```

### WebClient (Non-Blocking HTTP)

```kotlin
@Component
class PaymentClient(private val webClient: WebClient) {

    suspend fun charge(request: ChargeRequest): ChargeResponse =
        webClient.post()
            .uri("/charges")
            .bodyValue(request)
            .retrieve()
            .awaitBody<ChargeResponse>()

    fun streamEvents(): Flow<ServerEvent> =
        webClient.get()
            .uri("/events")
            .retrieve()
            .bodyToFlow<ServerEvent>()
}
```

### RouterFunction Style

```kotlin
@Configuration
class OrderRouter {
    @Bean
    fun routes(handler: OrderHandler) = coRouter {
        "/api/orders".nest {
            GET("", handler::listAll)
            GET("/{id}", handler::getById)
            POST("", handler::create)
        }
    }
}

@Component
class OrderHandler(private val service: OrderService) {
    suspend fun getById(request: ServerRequest): ServerResponse {
        val id = request.pathVariable("id")
        val order = service.findById(id) ?: return ServerResponse.notFound().buildAndAwait()
        return ServerResponse.ok().bodyValueAndAwait(order)
    }
}
```

### Mono/Flux ↔ Coroutines Bridge

```kotlin
// Mono → suspend
val result: T = mono.awaitSingle()
val resultOrNull: T? = mono.awaitSingleOrNull()

// Flux → Flow
val flow: Flow<T> = flux.asFlow()

// suspend → Mono; do not force Dispatchers.IO unless the body performs unavoidable blocking I/O
val mono: Mono<T> = mono { suspendFunction() }
// Flow → Flux
val flux: Flux<T> = flow.asFlux()
```

## 6. Ktor Coroutines Patterns

```kotlin
fun Application.module() {
    routing {
        get("/users/{id}") {
            val id = call.parameters["id"] ?: return@get call.respond(HttpStatusCode.BadRequest)
            val user = userService.findById(id)  // suspend function — native support
            call.respond(user ?: HttpStatusCode.NotFound)
        }

        // Streaming response
        get("/events") {
            call.respondTextWriter(contentType = ContentType.Text.EventStream) {
                eventFlow.collect { event ->
                    write("data: ${json.encodeToString(event)}\n\n")
                    flush()
                }
            }
        }
    }
}
```

## 7. Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| `GlobalScope.launch` | Unstructured — leaks coroutines, no cancellation | Use scoped `launch` within `coroutineScope`/service scope |
| `runBlocking` inside coroutines | Blocks thread, defeats purpose | Use `suspend` functions and `withContext` |
| `.block()` on Mono/Flux | Blocks reactive thread | Use `awaitSingle()`, `asFlow()` |
| `Thread.sleep()` in coroutine | Blocks thread | Use `delay()` |
| Catching `CancellationException` | Breaks structured concurrency | Rethrow `CancellationException` always |
| `flow { while(true) { emit(...) } }` without delay | Busy loop, no backpressure | Add `delay()` or use `callbackFlow` |
| Mutable shared state without mutex | Race conditions | Use `Mutex`, `StateFlow`, or `Channel` |
| `async` without `await` | Silent failure — exceptions lost | Always `await()` or use `launch` with handler |

## Common Mistakes

1. **Forgetting `flowOn`** — Flow operators run in collector's context by default. Use `flowOn(Dispatchers.IO)` for upstream I/O:
   ```kotlin
   flow { emit(blockingRead()) }
       .flowOn(Dispatchers.IO)  // Only affects upstream
       .collect { updateUi(it) }  // Runs in collector's dispatcher
   ```

2. **SharedFlow replay confusion** — `replay = 0` means new subscribers miss past events. Use `replay = 1` for state-like behavior, or use `StateFlow`.

3. **Leaking coroutine scope** — Always cancel custom scopes in `close()`/`destroy()`:
   ```kotlin
   class MyService : AutoCloseable {
       private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default)
       override fun close() { scope.cancel() }
   }
   ```
