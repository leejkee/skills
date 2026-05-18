---
name: image-optimizer
description: "Use this skill to optimize screenshots, UI captures, or diagrams before inserting them into technical blogs or Markdown/MDX posts. Execute the script to generate tiny, sharp, WebP images."
compatibility: "Requires Python 3.12+, Pillow, NumPy"
---

# Image Optimizer (Blog Screenshot Compression)

## Overview

This skill transforms screenshots and UI captures into tiny, sharp, black-on-transparent WebP images optimized for technical blogs and markdown-based publishing systems.

The script is autonomous:
- If no explicit image path is provided, it automatically resolves the latest system screenshot.
- It supports selecting the N-th latest image for multi-image workflows.
- It supports custom source directories for batch-like sequential processing.

## Execution Context

The optimizer script is located at `scripts/optimizer.py`. Always execute the script using this relative path, as the client handles resolving the base directory location automatically.

```bash
# Standard execution
python scripts/optimizer.py -o <filename>

```

## Input Resolution Rules

If no input arguments are provided, the script defaults to finding the absolute latest screenshot (`-n 1`) in the system's default screenshot directory.

| Priority | Flag | Meaning |
| --- | --- | --- |
| **1. Explicit Image** | `-i <path>` | Use the exact specified image source. |
| **2. Explicit Directory** | `-s <path>` | Look in this specific directory for the latest image. |
| **3. Explicit Index** | `-n <N>` | Use the N-th latest image from the target directory. |

## Output Placement

You **must** specify an output filename using `-o <filename>`. If omitted, the script will terminate with an error. By default, files are saved to `./public/static/blog_images/`. You can override the destination folder using the `--output-dir` flag.

## Quick Reference Examples

* **Optimize the latest screenshot (Default):**
`python scripts/optimizer.py -o nextjs-architecture.webp`
* **Process a specific previous screenshot (e.g., the 3rd latest):**
`python scripts/optimizer.py -n 3 -o agent-workflow.webp`
* **Process a specific file and save to a custom directory:**
`python scripts/optimizer.py -i ~/Desktop/demo.png --output-dir ~/Desktop/exported_imgs -o tutorial-step1.webp`
* **Advanced (Adjust thresholds and enable denoising):**
`python scripts/optimizer.py -o dark-mode-ui.webp -w 230 -b 50 -d`

## Gotchas

* If you omit the `-i`, `-s`, or `-n` flags, the script will silently assume you want the most recent screenshot from the default system folder.
* The script assumes the output format is WebP; you should always use the `.webp` extension in your `-o` filename.
* Do not attempt to hardcode absolute paths for the Python script itself; always rely on the relative `scripts/optimizer.py` path.

## References
See the [Pipeline Reference](./references/pipeline.md) for a detailed breakdown of the image processing steps, including thresholding, edge detection, and denoising techniques used to achieve optimal results.