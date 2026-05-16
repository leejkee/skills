---
name: image-optimizer
description: "Use this skill to compress screenshots and convert images into transparent lossless WebP blog assets. The script automatically resolves the input image source. Output files are automatically routed into the default blog static assets directory unless a custom output directory is explicitly provided. If the user does not explicitly provide an image path, DO NOT ask for one — the script automatically selects the latest screenshot from the default screenshot directory. Supports selecting the N-th latest image and custom source directories for multi-image workflows in a single LLM conversation. Trigger this skill when the user mentions blog images, screenshots, Markdown/MDX assets, technical notes, UI captures, diagrams, or image insertion into blog posts."
---

# Image Optimizer (Blog Screenshot Compression)

## Overview

This skill transforms screenshots and UI captures into tiny, sharp, black-on-transparent WebP images optimized for technical blogs and markdown-based publishing systems.


The script is autonomous:

- If no explicit image path is provided, it automatically resolves the latest screenshot.
- It supports selecting the N-th latest image for multi-image workflows.
- It supports custom source directories for batch-like sequential processing during a single LLM conversation.

The pipeline uses only **Pillow** and **NumPy** to:

- Preserve sharp text and UI edges
- Remove background noise
- Reduce file size aggressively
- Generate transparent dark-mode-friendly assets


# Execution Context (IMPORTANT)

The optimizer script resides inside the skill directory itself.

Agents MUST NOT assume the current working directory contains:

```text
scripts/optimizer.py
```

Always resolve the script path relative to the installed skill location.

Example (Windows):

```bash
python C:\Users\<user>\.config\opencode\skills\image-optimizer\scripts\optimizer.py
```

Example (Linux/macOS):

```bash
python ~/.config/opencode/skills/image-optimizer/scripts/optimizer.py
```

The current workspace/project directory is NOT guaranteed to contain the optimizer script.


# Input Resolution Rules (IMPORTANT)

## Automatic Input Resolution

If the user does NOT explicitly provide an image path:

The script automatically resolves the input image using:

- default screenshot directory
- latest image selection (`--latest-index 1`)

The assistant should NOT ask the user for image locations unless the workflow genuinely requires external images.


## Input Priority

The script resolves input sources using the following priority:

### 1. Explicit image path (highest priority)

```bash
-i /path/to/image.png
```

If provided, this file is used directly.


### 2. Automatic latest-image resolution

If no `--input` is provided:

```bash
--source-dir
--latest-index
```

are used together to resolve the target image.

Defaults:

```text
source-dir   = system screenshot directory
latest-index = 1
```

Meaning:

```text
Use the latest screenshot automatically.
```

# Output Placement & Naming Rules (IMPORTANT)

## Mandatory Output Parameter

You MUST provide:

```bash
-o
--output
```

The script fails if omitted.


## Contextual Naming

Generate meaningful filenames based on the conversation topic.

Good examples:

```text
nextjs-routing-overview.webp
llm-agent-workflow.webp
qt-signal-slot-diagram.webp
cli-error-fix.webp
```

Avoid generic names:

```text
image1.webp
test.webp
final.webp
```


## Automated Output Placement

DO NOT pass absolute output paths, always provide relative paths or just filenames.

Only provide:

```bash
-o filename.webp
```

or:

```bash
-o tutorial/step1.webp
```

By default, the script saves files into: `./public/static/blog_images/`  

However, a custom output directory can also be specified using: `--output-dir`

# Quick Reference Examples

| Task                                     | Execution Command                                                                                                                           |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Optimize latest screenshot automatically | `python scripts/optimizer.py -o nextjs-architecture.webp`                                                                                   |
| Process the 3rd latest screenshot        | `python scripts/optimizer.py -n 3 -o agent-workflow.webp`                                                                                   |
| Use a custom output directory            | `python scripts/optimizer.py --output-dir ~/Desktop/exported_imgs -o diagram.webp`                                                          |
| Use a custom source directory            | `python scripts/optimizer.py -s ~/Downloads/blog_imgs -n 2 -o vector-db-ui.webp`                                                            |
| Explicitly process a specific file       | `python scripts/optimizer.py -i ~/Desktop/demo.png -o tutorial/step1.webp`                                                                  |
| Adjust tonal thresholds                  | `python scripts/optimizer.py -o dark-mode-ui.webp --white-point 200 --black-point 100`                                                      |
| Enable denoising                         | `python scripts/optimizer.py -o scanned-doc.webp --denoise`                                                                                 |
| Full advanced example                    | `python scripts/optimizer.py -s ~/Downloads/chat_imgs -n 4 --output-dir ~/Desktop/exported_imgs-o tutorial/mcp-server.webp -w 230 -b 50 -d` |


# Technical Details

## Processing Pipeline (`scripts/process_img.py`)

Every image goes through these stages:

### 1. Alpha Pre-processing & Grayscale Conversion

If the source image already contains transparency (RGBA/LA):

* it is composited onto a white background first
* preventing transparent regions from becoming black artifacts

The image is then converted into grayscale luminance.


### 2. Transparency Mask Generation (Tonal Mapping)

Instead of binary thresholding, luminance is smoothly mapped into opacity.

Rules:

* luminance > `white_point`
  → fully transparent

* luminance < `black_point`
  → fully opaque

* intermediate pixels
  → linearly interpolated alpha

This preserves anti-aliasing and smooth text edges.


### 3. Optional Noise Removal

If:

```bash
--denoise
```

is enabled:

A small Mode filter removes isolated artifact pixels while preserving edge sharpness.


### 4. RGBA Composition

A pure black RGB layer is combined with the generated alpha mask.

Result:

```text
black foreground + transparent background
```


### 5. Lossless WebP Export

The final image is exported as:

```text
lossless WebP
```

using:

```text
method=6
```

for maximum compression efficiency.


# Output Characteristics

| Property      | Value                       |
| ------------- | --------------------------- |
| Format        | Lossless WebP               |
| Background    | Fully transparent           |
| Foreground    | Pure black                  |
| Edge Quality  | Anti-aliased                |
| Optimized For | Technical blogs / dark mode |

Ideal for:

* UI screenshots
* diagrams
* CLI captures
* architecture charts
* scanned notes
* markdown blog assets


# Default Parameters

Optimized for clean modern screenshots.

| Parameter     | Default | Purpose                              |
| ------------- | ------- | ------------------------------------ |
| `white_point` | `220`   | Removes white/light gray backgrounds |
| `black_point` | `80`    | Strengthens dark foreground text     |
| `denoise`     | `False` | Preserves maximum sharpness          |


# Dependencies

Requirements:

* Python 3.12+
* Pillow
* NumPy

Install:

```bash
pip install -r requirements.txt
```
