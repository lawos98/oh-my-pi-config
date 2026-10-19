# Local artwork, Aseprite and Penpot

The user chose local ComfyUI with downloaded models for subscription-free generation. Follow [comfy-local.md](comfy-local.md) for that installed route. Use Aseprite for controlled cleanup/animation and source preservation, and Penpot for editable composition and interaction. Keep navigation, labels, inputs and status text native in Penpot.

PixelLab remains an optional cloud alternative. Its Aseprite extension does not make the model run locally. The remaining notes apply only if the user specifically chooses that provider.

PixelLab's official docs list character directions/animations, tiles and objects, an Aseprite extension and remote HTTP MCP at `https://api.pixellab.ai/mcp`. MCP requires an active subscription and a private Bearer token. OMP already supports remote HTTP MCP, so use its native transport if connecting; no speculative npm package is needed. Do not print tokens or place them in prompts/repositories.

The Aseprite extension is downloaded from the user's PixelLab account after subscription or trial. The installation guide requires Aseprite 1.3.7 or later; the existing workstation version was 1.3.18.6 on 2026-10-01. PixelLab itself is researched but not authenticated or installed by this setup. Do not claim generations have been tested. Account login, extension download and MCP access remain account-specific steps.

For an authorized generation trial, specify one original subject, source size, projection, palette, outline, lighting and transparent background. Use owned/licensed sketches or approved original style references. Inspect the actual sprite at native scale and intended display scale before expanding into a family. Check silhouettes, seams, frame alignment and directional consistency. Retain prompt/settings, provider job ID where available, source and export hashes, and rights/provenance notes.

PixelLab's UI-art tool produces raster artwork. Use its output for decorative frames or material exploration where appropriate; redraw functional controls as native components. Review per-tool credit use in the account before a trial and avoid an unrequested batch. Do not upload health data, real GPS, gym photos or competitor assets.

Sources accessed 2026-10-01: [interfaces and MCP](https://www.pixellab.ai/docs/ways-to-use-pixellab), [Aseprite installation](https://www.pixellab.ai/docs/installation), [UI artwork](https://www.pixellab.ai/docs/tools/create-ui-elements-pro), [API index](https://api.pixellab.ai/v2/llms.txt). Vendor claims do not establish quality, legal clearance or successful local integration.
