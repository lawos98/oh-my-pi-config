---
name: learn
description: Extract verified lessons from this conversation, then ask before saving memory or creating a reusable skill.
argument-hint: "[topic or focus within this conversation]"
---

Learn from the current conversation. Optional focus: $ARGUMENTS

1. Read `skill://lesson-learned` and use its evidence-based reflection workflow. Use only this conversation and relevant current files; do not consult other sessions or scan unrelated history. Separate observations, decisions, failed attempts, and uncertainties. Never treat an applied edit or unrun check as verified behavior.
2. Present a short numbered list of useful lessons: what happened, the supporting evidence, and what to do next time. If there is no durable lesson, say so and stop without writing. Do not invent lessons to fill a quota.
3. Distinguish durable facts/preferences from reusable procedures and temporary task state. Check likely existing memories or skills for overlap before proposing persistence; use native recall and the current skill catalog, not full transcript searches. Do not expose credentials or copy private transcripts, proprietary code, or sensitive details into a general skill.
4. Show the exact proposed memory text and/or the proposed skill name, trigger, and complete compact procedure. Recommend the appropriate destination. Ask exactly one question with real applicable options: save the proposed facts, create the proposed skill, both, or keep the reflection only. Omit destinations that do not fit. Wait for an explicit choice before calling `learn`, `retain`, or `manage_skill` or writing any file. Invoking `/learn` alone is not permission to persist its output.
5. Save only the approved content. Use native memory tools for durable facts in the current project's scope; do not change memory/autolearn settings or claim global scope. Use `manage_skill` to create an approved reusable procedure in isolated managed skills, never by writing directly into that directory. If an existing skill already covers it, recommend using it instead. An update requires showing the proposed change and obtaining approval; do not overwrite user-authored or plugin-owned skills. If a procedure needs unavailable tools, dependencies or auxiliary files, explain the missing requirement instead of saving an incomplete skill.
6. Report what was actually saved, its scope or returned path, and any failure. A created managed skill is not automatically selected by the launcher: role/global selection needs separate explicit approval. Do not change `profiles.yml`, global rules, or other configuration as part of this command. Do not commit, publish, or start automatic post-stop learning.

Keep questions and explanations short. Preserve the user's existing passive-learning configuration; the approval gate above applies to this command's explicit persistence actions.
