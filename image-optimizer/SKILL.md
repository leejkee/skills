---
name: image-optimizer
description: "Use this skill to compress screenshots and convert images to WebP format. The processed images will be moved to a specified directory(typically a blog's static folder). Trigger this skill when the user metions blog images or wants to insert images into blog posts(e.g.,Markdown, MDX) or markdown notes."
---

# Image Optimizer (Blog Screenshot Compression)

## Overview

This skill transforms the screenshots into tiny, sharp, black-on-transparent WebP images. It uses only **Pillow** and **NumPy** to:

- Keep text and UI elements clear
- Remove noise and compression artifacts
- Reduce file size through transparency and posterisation
- Output fully transparent backgrounds (perfect for dark-mode blogs)

## Output Placement & Naming Rules (IMPORTANT)

- **Mandatory Output Parameter**: You **MUST** provide the `--output` (`-o`) argument. The script will fail if omitted.
- **Contextual Naming**: Generate a meaningful filename based on the current context/topic (e.g., `llm-architecture-diagram.webp`, `cli-error-fix.webp`).
- **Automated Directory Placement**: **DO NOT** pass absolute paths for the output. Just pass the filename or a relative subfolder path. The script automatically routes and saves the image to the Next.js static assets folder: `./public/static/blog_images/`.

## Quick Reference Examples
| Task | Execution Command |
| --- | --- |
| Optimize the latest screenshot & name it automatically | `python scripts/optimizer.py -o nextjs-architecture.webp` |
| Adjust thresholds (e.g., darker blacks, lower transparency threshold) | `python scripts/optimizer.py -o dark-mode-ui.webp --white-point 200 --black-point 100` |
| Enable denoising for a noisy image | `python scripts/optimizer.py -o scanned-doc-clean.webp --denoise` |
| Process a specific existing image with custom parameters | `python scripts/optimizer.py -i /path/to/old_image.png -o tutorial/step1.webp -w 230 -b 50 -d` |

## Technical Details

### Processing Pipeline (inside `scripts/process_img.py`)

Every image goes through these steps:

1. **Alpha Pre-processing & Grayscale conversion** – If the source image already has an alpha channel (RGBA/LA), it is first composited over a solid white background to prevent transparent areas from turning black. Then, the image is converted to a single luminance (grayscale) channel.
2. **Transparency mask generation (Tonal Mapping)** – Instead of a strict binary threshold, the script maps luminance to opacity using two points to preserve anti-aliasing:
   - Pixels brighter than `white_point` become fully transparent (Alpha = 0).
   - Pixels darker than `black_point` become fully opaque (Alpha = 255).
   - Pixels in between are linearly interpolated, ensuring smooth edges for text and icons.
3. **Optional Noise removal** – If the `denoise` flag is enabled, a Mode filter (size 3) is applied to the transparency mask. This removes isolated artifact pixels while preserving sharp edges.
4. **RGBA composition** – A solid black RGB layer is combined with the extracted transparency mask, creating a crisp black‑on‑transparent image.
5. **WebP export** – The final image is saved as a **lossless** WebP file. It uses maximum compression effort (`method=6`) to produce a very small file size while retaining razor-sharp edges.

### Output Characteristics

- **Format**: WebP (**lossless**)
- **Appearance**: Black foreground (text, lines, icons) on a completely transparent background. Anti-aliasing is preserved.
- **Intended use**: Blog illustrations, screenshots of UIs, diagrams, scanned documents. Perfect for sites that support transparent images and dark‑mode readers.

### Default Parameters (optimised for clean screenshots)

The script uses built‑in defaults that work well for typical UI screenshots and documents:

- `white_point = 220` – Pixels with luminance > 220 become fully transparent. Effectively removes white/light gray backgrounds.
- `black_point = 80` – Pixels with luminance < 80 become fully opaque. Strengthens the core black text and foreground elements.
- `denoise = False` – Denoising is disabled by default to maintain maximum sharpness, as modern UI screenshots rarely contain sensor noise. (Can be set to `True` for noisy/scanned images).


### Dependencies

The script requires:

- Python 3.12+
- [Pillow](https://python-pillow.org)
- [NumPy](https://numpy.org)

How to install dependencies:
(The `requirements.txt` file is included in `scripts/`.)
```bash
pip install -r requirements.txt
```
