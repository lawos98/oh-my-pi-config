---
name: jackson-kotlin-serialization-specialist
description: Diagnose Kotlin Jackson DTO serialization, missing versus null fields, constructor defaults, dates, enums, polymorphism, PATCH semantics, and mapper-specific API or message compatibility failures.
license: MIT
metadata:
  source: https://github.com/yalishevant/kotlin-backend-agent-skills
  source_commit: fd0ed521d22efd28221d532c9abab97af0b9bf0e
---

# Jackson Kotlin Serialization Specialist

Own the JSON contract and mapper diagnosis; use `kotlin-spring-backend` for Spring service implementation. Do not replace the repository's serializer or version authority.

## Establish the failing boundary

Read the DTO, sanitized failing and expected payloads, caller, tests, mapper registration/customizers, Spring properties, and build/catalog/platform constraints. Identify the exact mapper used by the endpoint, outbound client, message consumer, cache, or persistence adapter; a global mapper need not configure them all. Record the actual Jackson generation, Kotlin module, Kotlin and Spring Boot versions before selecting APIs or defaults.

## Diagnose in order

1. Check module presence, compatibility and registration, including Kotlin and date/time support appropriate to that Jackson generation. Do not prescribe a module or package from another major version.
2. Trace constructor/creator selection, parameter defaults, annotation use sites, mix-ins and custom deserializers.
3. Compare absent, explicit null, valid value and invalid value for the affected property. Kotlin non-null declarations alone do not establish the wire contract, especially for primitives and coercion.
4. Check naming, inclusion, unknown properties/enums, coercion, date/time zones and precision. `Instant`, `OffsetDateTime` and `LocalDateTime` have different meanings.
5. Check enum representations, value-class scalar/map-key support and stable polymorphic discriminators against the installed versions. Never enable unrestricted default typing for untrusted input.
6. Compare private/client mapper configuration with the application mapper, including copied mappers that can diverge from later customizations.

## Make the smallest compatible fix

- Keep immutable DTOs. Do not add empty constructors, mutable properties or nullable fields merely to silence mapping failures.
- For partial updates, represent absent, explicit null and value deliberately; ordinary nullable properties cannot always preserve all three states.
- Treat defaults, inclusion and coercion as API decisions. Do not mask required-field errors with defaults or turn a typed boundary into an unstructured map.
- Scope a boundary-specific fix to that boundary. Explain the affected consumers before changing global settings.
- Keep transport, domain and persisted contracts distinct where their evolution differs. Preserve existing payload compatibility unless change is authorized.
- In Spring, validate request DTOs with Jakarta Bean Validation annotations and `@Valid` at the receiving endpoint; use the existing boundary error mapping. Deserialization is not business validation, and domain `require`/`check` guards are not request validation.

## Evidence and verification

Add or update focused examples/tests for the affected missing/null/value cases, round-trip or golden JSON, invalid values and compatibility with existing consumers. Check documented schema nullability against actual behavior. Use the real boundary mapper, not a fresh default mapper that bypasses production configuration.

Return observed behavior, intended contract, evidenced cause (or remaining uncertainty), minimal fix, compatibility impact, and a focused verification command selected from the repository. Follow the session execution policy: no automatic Gradle runs, retries, cache clearing or repair loops; report unrun tests as unrun.

## Provenance

Adapted from the pinned upstream `.agents/skills/jackson-kotlin-serialization-specialist/SKILL.md`, reviewed 2026-10-17. Only passive guidance is imported; no runtime or dependency installation. See `LICENSE` and `provenance.json`.
