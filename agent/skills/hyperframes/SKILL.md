---
name: hyperframes
description: "Render local documentation videos when motion or sequence materially improves understanding, or when the user explicitly requests HyperFrames. Supports local MP4 rendering, HTML playback, static explanations, and Markdown thumbnail links. Never decorative video, cloud generation, or paid media."
---

# Documentation video with HyperFrames

Use HyperFrames when the current task authorizes video and temporal order, concurrency, state transitions, or a walkthrough is materially clearer with motion. State the reason briefly. Explicit use/no-use overrides win. Do not add video for decoration or duplicate a sufficient static diagram. Ordinary explanations remain native Mermaid/SVG. Use Archify for requested interactive exploration.

Before approved execution, prepare dependencies from `runtime/package-lock.json`, provide local ffmpeg at `/usr/bin/ffmpeg`, and set `CHROME_PATH` to an approved absolute Chromium executable path. Dependencies, browsers and runtime state are not included in this public snapshot. Installation requires separate approval; this skill does not grant it.

## Local workflow

1. Inspect the source evidence. Write a short storyboard with ordered steps, citations, assumptions, and unknowns. Never invent measurements or timing. Use the same facts as the accompanying static documentation.
2. Author one `index.html` in a dedicated output project directory. It is the editable composition and complete static explanation. Use local assets only, system fonts, and finite native Web Animations API effects. No CDN, remote resources, paid media, account login, TTS, or external generation.
3. Use `examples/request-sequence/index.html` as a runnable reference. The root has `data-composition-id`, `data-duration`, `data-width`, and `data-height`. For native Web Animations without a registered GSAP timeline, declare `data-no-timeline` on the composition host; this selects the supported non-GSAP readiness contract, not a static-only rendering mode. Create finite animations synchronously, pause them, and use `fill: "both"`. HyperFrames seeks their `currentTime`. Do not use timers, randomness, animation callbacks, or independent clocks for render-critical state. Do not add GSAP just for simple emphasis.
4. Keep every step and its meaning visible in the still source. Motion may emphasize order but must not carry exclusive information. Include visible numbered steps, readable contrast, semantic headings, and evidence/assumption labels. Default local HTML to still. Provide keyboard-operable Play/Still controls, honor `prefers-reduced-motion`, and never autoplay the delivered video. For narration, provide captions and an equivalent transcript. Prefer silent labelled sequences.
5. Render through the bounded adapter, not raw `npx` or the upstream router:

```sh
node $HOME/.omp/agent/skills/hyperframes/render.mjs /absolute/path/composition /absolute/path/walkthrough.mp4
```

The adapter uses installed `hyperframes@0.8.169`, one render worker, local ffmpeg, and the existing Chromium. It disables telemetry, updates, skill installation, and the producer health listener. It uses an isolated HOME below the runtime directory and does not inherit credentials. It creates MP4, PNG thumbnail, HTML playback page, and Markdown thumbnail links. The playback page links the original complete static composition. Keep the files together or preserve those relative links when publishing.

6. Link the Markdown thumbnail from the requested document. Add the sequence explanation and evidence there, not only in the video. Deliver the editable source, playback HTML, MP4, and preview. Do not call a file verified until the authorized acceptance check exercises it.

## Acceptance example for the coordinating agent

Local acceptance on 2026-10-17 rendered the corrected example successfully with strict correctness handling unchanged. The non-GSAP host declares `data-no-timeline`; omitting it previously caused a readiness timeout. This command performs actual local rendering and export:

```sh
node $HOME/.omp/agent/skills/hyperframes/render.mjs $HOME/.omp/agent/skills/hyperframes/examples/request-sequence /tmp/omp-documentation-acceptance/walkthrough.mp4
```

Open `/tmp/omp-documentation-acceptance/walkthrough.html`. Confirm that video controls work, the thumbnail link opens it, and the static source shows all three steps without playback. Inspect the video at 1, 3, and 5 seconds: emphasis should move left to right. With reduced motion, the source remains still with complete meaning. This example is explicitly illustrative, not repository evidence.

## Scope and security

Only the render adapter is admitted for normal use. Do not run upstream `init`, `skills`, `upgrade`, `publish`, cloud/lambda commands, media generation, remote capture, or services. No automatic installation or upgrades. Do not import bundled upstream skills as active OMP skills.

Review authored HTML and local assets before rendering: HTML executes JavaScript in the browser and is not an untrusted-content sandbox. The environment controls disable upstream telemetry and update paths, but do not impose an OS network firewall. Never render arbitrary downloaded HTML or include private unrelated files in the project directory. The transient producer file server serves local project assets on loopback. Rendering records local history/cache in the project and isolated HOME.

Source and package identity, dependency licenses, install policy, and residual risks are recorded in `provenance.json`. Preserve the Apache-2.0 license and installed dependency license files.
