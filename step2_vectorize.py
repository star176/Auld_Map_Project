"""
Step 2: 矢量化大陆轮廓 - 从参考图提取海岸线并生成 SVG
基于卫星参考图自动提取海岸线，同时手动标注关键地理特征
"""

import numpy as np
from PIL import Image
import os

PROJECT = r"C:\Users\shawn\.qclaw\workspace\Auld_Map_Project"
REF_SAT = os.path.join(PROJECT, "00_reference", "continent_satellite_ref.png")
REF_POL = os.path.join(PROJECT, "00_reference", "continent_political_ref.png")
OUT_DIR = os.path.join(PROJECT, "01_vector_base")

# 加载参考图
print("Loading satellite reference...")
sat_img = Image.open(REF_SAT).convert("RGB")
sat_arr = np.array(sat_img)
H, W = sat_arr.shape[:2]
print(f"  Image size: {W}x{H}")

# 提取海岸线：通过颜色差异检测陆地/海洋边界
# 海洋区域：深蓝色 (R<80, G<120, B>150)
# 陆地区域：其他颜色
print("Extracting coastline...")

def is_water(pixel):
    """判断像素是否为海洋/水域"""
    r, g, b = pixel[0], pixel[1], pixel[2]
    # 深蓝色调 + 亮度较低 = 水
    brightness = int(r) + int(g) + int(b)
    # 海洋特征：蓝色通道主导，整体偏暗
    if b > 100 and b > r * 1.3 and b > g * 1.1 and brightness < 400:
        return True
    # 浅水/近岸（青绿色）
    if b > 140 and g > 120 and r < 100 and brightness < 450:
        return True
    return False

# 创建 land/water mask
mask = np.zeros((H, W), dtype=np.uint8)
for y in range(H):
    for x in range(W):
        if not is_water(sat_arr[y, x]):
            mask[y, x] = 255  # 陆地

print("  Mask created, extracting contour points...")

# 简化的轮廓提取：扫描边缘
coastline_points = []
# 水平扫描，检测 water->land 过渡
for y in range(0, H, 2):  # 每2像素采样一次减少点数
    prev_land = mask[y, 0] > 0
    for x in range(1, W):
        curr_land = mask[y, x] > 0
        if curr_land != prev_land:
            coastline_points.append((x, y))
            prev_land = curr_land

# 垂直扫描补充
for x in range(0, W, 2):
    prev_land = mask[0, x] > 0
    for y in range(1, H):
        curr_land = mask[y, x] > 0
        if curr_land != prev_land:
            coastline_points.append((x, y))
            prev_land = curr_land

print(f"  Extracted {len(coastline_points)} coastline points")

# 使用 Douglas-Peucker 算法简化路径（简化版）
def simplify_points(points, epsilon=3.0):
    """Douglas-Peucker 路径简化"""
    if len(points) <= 2:
        return points
    
    # 找到距离首尾连线最远的点
    first = np.array(points[0])
    last = np.array(points[-1])
    
    max_dist = 0
    max_idx = 0
    
    for i in range(1, len(points) - 1):
        p = np.array(points[i])
        # 点到线段的距离
        line_vec = last - first
        line_len = np.linalg.norm(line_vec)
        if line_len == 0:
            dist = np.linalg.norm(p - first)
        else:
            t = max(0, min(1, np.dot(p - first, line_vec) / (line_len ** 2)))
            proj = first + t * line_vec
            dist = np.linalg.norm(p - proj)
        
        if dist > max_dist:
            max_dist = dist
            max_idx = i
    
    if max_dist > epsilon:
        left = simplify_points(points[:max_idx+1], epsilon)
        right = simplify_points(points[max_idx:], epsilon)
        return left[:-1] + right
    else:
        return [first.tolist(), last.tolist()]

print("Simplifying coastline...")
simplified = simplify_points(coastline_points, epsilon=5.0)
print(f"  Simplified to {len(simplified)} points")

# 生成 SVG
def generate_coastline_svg(points, width, height, filename):
    """生成海岸线 SVG"""
    svg_lines = []
    svg_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    
    # 背景（海洋）
    svg_lines.append(f'  <rect width="{width}" height="{height}" fill="#0a1628"/>')
    
    # 陆地多边形
    path_d = f"M {points[0][0]} {points[0][1]}"
    for i in range(1, len(points)):
        path_d += f" L {points[i][0]} {points[i][1]}"
    path_d += " Z"
    
    svg_lines.append(f'  <path d="{path_d}" fill="#3d5c35" stroke="#2a4025" stroke-width="2"/>')
    
    svg_lines.append('</svg>')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg_lines))
    print(f"  Saved: {filename}")

generate_coastline_svg(simplified, W, H, os.path.join(OUT_DIR, "coastline.svg"))

# 同时保存掩码图供后续使用
mask_img = Image.fromarray(mask)
mask_img.save(os.path.join(PROJECT, "02_masks", "land_mask.png"))
print("  Saved: 02_masks/land_mask.png")

print("\nStep 2 complete!")
