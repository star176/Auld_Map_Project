"""
prepare_reference.py
奥尔德大陆地图工程 - 参考图准备脚本

功能：
- 从 data/input/ 读取参考图
- 检查图片宽高
- 更新 config/project.yaml 中的 map_width_px 和 map_height_px
- 将图片复制到 data/output/ 作为规范化底图
- 不改变图片内容，不裁剪，不拉伸
"""

import sys
import shutil
from pathlib import Path
from PIL import Image
import yaml

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "project.yaml"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    import argparse
    parser = argparse.ArgumentParser(description="准备参考图，复制到 output 目录")
    parser.add_argument("--terrain", default="data/input/terrain_reference.png",
                        help="卫星地形图路径")
    parser.add_argument("--political", default="data/input/political_reference.png",
                        help="政治全景图路径")
    args = parser.parse_args()

    PROJECT_ROOT = Path(__file__).parent.parent

    terrain_path = PROJECT_ROOT / args.terrain
    political_path = PROJECT_ROOT / args.political
    output_dir = PROJECT_ROOT / "data" / "output"

    # 1. 检查输入文件
    print("[1/4] 检查输入文件...")
    for name, path in [("卫星地形图", terrain_path), ("政治全景图", political_path)]:
        if not path.exists():
            print(f"  ❌ 找不到: {path}")
            sys.exit(1)
        print(f"  ✅ {name}: {path}")

    # 2. 读取图片信息
    print("\n[2/4] 读取图片信息...")
    with Image.open(terrain_path) as img:
        w, h = img.size
        print(f"  terrain_reference.png: {w} x {h} px")

    with Image.open(political_path) as img:
        pw, ph = img.size
        print(f"  political_reference.png: {pw} x {ph} px")

    # 3. 复制到 output
    print("\n[3/4] 复制到 data/output/ ...")
    output_dir.mkdir(parents=True, exist_ok=True)
    terrain_out = output_dir / "base_terrain.png"
    political_out = output_dir / "political_reference.png"

    shutil.copy2(terrain_path, terrain_out)
    print(f"  ✅ → {terrain_out.relative_to(PROJECT_ROOT)}")

    shutil.copy2(political_path, political_out)
    print(f"  ✅ → {political_out.relative_to(PROJECT_ROOT)}")

    # 4. 更新配置
    print("\n[4/4] 更新 config/project.yaml ...")
    config = load_config()
    config["map_width_px"] = w
    config["map_height_px"] = h
    save_config(config)
    print(f"  ✅ map_width_px = {w}")
    print(f"  ✅ map_height_px = {h}")
    print("\n✅ 参考图准备完成！")


if __name__ == "__main__":
    main()
