"""
generate_masks.py
奥尔德大陆地图工程 - Mask 图层生成脚本

功能：
- 读取 base_terrain.png
- 按颜色/亮度规则生成 8 种 mask 图层
- land/ocean 基于颜色分析
- mountain/forest/desert/river/city/political 预留接口，方便后续替换为更复杂算法

输出：
- data/masks/land_mask.png
- data/masks/ocean_mask.png
- data/masks/mountain_mask.png
- data/masks/forest_mask.png
- data/masks/desert_mask.png
- data/masks/river_mask.png
- data/masks/city_mask.png
- data/masks/political_mask.png
"""

import sys
from pathlib import Path
from PIL import Image
import numpy as np


# ========================
# Mask 生成算法接口
# ========================

def is_water(pixel):
    """判断像素是否为海洋/水域"""
    r, g, b = float(pixel[0]), float(pixel[1]), float(pixel[2])
    brightness = r + g + b
    # 海洋：蓝色通道主导，亮度较低
    if b > 100 and b > r * 1.3 and b > g * 1.1 and brightness < 400:
        return True
    # 浅水/近岸
    if b > 140 and g > 120 and r < 100 and brightness < 450:
        return True
    return False


def is_land(pixel):
    """判断像素是否为陆地"""
    return not is_water(pixel)


def is_mountain(pixel):
    """山脉判断 - 亮色高对比度区域（占位算法，后续替换）"""
    r, g, b = float(pixel[0]), float(pixel[1]), float(pixel[2])
    # 高亮度 + 低饱和度 = 可能是雪山/岩石
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    sat = (max_c - min_c) / 255.0 if max_c > 0 else 0
    brightness = (r + g + b) / 3.0
    if brightness > 200 and sat < 0.3:
        return True
    return False


def is_forest(pixel):
    """森林判断 - 深绿色调（占位算法，后续替换）"""
    r, g, b = float(pixel[0]), float(pixel[1]), float(pixel[2])
    # 绿色通道较高，饱和度中高
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    sat = (max_c - min_c) / 255.0 if max_c > 0 else 0
    if g > r * 1.2 and g > b * 1.1 and sat > 0.2:
        return True
    return False


def is_desert(pixel):
    """荒漠判断 - 黄褐色调（占位算法，后续替换）"""
    r, g, b = float(pixel[0]), float(pixel[1]), float(pixel[2])
    # 暖色调，高红色或黄色，低蓝色
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    sat = (max_c - min_c) / 255.0 if max_c > 0 else 0
    brightness = (r + g + b) / 3.0
    if r > g * 1.1 and b < r * 0.7 and sat > 0.15 and brightness > 120:
        return True
    return False


def is_river(pixel):
    """河流判断 - 细长蓝色/蓝绿色条带（占位算法，后续替换）"""
    # 占位：第一阶段用空白 mask
    return False


def is_city(pixel):
    """城市判断 - 密集灰色区域（占位算法，后续替换）"""
    # 占位：第一阶段用空白 mask
    return False


def is_political(pixel):
    """政治边界 - 预留（占位算法，后续替换）"""
    # 占位：第一阶段用空白 mask
    return False


# ========================
# Mask 生成主函数
# ========================

def generate_land_ocean_masks(img_array, H, W):
    """生成 land 和 ocean mask"""
    land = np.zeros((H, W), dtype=np.uint8)
    ocean = np.zeros((H, W), dtype=np.uint8)

    for y in range(H):
        for x in range(W):
            if is_land(img_array[y, x]):
                land[y, x] = 255
            else:
                ocean[y, x] = 255

    return land, ocean


def generate_placeholder_mask(H, W):
    """生成占位空白 mask（全黑）"""
    return np.zeros((H, W), dtype=np.uint8)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    import argparse
    parser = argparse.ArgumentParser(description="生成 mask 图层")
    parser.add_argument("--input", required=True, help="base_terrain.png 路径")
    parser.add_argument("--output", required=True, help="输出目录路径")
    args = parser.parse_args()

    PROJECT_ROOT = Path(__file__).parent.parent
    input_path = PROJECT_ROOT / args.input
    output_dir = PROJECT_ROOT / args.output

    if not input_path.exists():
        print(f"❌ 找不到输入图片: {input_path}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    print("[1/3] 加载图片...")
    img = Image.open(input_path).convert("RGB")
    img_array = np.array(img)
    H, W = img_array.shape[:2]
    print(f"  尺寸: {W} x {H} px")

    print("\n[2/3] 生成 mask 图层...")
    masks = {}

    # land / ocean
    print("  生成 land_mask & ocean_mask ...")
    land, ocean = generate_land_ocean_masks(img_array, H, W)
    masks["land_mask.png"] = land
    masks["ocean_mask.png"] = ocean

    # 占位 mask
    placeholders = {
        "mountain_mask.png": "mountain (占位)",
        "forest_mask.png": "forest (占位)",
        "desert_mask.png": "desert (占位)",
        "river_mask.png": "river (占位)",
        "city_mask.png": "city (占位)",
        "political_mask.png": "political (占位)",
    }
    blank = generate_placeholder_mask(H, W)
    for name, desc in placeholders.items():
        print(f"  生成 {name} ({desc}) ...")
        masks[name] = blank

    print("\n[3/3] 保存 mask 文件...")
    for filename, mask_array in masks.items():
        out_path = output_dir / filename
        Image.fromarray(mask_array).save(out_path)
        print(f"  ✅ {filename}")

    print(f"\n✅ Mask 生成完成！共 {len(masks)} 个文件 → {output_dir.relative_to(PROJECT_ROOT)}/")


if __name__ == "__main__":
    main()
