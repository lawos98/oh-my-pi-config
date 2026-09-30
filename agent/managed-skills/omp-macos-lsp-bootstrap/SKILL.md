---
name: omp-macos-lsp-bootstrap
description: "Install and verify Kotlin, Java, Groovy, TypeScript, and JavaScript LSP servers for OpenCode on macOS arm64."
---

# OMP macOS LSP Bootstrap

Use for a macOS arm64 OpenCode workstation needing Kotlin, Java, Groovy, TypeScript, or JavaScript LSP support.

## Install

- Kotlin: `brew tap JetBrains/utils && brew install JetBrains/utils/kotlin-lsp`
- Java: `brew install jdtls`
- TypeScript and JavaScript: `npm install -g typescript-language-server typescript@6`
- Groovy: build `GroovyLanguageServer/groovy-language-server` from a pinned commit with Java 21 and Gradle; copy its shaded JAR to `~/.local/share/groovy-language-server/groovy-language-server-all.jar`.

Do not use floating Groovy source for a reproducible setup. Preserve the upstream Apache-2.0 license and source commit.

## OpenCode configuration

OpenCode has built-in Kotlin, Java, and TypeScript servers when `"lsp": true` is enabled. JavaScript uses the TypeScript server. Add a custom Groovy entry to `~/.config/opencode/opencode.jsonc`:

```jsonc
"lsp": {
  "groovy": {
    "command": [
      "java",
      "-jar",
      "/Users/<user>/.local/share/groovy-language-server/groovy-language-server-all.jar"
    ],
    "extensions": [".groovy", ".gvy", ".gy", ".gsh", ".gradle"]
  }
}
```

Merge with existing config; do not replace unrelated settings.

## Verification

1. Check commands and versions: `kotlin-lsp --version`, `jdtls --help`, `typescript-language-server --version`, `tsc --version`.
2. Confirm the Groovy JAR is non-empty and inspect the pinned source revision.
3. Start each server over stdio and send a real LSP `initialize` request with a valid temporary workspace root. Require a response with `result`, not an error or only a version banner.
4. For TypeScript, install `typescript` in the workspace or configure a valid `tsserver.path`/fallback path; a global install alone may not be found when probing an invalid workspace root.
5. Start a fresh OpenCode process after installation; `lsp reload` does not discover binaries absent at session startup.
6. Remove temporary workspaces and download artifacts after verification.
