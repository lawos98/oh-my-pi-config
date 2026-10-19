---
name: omp-kotlin-lsp-bootstrap
description: Install or upgrade the official JetBrains Kotlin LSP for OMP on Linux and verify it in a fresh session.
---

# OMP Kotlin LSP Bootstrap

1. Read the official Kotlin LSP latest release and release notes. Select the standalone archive for the workstation architecture.
2. Download the archive and its official SHA-256 sidecar over HTTPS. Compute the local SHA-256 and stop on any mismatch.
3. Extract into a versioned user-owned directory such as `~/.local/share/kotlin-lsp/kotlin-server-<version>`.
4. Create a PATH-visible symlink named `kotlin-lsp` that points directly to `<version>/bin/intellij-server`. Do not target `kotlin-lsp.sh`; it is deprecated. The archive contains its own JBR.
5. Verify `kotlin-lsp --version` and `kotlin-lsp --help`; confirm `--stdio` is supported.
6. Restart OMP or launch a fresh OMP process. An existing session's LSP registry may not discover a binary installed after session startup, and `lsp reload` only reloads servers already configured for that session.
7. In a temporary minimal Gradle Kotlin project, use a fresh OMP process to run LSP diagnostics on a valid `.kt` file. Success means the diagnostics request runs and returns no diagnostics—not merely that the executable prints a version.
8. Remove temporary project and download artifacts after the smoke test.
