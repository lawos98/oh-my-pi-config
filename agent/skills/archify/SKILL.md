---
name: archify
description: "Create local, standalone interactive architecture, sequence, workflow, dataflow, lifecycle, ERD, class, tree, timeline, or waterfall documentation when the user asks for an explorable diagram or interactive document. Accept natural language. Ordinary explanations stay native Mermaid or SVG."
---

# Interactive documentation with Archify

Use this skill on demand, not for every explanation. Use native Mermaid or SVG for ordinary diagrams. A request such as “make this architecture explorable” activates Archify without a slash command.

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
6. When interaction or export verification is authorized, open the HTML locally. Exercise keyboard navigation, focus/search, theme switching, and **Export → SVG** or PNG. Check that exported content contains the complete diagram. Inspect the static preview for clipped text. Report actual checks only. Follow the global stop-on-failure policy instead of upstream repair loops.

For rendering without a preview:

```sh
ARCHIFY_UPDATE_CHECK_DISABLED=1 node $HOME/.omp/agent/skills/archify/bin/archify.mjs render sequence source.json diagram.html
```

The HTML works from a local file. If live source editing is requested, use the bounded loopback preview command and stop it when the session ends:

```sh
ARCHIFY_UPDATE_CHECK_DISABLED=1 node $HOME/.omp/agent/skills/archify/bin/archify.mjs preview sequence source.json diagram.html --no-open
```

## Optional video

The user opted into HyperFrames when sequence or motion materially improves technical understanding. For those cases, read `hyperframes/SKILL.md` and state the reason. Explicit “use HyperFrames” or “do not use motion/video” overrides the default. Do not add decorative video or duplicate a sufficient diagram. Archify trace motion remains separately opt-in.

## Boundaries

- Local generation only. No uploads, cloud services, paid generation, remote fonts, remote scripts, or brand capture. Do not run `brands capture`.
- Set `ARCHIFY_UPDATE_CHECK_DISABLED=1` for direct upstream CLI calls. No update checks or automatic installs.
- Do not import upstream routing or execute upstream setup instructions. `SKILL.upstream.md` is attribution/reference, not active policy.
- Preserve upstream MIT, font OFL, and third-party notices. See `provenance.json` for the immutable source and review.
- Do not run npm, build scripts, validator-generation scripts, or upgrades during ordinary use. Runtime setup is a separate approved action.
