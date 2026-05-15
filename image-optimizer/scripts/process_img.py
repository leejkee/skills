import numpy as np
import json
from PIL import Image, ImageFilter


def log(error_str: str, context: str) -> None:
    """Logs a JSON error message to the console."""
    error_data = {
        "error": error_str,
        "context": context
    }
    print(json.dumps(error_data))

def process_image(input_path: str, output_path: str, white_point: int = 220, black_point: int = 80, denoise: bool = False):
    """
    Process a screenshot and optimize its size.
    :param white_point: pixels brighter than this become fully transparent (removes background noise)
    :param black_point: pixels darker than this become fully opaque (strengthens black foreground)
    :param denoise: whether to apply light denoising (set to False for clean screenshots)
    """
    try:
        # 1. Load the image and convert it to grayscale.
        # If the source image has an alpha channel, composite it over white first to avoid transparent pixels turning black.
        img = Image.open(input_path)
        if img.mode in ('RGBA', 'LA'):
            bg = Image.new('RGB', img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[-1])
            img = bg
        
        img_gray = img.convert("L")
        img_array = np.array(img_gray).astype(np.float32)
        # 2. Compute the alpha channel (core logic: tonal mapping).
        # Map [black_point, white_point] to [255, 0] (inverted so darker pixels are more opaque).
        # brightness >= white_point -> Alpha = 0 (fully transparent)
        # brightness <= black_point -> Alpha = 255 (fully opaque)
        
        # Linear interpolation mapping.
        alpha = 255 - ((img_array - black_point) / (white_point - black_point) * 255)
        
        # Clamp values to the 0-255 range.
        alpha = np.clip(alpha, 0, 255)
        # Optional: posterize alpha (use a higher number of steps like 8 or 16 to preserve anti-aliasing while reducing file size).
        # step = 255 / 16
        # alpha = np.round(alpha / step) * step
        # 3. Create the alpha image.
        alpha_img = Image.fromarray(alpha.astype(np.uint8))
        # 4. Remove artifacts (enable only if the source contains significant noise).
        if denoise:
            # ModeFilter or very light Gaussian blur/UnsharpMask.
            # ModeFilter preserves edges while removing isolated pixels.
            alpha_img = alpha_img.filter(ImageFilter.ModeFilter(size=3))
        # 5. Compose the final image.
        width, height = img.size
        black_layer = Image.new("L", (width, height), 0)
        
        # Compose RGBA: RGB channels are all black, keeping only the extracted alpha.
        result = Image.merge("RGBA", (black_layer, black_layer, black_layer, alpha_img))
        # 6. Export as WebP.
        # For monochrome screenshots, strongly recommend lossless=True, method=6 (maximum compression level).
        # This produces a very small file with razor-sharp edges.
        result.save(output_path, "WEBP", lossless=True, method=6)
        
        log("None", f"Output saved to {output_path}")
    except Exception as e:
        log(str(e), f"Failed to process {input_path}")