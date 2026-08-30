---
name: gitnexus-analyze
description: Index the current repository with GitNexus and report the resulting graph status.
---

Run GitNexus analysis in the current repository root.

1. Verify `gitnexus --version` succeeds.
2. Stop if `.gitnexusrc` exists or if `GITNEXUS_EMBEDDING_URL`, `GITNEXUS_EMBEDDING_MODEL`, or `GITNEXUS_EMBEDDING_API_KEY` is set. Check only whether a variable exists; never print its value.
3. Run `DO_NOT_TRACK=1 SCARF_ANALYTICS=false GITNEXUS_LBUG_EXTENSION_INSTALL=load-only gitnexus analyze --index-only` with only the safe indexing arguments supplied after this command.
4. State before execution that indexing creates or updates `.gitnexus/`, the GitNexus global registry, and possibly the repository's local Git exclude file. It must not inject `AGENTS.md`, `CLAUDE.md`, or skill files.
5. Do not add `--skills`, remove `--index-only`, update agent files, enable embeddings, publish an index, or install packages or database extensions.
6. Do not invent flags or remove the privacy and load-only environment variables.
7. Report indexed file count, duration, warnings, and failures from the actual output.
8. On success, run `gitnexus status` and report the index state.
