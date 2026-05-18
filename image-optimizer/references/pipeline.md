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
