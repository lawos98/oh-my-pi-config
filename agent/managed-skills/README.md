# Managed skills

This directory contains the reviewed `service-documentation` workflow. General skills live in [skills](../skills/README.md); this directory does not retain duplicate or obsolete entrypoints.

## Use

Use `service-documentation` for a local-first service documentation site, not an ordinary README edit. It combines source-backed pages, API references and optional diagrams or video. Existing repository documentation conventions take precedence.

Read its [instructions](service-documentation/SKILL.md) and [authoring reference](service-documentation/references/authoring.md). The templates contain:

- Zensical configuration and a pinned, hash-checked Python dependency lock.
- Example pages that explain API and media integration.
- An inert GitHub Pages workflow example. Activation and publication require separate approval.

Copy reviewed templates into the target project without overwriting existing work. Replace instructional examples with real service evidence. Install dependencies only with approval, in a project-local environment. Archify and HyperFrames helpers require their separately prepared runtime; see the [skills guide](../skills/README.md).

## Provenance and limits

This is a locally authored workflow, not an imported third-party skill. Its [provenance](service-documentation/provenance.json) records the Zensical source pin, reviewed platform, historical acceptance observations and unresolved limits. The runtime package is not bundled. Source-local acceptance reports, browser state and generated output are excluded.

Historical observations are not a test of this export. No publication, full accessibility audit or OS-level network isolation is established. See [third-party notices](../../THIRD_PARTY_NOTICES.md) before redistribution or dependency adoption.
