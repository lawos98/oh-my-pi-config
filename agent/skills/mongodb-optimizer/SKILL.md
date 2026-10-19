---
name: mongodb-optimizer
description: >-
  Use when optimizing MongoDB queries or aggregation pipelines. Use when
  designing indexes, analyzing slow queries or explain plans, tuning data-access
  patterns in the repository's established driver/framework, or improving
  aggregation stages like $lookup, $group, $facet, $unwind, $merge, and $out.
  Triggers: slow MongoDB query, query performance, index optimization,
  collection scan, aggregation pipeline, pipeline optimization, explain plan,
  stage ordering.
---

# MongoDB Optimizer

Expert guidance for MongoDB query and aggregation optimization. Apply the repository's established driver and framework; the Kotlin/Spring/MongoOperations snippets below are examples for repositories that establish that stack.

## Repository and deployment context

Before tuning:

- Inspect build/dependency files, data-access code, application configuration, deployment manifests, and operational runbooks to identify the driver, server version, provider, topology, and connection settings.
- Determine whether the deployment is managed (including Atlas), self-managed, or another supported environment. Never assume a specific vendor, provisioning platform, replica-set shape, fixed datacenter layout, or any other deployment topology.
- Verify transaction and sharding capabilities from the server topology/version, driver, and deployment policy; do not infer availability from a provider name.
- Determine index ownership, automatic-index policy, and rollout location from repository/deployment evidence. Indexes may be managed by startup code, migrations, infrastructure, or an operational process; do not prescribe a fixed DDL directory or default.
- Let repository evidence override generic guidance; when a repository establishes a scoped stack convention, that scoped skill governs it.

## Core principle
Reduce the amount of work MongoDB does as early as possible:
- narrow documents with indexes, `$match`, and projections
- keep compound indexes aligned to the query shape
- filter before expensive stages like `$lookup`, `$unwind`, `$group`, and `$sort`

## Client and connection management

- Reuse one MongoDB client per connection identity (URI, credentials, TLS, and relevant client options) within each application process; do not create a client per request or operation.
- Before sizing a pool, inspect the exact deployment topology—standalone, replica set members,
  or sharded routers—and the driver's per-server pool multiplication.
- Derive pool sizing from measured workload, application instances, concurrency/request limits,
  server connection limits, topology, and driver behavior. There is no universal pool number.
- Any pool recommendation must account for the deployed driver version and its per-server pools,
  wait queue, connection creation/handshake limits, timeout semantics, and monitoring behavior.
- Do not change pool limits until a time-aligned comparison covers client checkout wait/failures,
  client pool utilization, server current/active/available connection metrics, application
  instance count, and operation latency.
- Diagnose slow operations with explain plans, profiling, server load, and resource metrics before increasing pools; more connections do not make expensive operations cheaper.

## Query optimization

### ESR rule: Equality → Sort → Range

Order compound index fields as:
1. **Equality** fields first (`field: value`)
2. **Sort** fields next (`orderBy` fields)
3. **Range** fields last (`gt`, `lt`, `lte`, `gte`, `in`)

```kotlin
// status == "ACTIVE" AND createdAt <= now ORDER BY priority DESC
mongoOperations.indexOps(JobEntity::class.java)
    .ensureIndex(
        Index()
            .on(JobEntity::status.name, Sort.Direction.ASC)
            .on(JobEntity::priority.name, Sort.Direction.DESC)
            .on(JobEntity::createdAt.name, Sort.Direction.ASC)
            .named("idx_status_priority_createdAt")
    )
```

### Query anti-patterns

- ❌ Index every field individually
- ❌ Put range before sort in compound indexes
- ❌ Add indexes without measuring write cost, storage, selectivity, and actual query use
- ❌ Index large arrays without limit analysis
- ❌ Use non-anchored `$regex` when you expect index usage
- ❌ Rely on index intersection for complex queries

### High-value query patterns

#### Covered queries

```kotlin
val query = Query(JobEntity::status isEqualTo "PENDING")
    .fields().include(JobEntity::id).include(JobEntity::nextProcessAt)
```

#### Projection

```kotlin
val query = Query(AccountEntity::userId isEqualTo userId)
query.fields()
    .include(AccountEntity::userId)
    .include(AccountEntity::status)
    .exclude(AccountEntity::details)
```

#### Atomic claim / lock pattern

```kotlin
val query = Query.query(
    JobEntity::nextProcessAt lte now(clock)
).maxTimeMsec(mongoSettings.maxTimeCandidateQueryMS)

val update = Update()
    .set(JobEntity::nextProcessAt, now + lockDuration)
    .inc(JobEntity::retry, 1)

val options = FindAndModifyOptions.options()
    .returnNew(false)
    .upsert(false)

mongoOperations.findAndModify(query, update, options, JobEntity::class.java)
```

#### Bulk operations

```kotlin
mongoOperations.insertAll(entities)
// Prefer this over entities.forEach { mongoOperations.save(it) }
```

#### Timeout control

```kotlin
val query = Query(criteria).maxTimeMsec(5000)
```

### Slow query checklist

1. Check explain plan for `COLLSCAN`
2. Confirm the intended index is selected
3. Compare scanned documents vs returned documents
4. Look for in-memory sort stages
5. Verify projection is trimming large documents
6. Rework the query to fit ESR if possible

### Index rollout convention

Define indexes through the repository's established owner: a versioned migration, application startup, infrastructure/deployment, or an approved operational process. Do not assume a particular DDL filename or directory. Create and validate indexes before deploying dependent query shapes, following the repository's rollout and rollback procedure.

```kotlin
val jobIndex = mongoOperations.indexOps(JobEntity::class.java)
    .ensureIndex(
        Index()
            .on(JobEntity::userId.name, Sort.Direction.ASC)
            .on(JobEntity::status.name, Sort.Direction.ASC)
            .named("idx_userId_status")
    )
```

## Aggregation optimization

### Core principle

Push filtering and projection upstream. Reduce document count and size before expensive stages.

### Stage ordering

| Priority | Stage | Why |
|----------|-------|-----|
| 1st | `$match` | Filters early and can use indexes |
| 2nd | `$project` / `$addFields` | Reduces document size before joins or grouping |
| 3rd | `$lookup` | Join after filtering to minimize scans |
| 4th | `$unwind` | Expand arrays only after reducing document count |
| 5th | `$group` | Aggregate on the smallest possible dataset |
| 6th | `$sort` | Sort the reduced result set |
| 7th | `$limit` / `$skip` | Apply final pagination |

```kotlin
val agg = Aggregation.newAggregation(
    Aggregation.match(Criteria.where("status").`is`("ACTIVE")),
    Aggregation.project("userId", "category", "amount"),
    Aggregation.lookup("users", "userId", "_id", "user"),
    Aggregation.group("category").sum("amount").`as`("total")
)
```

### $lookup optimization

#### Equality form

```kotlin
Aggregation.lookup("foreignCollection", "localField", "foreignField", "outputArray")
```

- uses an index on `foreignField` if available
- returns an array of matching documents

#### Pipeline form

```kotlin
LookupOperation.newLookup()
    .from("orders")
    .let(ExposedFields.Synthetic.syntheticField("uid", "\$userId"))
    .pipeline(
        Aggregation.match(
            AggregationExpression { _ ->
                Document("\$expr", Document("\$and", listOf(
                    Document("\$eq", listOf("\$\$uid", "\$customerId")),
                    Document("\$gte", listOf("\$createdAt", cutoffDate))
                )))
            }
        ),
        Aggregation.project("orderId", "total")
    )
    .`as`("recentOrders")
```

Use pipeline form when you need to filter inside the join, project only required fields, or express complex conditions.

#### $lookup anti-patterns

- ❌ `$lookup` before `$match`
- ❌ Large output arrays without a plan
- ❌ Repeating multiple lookups against the same collection when one pipeline would do

### $group accumulator efficiency

| Accumulator | Cost | Notes |
|-------------|------|-------|
| `$sum`, `$avg`, `$min`, `$max` | Low | Constant memory per group |
| `$first`, `$last` | Low | Order-dependent; needs prior `$sort` |
| `$push` | High | Unbounded array growth |
| `$addToSet` | Higher | Deduplication overhead + unbounded growth |

```kotlin
Aggregation.group("category")
    .count().`as`("total")
    .sum("amount").`as`("totalAmount")
    .avg("amount").`as`("avgAmount")
```

Use `$push` / `$addToSet` only for known-small groups.

### $facet vs multiple aggregate() calls

Use `$facet` when the pipelines share the same filter and the results stay small. It scans once, but keeps all facets in memory and is capped by the 16MB combined result limit. Use separate calls when filters or index needs differ.

### $merge / $out for materialized views

#### $out

```kotlin
val agg = Aggregation.newAggregation(
    Aggregation.match(Criteria.where("createdAt").gte(startOfMonth)),
    Aggregation.group("category").sum("revenue").`as`("totalRevenue"),
    Aggregation.out("monthly_category_stats")
)
```

Replaces the target collection.

#### $merge

```kotlin
val mergeOp = MergeOperation.builder()
    .intoCollection("daily_stats")
    .on("_id")
    .whenMatched(MergeOperation.WhenDocumentsMatch.replaceDocument())
    .whenNotMatched(MergeOperation.WhenDocumentsDontMatch.insertNewDocument())
    .build()

val agg = Aggregation.newAggregation(
    Aggregation.match(Criteria.where("updatedAt").gte(lastRunTime)),
    Aggregation.group("date", "category")
        .sum("amount").`as`("total")
        .count().`as`("count"),
    mergeOp
)
```

Prefer `$merge` for incremental updates because it keeps the target collection available and processes only changed documents.

### Aggregation anti-patterns

| Anti-pattern | Problem | Fix |
|-------------|---------|-----|
| `$unwind` before `$match` | Explodes documents then filters | Match first |
| Unnecessary `$project` between stages | Extra overhead | Project only when trimming matters |
| `$lookup` without an index on the foreign field | Collection scan per document | Index the join field |
| `$group` with unbounded `$push` | Memory exhaustion | Limit earlier or split the query |
| `$sort` on a large unindexed dataset | Disk spill, slow execution | Pre-filter or allow disk use |
| `$match` after `$project` removes the matched field | Empty results | Keep downstream fields intact |
| Multiple `$unwind` without intermediate `$match` | Cartesian explosion | Filter between unwinds |

## MUST DO

- Follow ESR ordering for compound indexes
- Put `$match` as early as possible
- Use projections to trim large documents
- Set `maxTimeMsec` (or the established driver's equivalent operation max-time) on production workloads
- Use `allowDiskUse(true)` for large sorts when needed
- Prefer pipeline-form `$lookup` when joins need filtering or projection
- Use `findAndModify` for atomic claim / lock patterns
- Use `insertAll` for bulk inserts when supported by the established stack
- Use `$merge` over `$out` for incremental materialized views
- Profile with `.explain()` or equivalent before and after changes
- Keep index definitions in the repository's established schema-change owner

## MUST NOT DO

- Don't rely on transactions or sharding capabilities until the server topology/version, driver, and deployment policy have been verified
- Don't create or change indexes outside the repository's established schema-change owner
- Don't use `$where` or JavaScript expressions in queries
- Don't rely on index intersection for complex queries
- Don't use `$unwind` just to flatten and then group everything back
- Don't sort before matching
- Don't use aggregation for simple find + projection queries
- Don't impose `MongoRepository` or `MongoOperations` when the repository has established a different data-access style
