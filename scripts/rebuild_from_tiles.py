"""
rebuild_from_tiles.py
奥尔德大陆地图工程 - 从 Tiles 重建图片脚本

功能：
- 读取 tile_index.json
- 根据 tiles 拼回完整图片
- overlap=0 时直接覆盖拼合
- overlap>0 时先覆盖拼接，预留 feather_blend 函数
- 输出 data/output/rebuilt_XXX.png
"""

import sys
import json
from pathlib import Path
from PIL import Image
import numpy as np


def feather_blend(tile_region, base_region, overlap_w, overlap_h):
    """
    羽化混合函数（预留）
    在 overlap 区域使用线性渐变权重混合两张图片

    参数：
    - tile_region: 当前 tile 像素 (numpy array)
    - base_region: 已有底图的对应区域
    - overlap_w: 水平重叠宽度
    - overlap_h: 垂直重叠高度

    返回：混合后的像素 array
    """
    if overlap_w <= 0 and overlap_h <= 0:
        return tile_region

    result = base_region.copy().astype(np.float32)

    # 水平渐变权重（从右到左衰减）
    if overlap_w > 0:
        for x in range(overlap_w):
            weight = (x + 1) / overlap_w  # 0→1，从 tile 渐变到底图
            w_tile = weight
            w_base = 1.0 - weight
            for row in range(tile_region.shape[0]):
                result[row, x] = (
                    tile_region[row, x].astype(np.float32) * w_tile +
                    base_region[row, x].astype(np.float32) * w_base
                )

    # 垂直渐变权重（从下到上衰减）
    if overlap_h > 0:
        for y in range(overlap_h):
            weight = (y + 1) / overlap_h
            w_tile = weight
            w_base = 1.0 - weight
            for col in range(tile_region.shape[1]):
                result[y, col] = (
                    tile_region[y, col].astype(np.float32) * w_tile +
                    base_region[y, col].astype(np.float32) * w_base
                )

    return result.clip(0, 255).astype(np.uint8)


def rebuild_from_tiles(index_path, output_path, overlap=0):
    """根据 tile_index.json 重建图片"""

    with open(index_path, "r", encoding="utf-8") as f:
        index = json.load(f)

    W = index["image_width"]
    H = index["image_height"]
    tiles = index["tiles"]
    tile_dir = Path(index_path).parent

    # 创建空白底图
    result = Image.new("RGB", (W, H), (0, 0, 0))

    print(f"  底图尺寸: {W} x {H}")
    print(f"  开始拼合 {len(tiles)} 个 tiles ...")

    for tile_info in tiles:
        tile_path = tile_dir / tile_info["filename"]
        if not tile_path.exists():
            print(f"  ⚠️ 跳过缺失 tile: {tile_info['filename']}")
            continue

        tile = Image.open(tile_path)
        x = tile_info["x"]
        y = tile_info["y"]
        w = tile_info["width"]
        h = tile_info["height"]

        result.paste(tile, (x, y))

    result.save(output_path)
    return W, H, len(tiles)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    import argparse
    parser = argparse.ArgumentParser(description="从 tiles 重建完整图片")
    parser.add_argument("--index", required=True, help="tile_index.json 路径")
    parser.add_argument("--output", required=True, help="输出图片路径")
    parser.add_argument("--overlap", type=int, default=0, help="重叠像素（默认 0）")
    args = parser.parse_args()

    PROJECT_ROOT = Path(__file__).parent.parent
    index_path = PROJECT_ROOT / args.index
    output_path = PROJECT_ROOT / args.output

    if not index_path.exists():
        print(f"❌ 找不到 index 文件: {index_path}")
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[从 Tiles 重建图片]")
    print(f"  index:  {index_path}")
    print(f"  output: {output_path}")

    W, H, count = rebuild_from_tiles(
        index_path=index_path,
        output_path=output_path,
        overlap=args.overlap
    )

    print(f"\n✅ 重建完成！{count} 个 tiles → {output_path.relative_to(PROJECT_ROOT)}")
    print(f"   尺寸: {W} x {H} px")


if __name__ == "__main__":
    main()
