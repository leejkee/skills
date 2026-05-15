import process_img
import os
from pathlib import Path
import argparse

SCREENSHOT_IMG_DIR = str(Path.home() / "Pictures" / "Screenshots")

# Nextjs Starter public static assets folder
DEFAULT_OUTPUT_DIR = "./public/static/blog_images/"

def get_latest_screenshot_ab_path() -> str:
    """Returns the absolute path of the latest screenshot in the Screenshots directory."""
    if not os.path.exists(SCREENSHOT_IMG_DIR):
       process_img.log("Directory not found.", f"The default screenshot directory {SCREENSHOT_IMG_DIR} does not exist.")
       return ""

    files = [os.path.join(SCREENSHOT_IMG_DIR, f) for f in os.listdir(SCREENSHOT_IMG_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not files:
        process_img.log("No image files found.", f"No PNG/JPG images found in {SCREENSHOT_IMG_DIR}.")
        return ""

    latest_file = max(files, key=os.path.getctime)
    return os.path.abspath(latest_file)

def check_file_exists(path: str) -> bool:
    """Checks if the specified file exists."""
    return os.path.isfile(path) if path else False

def parse_args():
    """parse command-line arguments for the image optimizer script."""
    parser = argparse.ArgumentParser(description="Process a screenshot and optimize its size. Designed for LLM skill invocation.")
    
    # 输入文件参数
    parser.add_argument("-i", "--input", type=str, default="", 
                        help="Path to the input image. If not provided, the latest screenshot will be used.")
    
    # 强制要求的输出参数 (required=True)
    parser.add_argument("-o", "--output", type=str, required=True, 
                        help=f"REQUIRED: The output filename (e.g. 'my-new-post-header.webp'). It will be saved automatically into {DEFAULT_OUTPUT_DIR}")
    
    # 图像处理参数
    parser.add_argument("-w", "--white-point", type=int, default=220, 
                        help="Pixels brighter than this become fully transparent (removes background noise). Default: 220")
    parser.add_argument("-b", "--black-point", type=int, default=80, 
                        help="Pixels darker than this become fully opaque (strengthens black foreground). Default: 80")
    
    # 布尔值开关参数
    parser.add_argument("-d", "--denoise", action="store_true", 
                        help="Apply light denoising. Set this flag if the screenshot is noisy. Default: False")
    
    return parser.parse_args()

def main():
    args = parse_args()
    
    # 获取输入路径
    input_path = args.input if args.input else get_latest_screenshot_ab_path()
    if not check_file_exists(input_path):
        process_img.log("Input file not found.", "The specified input file does not exist")
        return

    # 拼接并处理输出路径
    # 例如 LLM 传入 "llm_tutorial.webp"，结果为 "./public/static/blog_images/llm_tutorial.webp"
    final_output_path = os.path.join(DEFAULT_OUTPUT_DIR, args.output)
    
    # 确保 Nextjs 的静态资源目标文件夹存在，如果不存在则自动创建
    os.makedirs(os.path.dirname(final_output_path), exist_ok=True)

    try:
        process_img.process_image(
            input_path=input_path, 
            output_path=final_output_path,
            white_point=args.white_point,
            black_point=args.black_point,
            denoise=args.denoise
        )
        print(f"Success: Image processed and saved to {final_output_path}")
    except Exception as e:
        process_img.log(str(e), "An error occurred during image processing.")
        return

if __name__ == "__main__":
    main()