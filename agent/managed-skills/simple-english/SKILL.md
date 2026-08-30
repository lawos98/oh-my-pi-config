---
name: simple-english
description: "Use for writing or rewriting non-normative technical documentation, runbooks, troubleshooting text, incident reports, release notes, and user-facing error text. Do not use for RFC 2119 requirements, legal or compliance text, marketing, code, identifiers, commands, logs, or quoted errors unless the user explicitly requests ASD-STE100."
---

# Simple English for Technical Prose

Write clear technical prose with a pragmatic subset of ASD-STE100 Simplified Technical English.

## Scope

Use this skill for documentation, runbooks, procedures, troubleshooting text, incident reports, release notes, and user-facing error text.

Use pragmatic mode by default. Use strict ASD-STE100 mode only when the user explicitly requests STE, ASD-STE100, or compliance-oriented wording.

Do not apply this skill to marketing, brand voice, casual conversation, source code, code comments that quote code, or normative specifications.

## Preserve Meaning

Never change or invent facts, measurements, causes, dates, names, requirements, or error details.

Preserve these items exactly:

- Code blocks and inline code
- Identifiers, commands, flags, paths, configuration keys, and API names
- Product names and UI labels
- Quoted errors and log lines
- RFC 2119 keywords such as MUST, MUST NOT, SHOULD, SHOULD NOT, MAY, and OPTIONAL

Normative strength is untouchable. Do not replace an RFC 2119 keyword with ordinary prose. Do not strengthen or weaken a requirement.

If the source does not provide an exact error, cause, number, or remedy, keep the statement general. Do not invent specificity to make the text look clearer.

## Classify the Passage

Classify each passage before writing:

- Procedural text tells the reader what to do. Use the imperative mood and one instruction per sentence.
- Descriptive text explains what happened or how something works. Use simple present, simple past, or simple future.

Do not mix instructions and explanations in one list.

## Core Rules

1. Put a condition before its instruction: "If the build fails, read the log."
2. Use active voice unless the actor is unknown and the passage is descriptive.
3. Use one term for one concept throughout the document. Do not rotate synonyms.
4. Use complete grammar. Keep articles and the word "that" when they prevent ambiguity.
5. Avoid contractions, semicolons, present-perfect constructions, decorative clauses, and filler.
6. Delete words that add no fact, such as "simply", "seamlessly", "robust", "powerful", and "it is worth noting".
7. Prefer direct words: "use" instead of "utilize", "before" instead of "prior to", and "if" instead of "in the event that".
8. Put a warning or caution before the risky step. Give the command first and the consequence second.
9. Use a vertical list for more than two steps or items. Do not nest the list unless the structure requires it.
10. Keep sentences short, but never remove necessary technical meaning to satisfy a word limit.

Use 20 words as the target maximum for procedural sentences. Use 25 words as the target maximum for descriptive sentences. These are readability targets in pragmatic mode, not permission to alter facts or normative language.

## Content Patterns

### Error text

State what happened. State the known cause. Then state the safe corrective action. Never expose internal exceptions, stack traces, secrets, queries, or infrastructure details.

### Runbooks

Use one action per step. Put prerequisites and conditions before actions. Put destructive-operation warnings immediately before the affected step.

### Incident reports

Use simple past for completed events. Give exact times, impact, cause, and remediation only when the source provides them. State that information is unknown when it is unknown.

### Release notes

Use one change per entry. Preserve API names, field names, flags, version numbers, and compatibility terms. Mark breaking changes without changing their normative meaning.

## Final Check

Before delivery:

1. Confirm that all facts and untouchable text remain exact.
2. Confirm that every RFC 2119 keyword remains exact.
3. Split avoidably long sentences.
4. Move each procedural condition before its instruction.
5. Remove filler and synonym rotation.
6. Confirm that warnings precede risky actions.
7. Confirm that the rewrite does not claim ASD-STE100 certification.

No AI tool can guarantee ASD-STE100 compliance. For strict work, use the official Issue 9 standard and human review.

## Source and License

Adapted from SimpleEnglish version 1.3.0 at commit `8e8a008a13e4b478f9ccc20ca16e79aef66c0739`:
https://github.com/AminBlg/SimpleEnglish

Copyright (c) 2026 AminBlg

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and sell copies, subject to inclusion of this copyright notice and permission notice.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR CLAIMS, DAMAGES, OR OTHER LIABILITY ARISING FROM THE SOFTWARE OR ITS USE.
