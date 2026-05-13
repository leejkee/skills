import numpy as np
from PIL import Image, ImageFilter

def process_image_python(input_path, output_path, thresh=128, levels_count=4, quality=80):
    # 1. 加载图片并转为灰度
    img = Image.open(input_path).convert("L")
    img_array = np.array(img).astype(np.float32)

    # 2. 计算 Alpha 通道
    # 逻辑：明度越高，越透明 (255 - gray)
    alpha = 255 - img_array
    
    # 应用阈值：如果原图亮度 > thresh，则完全透明
    alpha[img_array > thresh] = 0
    
    # 3. 核心：阶梯化 (Posterization) 以减小体积
    step = 255 / levels_count
    alpha = np.round(alpha / step) * step
    
    # 4. 去毛刺 (降噪处理)
    # 将 numpy 转回 PIL 进行滤镜处理，使用 MEDIAN_FILTER (中值滤波) 能有效去除孤立毛刺
    alpha_img = Image.fromarray(alpha.astype(np.uint8))
    alpha_img = alpha_img.filter(ImageFilter.MedianFilter(size=3)) 

    # 5. 合成最终图像
    # 创建一个纯黑色的底图 (RGB: 0, 0, 0)
    width, height = img.size
    black_layer = Image.new("L", (width, height), 0)
    
    # 合成 RGBA：R=0, G=0, B=0, A=计算出的灰阶Alpha
    result = Image.merge("RGBA", (black_layer, black_layer, black_layer, alpha_img))

    # 6. 导出为 WebP
    result.save(output_path, "WEBP", quality=quality, lossless=False)
    print(f"处理完成，保存至: {output_path}")