# Local ComfyUI artwork

Use this route for local artwork without a generation subscription. Root: `~/.local/share/omp-comfyui`. OMP's language-model provider is separate.

Start with `sh ~/.local/share/omp-comfyui/start.sh`; stop with `sh ~/.local/share/omp-comfyui/stop.sh`. The service listens at `http://127.0.0.1:8188`, is not enabled at login, disables API nodes and allows only the local `omp_sprite` custom-node folder. Other custom nodes remain disabled.

Downloaded models: SDXL Base 1.0, Pixel Art XL LoRA, fixed SDXL VAE, and U2Net ONNX for foreground masking. `models.json` and `provenance/` record sources, hashes and notices. The sprite exporter runs U2Net on CPU with ONNX Runtime 1.23.2; SDXL uses the AMD GPU. Runtime export does not download models or contact a cloud service.

## Choose the sprite recipe

The founder requested transparent backgrounds, larger visible pixels and selectable sizes, using The Binding of Isaac as a stylistic reference. For this project's sprites, start with compact silhouettes, expressive heads, dark outlines and simple flat shading. Create original subjects. A proposed 32×32 canvas with 12–16 opaque colours and two padding pixels is a useful starting point, not a universal accepted art standard. Use 48×48 or 64×64 when a face/equipment needs more detail; rectangles such as 32×48 are supported. Keep practical text and controls native in Penpot.

Native grid and display size differ: 32×32 at 6×, 48×48 at 4× and 64×64 at 3× all display at 192×192. The first has the largest visible pixels. Use nearest-neighbour integer scaling. Avoid gradients, glossy highlights, dithering and excessive texture when the request is for chunky sprites.

## Generate and inspect

1. Read the project brief and specify subject, projection, silhouette, palette, outline, lighting and native/display sizes. Keep content fictional and references original or licensed.
2. Check `python3 ~/.local/share/omp-comfyui/scripts/comfy_local.py doctor`.
3. Run `comfy_local.py generate --prompt '...' --name simple-label --size 32x32 --colors 12 --scale 6`. Defaults: one image, 24 Euler steps, CFG 6, LoRA 0.7, 32×32, 16 colours, padding 2, preview 6×. Prompt for a single isolated subject with margin on a plain background. Use `--help` for supported settings. Pass user text through proper shell quoting or a subprocess argument array.
4. Retain the returned job ID and call `comfy_local.py status JOB_ID` until completion. On a submission timeout, inspect the saved request/client ID, queue and history before retrying; the job may already be queued.
5. Inspect all outputs: 1024×1024 source, native RGBA sprite and enlarged RGBA preview. Check actual alpha (0/255), silhouette, face, stray pixels, edge halos, clipping, palette count and native-grid readability on light and dark backgrounds. A model can ignore a prompt or generate a sheet. Select the intended original subject with a recorded crop before exporting; never claim an arbitrary sheet is one clean sprite.
6. Repair the selected candidate in Aseprite. Save editable source and retain prompts, seed, models and hashes. Palette reduction alone does not make deliberate clusters, ensure a shared family palette, or establish animation consistency.

GUI: **Workflows → OMP Transparent Sprites** (`user/default/workflows/OMP Transparent Sprites.json`); the **OMP Transparent Sprite** node exposes dimensions, colour count, padding, background method, alpha threshold and preview scale. API graph: `sprite-api.json`. The original opaque **OMP Pixel Art** workflow is retained; `generate --mode art` uses it. Jobs live in `jobs/`; outputs in `output/local-art/`.

## Export existing art without regenerating

Run with the installed generation Python, using a new output directory:

```sh
~/.local/share/omp-comfyui/venv/bin/python \
  ~/.local/share/omp-comfyui/scripts/sprite_export.py \
  /absolute/path/source.png /absolute/path/new-export \
  --size 32x32 --colors 12 --scale 6 --aseprite
```

This saves `sprite.png`, `preview.png`, provenance and optionally one raster-layer `sprite.aseprite`. `--background existing_alpha` preserves a manually cleaned mask instead of rerunning U2Net. `--alpha-threshold` defaults to 128. Check thin limbs, hair/leaf tips and outlines after changes. Empty cutouts or foreground reaching the source edge fail explicitly. Repair in Aseprite or make a better isolated source; do not conceal the failure with a fabricated success claim.

The exporter crops to foreground, preserves aspect ratio and bottom-aligns within padding. Independently fitting frames causes animation jitter: choose a fixed canvas/pivot/scale and author consistent frames in Aseprite. Do not claim this workflow generates reliable directions, animation or seamless tiles. The installed size study is in `output/sprite-study/`.

## Official local MCP

OMP has `comfy-local` (`comfy-mcp` 0.10.0, `comfy-cli` 1.22.0). Use live node/model discovery and `validate_workflow` for changes beyond the helper, checking the returned `valid` value. Use the configured local address and installed graphs. Generic `generate_image` may assume another model template. Optional partner operations are outside this setup: do not enable API nodes, sign in, supply cloud credentials or spend credits under a local artwork request.

`installation.json` records verification. Krita AI Diffusion, InvokeAI and stable-diffusion.cpp remain documented alternatives, not installed dependencies. Use the supplied service scripts to preserve GPU/path settings. Valid PNGs and completed jobs prove execution; final visual quality requires review in Aseprite and the actual Penpot composition.
