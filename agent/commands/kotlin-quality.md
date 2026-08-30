---
name: kotlin-quality
description: Check changed Kotlin against the repository's existing ktlint and detekt Gradle tasks, fix source findings, and report verified outcomes.
---

Apply the `kotlin-quality-gates` skill to the current repository.

1. Identify changed `.kt` and `.kts` files and their Gradle modules.
2. Read `.editorconfig`, detekt configuration, and the relevant Gradle task definitions.
3. Discover the actual ktlint and detekt tasks; do not add plugins or assume task names.
4. Run the narrowest applicable ktlint check and detekt task.
5. Fix findings in source without suppressions, exclusions, baseline changes, or configuration weakening.
6. Re-run the failed checks, then run focused tests covering changed behavior.
7. Report exact commands, exit status, and any remaining finding. Do not claim a formatter run proves the checks pass.

Do not modify machine-generated source files or unrelated user changes.
