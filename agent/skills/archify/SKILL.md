---
name: archify
description: "Create local, standalone interactive architecture, sequence, workflow, dataflow, lifecycle, ERD, class, tree, timeline, or waterfall documentation for requested exploration or as the default diagram workflow for new service handbooks. Preserve repository conventions. Ordinary small explanations stay native Mermaid or SVG; handbook motion requires an explicit request."
---

# Interactive documentation with Archify

Use this skill for requested exploration and, through `service-documentation`, as the default process/architecture diagram workflow for new service handbooks without an established convention. Do not migrate existing diagrams merely for uniformity. Ordinary small explanations stay native Mermaid/SVG. A request such as “make this architecture explorable” activates Archify without a slash command. For handbook delivery, read [the media contract](../service-documentation/references/media.md).

Before approved execution, prepare the locked sibling HyperFrames runtime and set `CHROME_PATH` to an approved absolute Chromium executable path. Installed dependencies and browsers are not included in this public snapshot. Missing prerequisites require separate installation approval.

## Author and deliver

1. Inspect the relevant implementation and evidence before describing repository behavior. Distinguish observed facts, source-backed relationships, assumptions, and unknowns. Do not portray authored reachability as measured runtime behavior.
2. Select one supported diagram type. Read its schema in `schemas/` and a matching source in `examples/`. Read `references/authoring-contract.md` for the selected authoring contract. Keep one JSON file as the editable source.
3. Set `meta.animation` to `"none"`. Use `"trace"` only when the user requests diagram motion. Preserve the full meaning in the still diagram. Respect reduced-motion preferences and provide text labels, readable contrast, keyboard-accessible controls, and a text explanation.
4. Generate locally with the installed adapter:

```sh
node $HOME/.omp/agent/skills/archify/generate.mjs architecture /absolute/path/system.json /absolute/path/system.html
```

This invokes the pinned renderer and writes standalone interactive HTML, a reduced-motion PNG preview, and a Markdown thumbnail link. JSON stays the only authored diagram source. The preview uses the installed HyperFrames runtime's Puppeteer dependency and the existing Chromium executable. No browser download occurs. Give the user links to the Markdown, HTML, preview, and JSON.

5. Put evidence citations and explicitly labelled assumptions beside the diagram in the requested documentation. The adapter's Markdown is a link fragment, not a substitute for the explanation.
6. When interaction or export verification is authorized, open the actual standalone or embedded delivery. Exercise keyboard navigation, focus/search, theme switching, and **Export → SVG** or PNG. Check complete exports and unclipped previews. Update editable source, generated derivatives, adjacent explanation and affected links together; never change generated meaning independently. Report actual checks only and follow the shared bounded execution policy, not upstream repair loops.

For rendering without a preview:

```sh
ARCHIFY_UPDATE_CHECK_DISABLED=1 node $HOME/.omp/agent/skills/archify/bin/archify.mjs render sequence source.json diagram.html
```

The HTML works from a local file. If live source editing is requested, use the bounded loopback preview command and stop it when the session ends:

```sh
ARCHIFY_UPDATE_CHECK_DISABLED=1 node $HOME/.omp/agent/skills/archify/bin/archify.mjs preview sequence source.json diagram.html --no-open
```

## Optional video

For handbooks, motion and video require an explicit request; the availability of HyperFrames is not permission to add playback. For separately requested video or non-handbook use, read `hyperframes/SKILL.md` and follow its scope and approval boundaries. Preserve complete still/text alternatives. Do not add decorative video or duplicate a sufficient diagram. Archify trace motion remains explicitly opt-in.

## Boundaries

- Local generation only. No uploads, cloud services, paid generation, remote fonts, remote scripts, or brand capture. Do not run `brands capture`.
- Set `ARCHIFY_UPDATE_CHECK_DISABLED=1` for direct upstream CLI calls. No update checks or automatic installs.
- Do not import upstream routing or execute upstream setup instructions. `SKILL.upstream.md` is attribution/reference, not active policy.
- Preserve upstream MIT, font OFL, and third-party notices. See `provenance.json` for the immutable source and review.
- Do not run npm, build scripts, validator-generation scripts, or upgrades during ordinary use. Runtime setup is a separate approved action.
