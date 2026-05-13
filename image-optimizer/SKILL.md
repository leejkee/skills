---
name: image-optimizer
description: "Use this skill to compress screenshots and scanned images for blog posts. It converts images to black-on-transparent WebP files with minimal file size, sharp edges, and no background noise. Trigger this skill when the user wants to insert optimized images into notes, documents, or dark-mode web pages."
---

# Image Optimizer (Blog Screenshot Compression)

## Overview

This skill transforms blog screenshots into tiny, sharp, black-on-transparent WebP images. It uses only **Pillow** and **NumPy** to:

- Keep text and UI elements clear
- Remove noise and compression artifacts
- Reduce file size through transparency and posterisation
- Output fully transparent backgrounds (perfect for dark-mode blogs)

No external tools like OpenCV are required. The entire pipeline runs inside a single script.

## Quick Reference

| Task | Execution Command |
| --- | --- |
| Optimize an image | `python3 scripts/run.py <input_path> <output_path>` |

> **LLM must only use this single command.**
> There are no separate environment checks or processing scripts to call.

## Execution Protocol

1. **Call the unified entrypoint**
   Convert paths to **absolute paths** and wrap them in **double quotes**.  
   For the execution command, on Windows, use `python` instead of `python3` if `python3` is unavailable.

   ```powershell
   python3 run.py "C:\absolute\path\to\input.png" "C:\absolute\path\to\output.webp"
   ```
   Note: If the user provides a non-webp output extension, you must change it to .webp and notify the user of this modification.

2. **Handle results**
   - On success, the script prints a JSON object containing the final `.webp` path.
   - On failure, the script prints a JSON error object with a `context` field.
   - If an error occurs, read the `context` and present the user with a concise, actionable suggestion.

3. **No manual steps**
   - Do **not** run `scripts/process_img.py` or `scripts/check_env.py`.
   - The script manages its own environment internally (dependency verification, silent pip installation if needed, and import checks).

## Technical Details

### Processing Pipeline (inside `scripts/run.py`)

Every image goes through these steps:

1. **Grayscale conversion** – the image is converted to a single luminance channel.
2. **Transparency mask generation** – brighter pixels become transparent, darker pixels become opaque. A luminance threshold (`thresh`) separates background from foreground.
3. **Posterisation** – the transparency channel is quantised to a small number of levels (`levels_count`). This sharply reduces file size by eliminating subtle gradients.
4. **De‑burring and noise removal** – a median filter (size 3) is applied to the transparency mask, removing isolated noise pixels and smoothing jagged edges without blurring sharp edges.
5. **RGBA composition** – a solid black RGB layer is combined with the processed transparency mask, creating a black‑on‑transparent image.
6. **WebP export** – the final image is saved as a lossy WebP file with a quality setting that balances file size and visual clarity.

### Output Characteristics

- **Format**: WebP (lossy)
- **Appearance**: Black foreground (text, lines, icons) on a completely transparent background.
- **Intended use**: Blog illustrations, screenshots of UIs, diagrams, scanned documents. Perfect for sites that support transparent images and dark‑mode readers.

### Default Parameters (optimised for blog screenshots)

The script uses built‑in defaults that work well for typical blog screenshots:

- `thresh = 200` – pixels with luminance > 200 become fully transparent.
- `levels_count = 2` – transparency is reduced to only 2 levels (fully opaque or fully transparent), producing a crisp “binary” look.
- `quality = 50` – WebP quality is set to 50, offering strong compression while keeping edges crisp.

The LLM does **not** need to pass these parameters. `run.py` handles them internally.

### Dependencies

The script requires:

- Python 3.7+
- [Pillow](https://python-pillow.org)
- [NumPy](https://numpy.org)

On first run, `scripts/run.py` automatically checks for these packages. If any are missing, it attempts a silent `pip install`. If dependency installation fails and no JSON error is returned, provide a generic message suggesting the user manually install the required dependencies. If the script fails silently, return a generic error message: "An unexpected error occurred. Please check the script logs for details."

## Critical Rules

- **Always use the single entrypoint** – `python3 scripts/run.py <input_path> <output_path>`.
- **Do not pre‑check the environment** – the script handles that itself.
- **Report errors verbatim** – if a JSON error is returned, present its `context` to the user.
- **This skill is optimised for text / UI screenshots** – it produces black‑on‑transparent output. It is **not** intended for colour photography.
- **Output format is always WebP** – ensure the destination path ends with `.webp`.