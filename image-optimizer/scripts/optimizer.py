import process_img
import os
from pathlib import Path
import argparse
import heapq

SCREENSHOT_IMG_DIR = str(Path.home() / "Pictures" / "Screenshots")

# Nextjs Starter public static assets folder
DEFAULT_OUTPUT_ROOT_DIR = "./public/static/blog_images/"

MAX_IMAGE_COUNT = 10


def get_latest_screenshot_path_via_index(image_dir: str, index: int, image_count: int) -> str:
    """Returns the absolute path of the screenshot at the specified index in the Screenshots directory."""

    base_dir = os.path.abspath(image_dir)
    if not os.path.exists(base_dir):
       process_img.log("Arguments invalid.", f"The screenshot directory does not exist.")
       return ""

    img_heap: list[tuple[float, str]] = []

    with os.scandir(base_dir) as entries:
        for entry in entries:
            if not entry.is_file():
                continue

            ext = os.path.splitext(entry.name)[1].lower()
            if ext not in ['.png', '.jpg', '.jpeg', '.bmp', '.webp']:
                continue

            mtime = entry.stat().st_mtime

            if len(img_heap) < image_count:
                heapq.heappush(img_heap, (mtime, entry.path))
            elif mtime > img_heap[0][0]:
                heapq.heappushpop(img_heap, (mtime, entry.path))

    if not img_heap:
        process_img.log("No image files found.", f"No images found in {image_dir}.")
        return ""
    
    if index < 1 or index >= len(img_heap):
        process_img.log("Index out of range.", f"Requested index {index} is out of range. There are only {len(img_heap)} screenshots available.")
        return ""

    top_k = heapq.nlargest(image_count, img_heap, key=lambda x: x[0])

    return top_k[index - 1][1]


def get_latest_screenshot_ab_path() -> str:
    """Returns the absolute path of the latest screenshot in the Screenshots directory."""
    return get_latest_screenshot_path_via_index(SCREENSHOT_IMG_DIR, index=1, image_count=MAX_IMAGE_COUNT)

def check_file_exists(path: str) -> bool:
    """Checks if the specified file exists."""
    return os.path.isfile(path) if path else False

def parse_args():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Process and optimize images."
    )

    # 直接输入文件（可选）
    parser.add_argument(
        "-i", "--input",
        type=str,
        default="",
        help="Direct input image path. Overrides automatic image selection."
    )

    # 输入源目录
    parser.add_argument(
        "-s", "--source-dir",
        type=str,
        default=SCREENSHOT_IMG_DIR,
        help=f"Source image directory. Default: {SCREENSHOT_IMG_DIR}"
    )

    # 最新的第几个
    parser.add_argument(
        "-n", "--latest-index",
        type=int,
        default=1,
        help="Use the N-th latest image in source-dir. 1 = latest."
    )

    # 输出
    parser.add_argument(
        "-o", "--output",
        type=str,
        required=True,
        help=f"Output filename (without path)."
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default=DEFAULT_OUTPUT_ROOT_DIR,
        help=(
            "Output directory. "
            f"Default: {DEFAULT_OUTPUT_ROOT_DIR}"
        )
    )

    # image process params
    parser.add_argument(
        "-w", "--white-point",
        type=int,
        default=220
    )

    parser.add_argument(
        "-b", "--black-point",
        type=int,
        default=80
    )

    parser.add_argument(
        "-d", "--denoise",
        action="store_true"
    )

    parser.add_argument(
        "--image-count",
        type=int,
        default=MAX_IMAGE_COUNT,
        help=f"Max image count to consider for latest-N. Default: {MAX_IMAGE_COUNT}"
    )

    return parser.parse_args()


def main():
    args = parse_args()
    
    # 获取输入路径
    if args.input:
        input_path = os.path.abspath(args.input)
    else:
        input_path = get_latest_screenshot_path_via_index(
            image_dir=args.source_dir,
            index=args.latest_index,
            image_count=args.image_count
        )

    if not check_file_exists(input_path):
        process_img.log("Input file not found.", "The specified input file does not exist")
        return

    # 拼接并处理输出路径
    # 例如 LLM 传入 "llm_tutorial.webp"，结果为 "./public/static/blog_images/llm_tutorial.webp"
    op_dir: str = args.output_dir
    op: str = args.output
    assert isinstance(op_dir, str)
    assert isinstance(op, str)
    final_output_path = os.path.join(op_dir, op)
    
    # 确保 Nextjs 的静态资源目标文件夹存在，如果不存在则自动创建
    os.makedirs(os.path.dirname(final_output_path), exist_ok=True)

    process_img.process_image(
        input_path=input_path, 
        output_path=final_output_path,
        white_point=args.white_point,
        black_point=args.black_point,
        denoise=args.denoise
    )
    return

if __name__ == "__main__":
    main()