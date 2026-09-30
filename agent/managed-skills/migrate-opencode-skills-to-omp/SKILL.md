---
name: migrate-opencode-skills-to-omp
description: "Use when copying user-authored OpenCode skills into OMP's agent skill directory while preserving supporting files and verifying parity."
---

# Migrate OpenCode skills to OMP

1. Treat `/Users/jakub.spolnik/.config/opencode/skills/<name>` as the source and `/Users/jakub.spolnik/.omp/agent/skills/<name>` as the target.
2. Inspect both directories before editing. Existing target skills may differ; do not overwrite unrelated skills.
3. Copy each requested skill directory recursively, preserving `SKILL.md`, frontmatter, and any supporting files such as `README.md` or `codemap.md`.
4. Verify each migrated source/target tree with `diff -rq` or equivalent. Confirm expected `SKILL.md` count and supporting files.
5. Report exact migrated skill names and mention that OpenCode may need a restart or next run to load changes.

Use direct filesystem copy only for explicit migration requests. Do not alter skill contents unless requested.
