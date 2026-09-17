---
name: humanizer
description: Rewrite user-selected documentation prose to sound natural while preserving every technical fact, term, code block, link target, and intended meaning. Invoke only when the user explicitly asks to humanize, de-AI, or naturalize existing documentation; never apply automatically.
license: MIT
metadata:
  source: "https://github.com/blader/humanizer"
  source_commit: "e2e92e7b4b8229253ed5c8e81dc65463fdeddda5"
  source_version: "2.11.2"
  adaptation: "OpenCode SKILL.md; documentation-only, explicit invocation"
---

# Humanizer for documentation

This is an OpenCode adaptation of `blader/humanizer` at the pinned source commit above. It removes common AI-writing patterns from documentation without changing its technical meaning.

## Invocation gate

Use this skill **only** when the user explicitly requests humanization, naturalization, removal of AI-sounding prose, or removal of chatbot artifacts in supplied or identified documentation.

Do not infer that a document needs humanizing. Do not run this skill as part of ordinary documentation writing, review, editing, release notes, or a pull request. If the request is ambiguous, ask whether the user wants a humanizing rewrite rather than changing the document.

## Non-negotiable preservation rules

1. Preserve all factual and technical claims, including scope, guarantees, limitations, requirements, versions, names, API identifiers, commands, flags, configuration keys, numbers, dates, error messages, and citations.
2. Preserve established technical terminology. Do not replace precise terms with friendlier but less accurate language.
3. Do not invent facts, examples, rationale, attribution, citations, or user intent. If a sentence depends on missing information, retain it or ask for clarification rather than filling the gap.
4. Keep code blocks, inline code, YAML/frontmatter, tables, data, commands, URLs, anchors, file paths, link destinations, and reference definitions unchanged unless the user explicitly requests a change to them.
5. Preserve project documentation conventions and any supplied writing sample. For technical, legal, operational, security, and reference content, favor neutral and precise prose over personality.
6. Do not remove meaningful caveats, compatibility notes, deprecations, migration details, safety guidance, or known limitations merely to make the text shorter.

## What to improve

Look for several patterns in context, not isolated words:

- inflated importance or legacy claims such as "pivotal" or "testament to"
- sales language, generic praise, and unsupported superlatives
- vague attribution such as unnamed experts, reports, or observers
- shallow "highlighting," "ensuring," or "reflecting" clauses that add no fact
- repeated stock transitions, forced three-item lists, and repetitive openings
- wordy substitutes for simple verbs such as `is`, `has`, and `uses`
- formulaic challenge, future-outlook, or generic-positive-ending sections
- unnecessary passive voice when naming the actor improves clarity
- chatbot greetings, offers, praise, knowledge-cutoff disclaimers, and guesses
- filler, stacked hedges, staged candor, fake alternatives, and dramatic fragments
- decorative emoji, excessive bold labels, or title-case headings when they conflict with the surrounding document style

Do not treat perfect grammar, one formal word, one em dash, deliberate repetition, a useful disclaimer, a real alternative, or a quotation as proof of AI writing. Preserve quoted material, proper names, titles, and examples unless the user specifically asks to edit them.

## Rewrite process

1. Read the requested text and nearby context. Identify the document type, audience, existing terminology, and project style.
2. Mark only patterns that make the prose less direct or less useful. Keep every concrete claim and qualification.
3. Rewrite around the main point instead of mechanically swapping flagged words. Prefer direct, active, technically precise sentences.
4. Compare the result against the source. Check that no fact, identifier, constraint, date, number, command, link destination, or citation was added, removed, or weakened.
5. Recheck formatting-sensitive content. Never alter code, commands, metadata, URLs, anchors, or structured data as a side effect of prose editing.

## Response modes

- **Pasted text:** Briefly name the material patterns found, then provide the final rewrite.
- **Named file:** Edit only the requested prose in that file. Leave protected technical and structured content unchanged, then summarize the edit.
- **Embedded documentation task:** Return only the final requested text unless the caller asks for analysis.

## Provenance

Adapted from [blader/humanizer](https://github.com/blader/humanizer), version 2.11.2, pinned to commit `e2e92e7b4b8229253ed5c8e81dc65463fdeddda5`. The upstream skill is based on Wikipedia's "Signs of AI writing" guidance. This adaptation intentionally excludes upstream Claude plugin and CLI-related files and dependencies.

## License notice

Copyright (c) 2025 Siqi Chen.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
