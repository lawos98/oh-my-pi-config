# Diagrams and video

This page describes documentation media, not a real service's architecture. A static explanation is the primary source for readers who cannot use an interactive diagram or play a video.

## Interactive diagrams

Use the existing local Archify skill when readers need to explore a diagram. Read its schema and authoring contract before creating the editable JSON. Cite the evidence beside the diagram and label assumptions. Default to no animation.

The installed adapter produces standalone HTML, a PNG preview, and a Markdown link fragment. Its local invocation is:

```sh
node $HOME/.omp/agent/skills/archify/generate.mjs architecture /absolute/path/system.json /absolute/path/system.html
```

Copy only reviewed deliverables into `docs/assets/`, including editable source if it is safe to publish. Keep the adapter's generated Markdown link fragments outside `docs/`: `system.md` would render to `system.html` and overwrite the interactive asset. Paste the useful links into a page with a different basename. Preserve relative links among the HTML, images and editable sources. The following example is inert until the named files exist:

```markdown
[![Static overview of the documented components and their connections](assets/system.png)](assets/system.html)

[Open interactive diagram](assets/system.html) · [Read editable source](assets/system.json)
```

Prefer the preview and direct link. If an inline view is useful, use a descriptive frame title and retain the direct link and text explanation outside the frame:

```html
<iframe src="assets/system.html" title="Interactive component diagram"
        width="100%" height="560" loading="lazy"></iframe>
<p><a href="assets/system.html">Open the diagram in a separate page</a></p>
```

Only embed reviewed local HTML. Same-origin HTML can execute scripts with the site's privileges. An iframe is not a security boundary for arbitrary downloaded content. Keep the site free of secrets and authentication state. Check keyboard navigation, focus, contrast, exports, and reduced-motion behavior when verification is authorized.

## Video walkthroughs

Use the existing HyperFrames skill when temporal order or concurrency adds useful information. State why motion helps. Its storyboard and still composition must explain every step without playback. Keep sources and assets local. Do not install a second runtime or use cloud rendering.

```sh
node $HOME/.omp/agent/skills/hyperframes/render.mjs /absolute/path/composition /absolute/path/walkthrough.mp4
```

The adapter produces the MP4, thumbnail, playback HTML, and Markdown links. Keep its Markdown link fragment outside `docs/` to avoid overwriting the same-named playback HTML during the site build. Keep the static composition at the path referenced by the playback HTML. Inspect those references before copying the files into the site.

A direct video embed can use this pattern once the reviewed files exist:

```html
<video controls preload="metadata" poster="assets/walkthrough.png"
       width="960" style="max-width:100%;height:auto"
       aria-label="Documentation authoring sequence">
  <source src="assets/walkthrough.mp4" type="video/mp4">
  <p><a href="assets/walkthrough.mp4">Download the walkthrough</a></p>
</video>
<p><a href="assets/composition/index.html">Read the complete static walkthrough</a></p>
```

Do not add autoplay or looping. For narrated video, add reviewed captions with a `track` element and provide an equivalent transcript. Silent labelled steps still need the complete static explanation. The alternative must remain available outside the video element, not only as a browser fallback.

## Paths and delivery

These patterns assume this page is `media.md` and `use_directory_urls = false`. It becomes `media.html`, beside `assets/`. Use relative paths without a leading slash. If a page moves into a subdirectory, adjust raw HTML paths from the generated page location. Markdown links to other pages use their `.md` source paths.

Keep the template's normal page navigation. Do not enable instant navigation without checking embedded scripts across page changes. Review the complete generated output before publication, including source JSON, HTML, and media metadata.
