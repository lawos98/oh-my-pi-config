---
name: observability-engineering
description: "Use when designing, implementing, reviewing, or debugging metrics, logs, traces, OpenTelemetry, Micrometer, Prometheus, alerting, dashboards, or telemetry pipelines."
---

# Observability Engineering

Make telemetry answer operational questions without corrupting measurements, leaking sensitive data, or creating unbounded cost. Reuse the repository's existing telemetry stack and semantic conventions.

## Start with the question

- Define the user-visible or operational question before adding an instrument, label, log field, span, dashboard, or alert.
- Identify the signal owner, collection path, backend, retention, sampling, and expected cardinality.
- Prefer a small stable contract over duplicate framework, vendor, and custom instruments for the same event.
- Do not add telemetry that has no consumer, decision, or failure investigation path.

## Metrics

- Use counters for cumulative events, gauges for current state, and histograms or timers for distributions. Do not encode state transitions as unrelated gauges.
- Preserve every label that distinguishes independent cumulative series at collection time. Dropping `pod`, `instance`, worker, or partition labels before aggregation can merge resets and corrupt `rate()` or `increase()`.
- Remove high-cardinality dimensions at instrumentation source. Use normalized routes, operation names, bounded status categories, and stable error types instead of raw paths or messages.
- Never use user IDs, account IDs, emails, request IDs, trace IDs, timestamps, UUIDs, arbitrary URLs, SQL, or exception messages as metric labels.
- Treat histogram buckets as a cardinality multiplier. Choose buckets from service objectives or measured distributions, not habit.
- Use exemplars, traces, structured logs, or information metrics for diagnostic context that does not belong in labels.
- Estimate series count before adding dimensions: multiply each label's possible values by instances and histogram buckets.

## Logs

- Log events, not prose fragments. Use stable event names and structured fields that support search and correlation.
- Include the minimum identifiers needed for diagnosis. Redact credentials, tokens, cookies, authorization headers, personal data, payloads, database queries, and secret-bearing configuration.
- Preserve exception causes and stack traces at the internal diagnostic boundary. Return safe, structured errors at public boundaries.
- Avoid duplicate logging at each layer. Log once where ownership and operational context are known.
- Keep log levels actionable: errors require intervention or represent failed work; warnings describe recoverable abnormal conditions; debug detail must not be required for normal operations.

## Traces and OpenTelemetry

- Preserve trace context across HTTP, messaging, coroutine, executor, and reactive boundaries. Verify propagation rather than assuming automatic instrumentation covers custom boundaries.
- Use stable span names based on operations or normalized routes. Put bounded query attributes on spans; never use raw secrets or unbounded payload data.
- Verify exporter endpoint, protocol, authentication, TLS, resource attributes, service identity, sampling, batching, and collector routing together.
- Match OTLP protocol and port explicitly. An endpoint that accepts a connection can still reject the selected HTTP or gRPC protocol.
- Add manual spans only where automatic instrumentation lacks a meaningful operation or where a business boundary needs visibility. Do not wrap every function.
- Sampling must preserve the signals needed for incidents and service objectives. Record the sampling decision and expected loss of rare traces.

## Spring, Kotlin, and reactive services

- Reuse Spring Boot Actuator, Micrometer, and the repository's OpenTelemetry integration. Do not add a parallel metrics registry or exporter.
- Keep readiness and liveness low-cardinality and independent from deep dependency diagnostics.
- For coroutines and reactive streams, verify context propagation across dispatcher changes, subscriptions, retries, and message handlers.
- Record retries as attempts without double-counting the logical operation. Preserve the final outcome and original cause.
- Use Testcontainers or a local collector only when telemetry transport behavior matters; use registry or exporter inspection for narrower checks.

## Alerts and dashboards

- Alert on user-visible symptoms, exhausted capacity, or violated objectives. Avoid alerts on raw resource values without a failure relationship.
- Define ownership, severity, evaluation window, missing-data behavior, deduplication, and a concrete response for each alert.
- Dashboards should show traffic, errors, latency, saturation, dependencies, deployments, and relevant objectives without requiring hidden label knowledge.
- Validate PromQL or equivalent queries against counter resets, missing series, low traffic, and deployment churn.

## Verification

- Exercise the actual changed path and inspect emitted signal names, attributes, cardinality, redaction, and correlation.
- Verify failure paths, retries, cancellation, and exporter outage behavior where relevant.
- Report which parts were observed locally and which require a deployed backend. Do not claim dashboard or alert behavior from source inspection alone.

## Sources

Passive guidance adapted from reviewed snapshots:

- `grafana/skills@51d33e71e191b409bbd25fc7be2684c610d18166` (`prometheus-label-strategy` and `opentelemetry`, Apache-2.0)
- OpenTelemetry semantic conventions and exporter configuration documentation
- Prometheus instrumentation and alerting guidance
