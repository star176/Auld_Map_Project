"""
tile_image.py
奥尔德大陆地图工程 - 图片切片脚本

功能：
- 将大图切成固定大小 tiles
- 支持 tile_size 和 overlap
- 输出 tile_index.json（含每个 tile 的坐标信息）
- 输出多个 tile_X_Y.png 文件
"""

import sys
import json
from pathlib import Path
from PIL import Image


def tile_image(image_path, output_dir, tile_size=512, overlap=0):
    """将图片切成 tiles"""

    img = Image.open(image_path).convert("RGB")
    W, H = img.size

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    tiles = []
    count = 0

    y = 0
    while y < H:
        x = 0
        while x < W:
            # 计算当前 tile 范围
            tx = x
            ty = y
            tw = min(tile_size, W - x)
            th = min(tile_size, H - y)

            # 裁剪 tile
            tile = img.crop((tx, ty, tx + tw, ty + th))
            filename = f"tile_{tx}_{ty}.png"
            tile.save(output_dir / filename)

            tiles.append({
                "x": tx,
                "y": ty,
                "width": tw,
                "height": th,
                "filename": filename
            })

            count += 1
            x += tile_size - overlap
        y += tile_size - overlap

    # 写入 tile_index.json
    index = {
        "source_image": str(Path(image_path).name),
        "image_width": W,
        "image_height": H,
        "tile_size": tile_size,
        "overlap": overlap,
        "tile_count": count,
        "tiles": tiles
    }

    index_path = output_dir / "tile_index.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    return count, index_path


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    import argparse
    parser = argparse.ArgumentParser(description="将图片切成 tiles")
    parser.add_argument("--input", required=True, help="输入图片路径")
    parser.add_argument("--output", required=True, help="输出目录路径")
    parser.add_argument("--tile-size", type=int, default=512, help="瓦片大小（默认 512）")
    parser.add_argument("--overlap", type=int, default=0, help="重叠像素（默认 0）")
    args = parser.parse_args()

    PROJECT_ROOT = Path(__file__).parent.parent
    input_path = PROJECT_ROOT / args.input
    output_dir = PROJECT_ROOT / args.output

    if not input_path.exists():
        print(f"❌ 找不到输入图片: {input_path}")
        sys.exit(1)

    print(f"[开始切片]")
    print(f"  输入图片: {input_path}")
    print(f"  输出目录: {output_dir}")
    print(f"  tile_size: {args.tile_size}")
    print(f"  overlap:   {args.overlap}")

    count, index_path = tile_image(
        image_path=input_path,
        output_dir=output_dir,
        tile_size=args.tile_size,
        overlap=args.overlap
    )

    print(f"\n✅ 切片完成！共 {count} 个 tiles")
    print(f"   index 文件: {index_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
