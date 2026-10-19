# Service documentation workflow

This site explains how to author and review documentation with Zensical 0.0.71. It does not describe a real service, deployment, or measured runtime behavior.

## Start with evidence

The project maintainer assigns a content owner before service-specific writing begins. That owner decides the audience, checks claims, and approves the intended publication audience. An agent can draft documentation but cannot replace that review.

For each behavioral claim, record the source path and symbol, configuration entry, test, or approved design decision. Include the source revision and review date. Label an inference as an inference. Record unresolved questions instead of inventing components, guarantees, timings, or operational steps. Keep private evidence outside any public build.

## Author, preview, review

1. Inspect the project's existing documentation. Keep its structure and publishing process unless a separate workspace is approved.
2. Write Markdown from the reviewed evidence. Explain the purpose, inputs, outputs, failure behavior, and owner where these are known.
3. Add a static explanation first. Add an interactive diagram or video only when it helps readers understand the same facts.
4. Build and preview from the project's isolated environment. The authoring reference distributed with this workflow gives the commands.
5. Review the generated site, including navigation, media controls, reduced-motion behavior, and any repository subpath.
6. Publish only after separate approval of the destination and content. A successful local build is not permission to upload it.

## What the template provides

The three pages are a working guide to this workflow. [Diagrams and video](media.md) describes local media delivery. [API references](api.md) describes an optional read-only API reference. Code fences contain illustrative integration patterns, not active links to missing assets.

The configuration uses system fonts and normal page navigation. Source files live in `docs/`; generated output lives in `site/`. Keep generated output, the local environment, caches, and private notes out of source reviews and publication inputs. Do not place credentials anywhere under `docs/`: files there can become public assets even when they are absent from navigation.

## Keep documentation current

Review source citations when the corresponding implementation changes. Update the explanation and its media together. If a claim no longer has evidence, remove it or mark it unresolved. Record the date and revision of each substantive content review in the owning project's existing documentation convention.

## Sources

- [Zensical project configuration](https://zensical.org/docs/setup/basics/)
- [Zensical font configuration](https://zensical.org/docs/setup/fonts/)
- [Zensical local preview](https://zensical.org/docs/usage/preview/)
