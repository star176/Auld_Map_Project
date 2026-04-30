# 奥尔德大陆地图工程 - 处理流程

本文档记录地图工程的完整处理流程和后续迭代路线。

---

## 阶段 1：MVP 工程骨架 ✅

**目标**：建立可运行的项目工程骨架。

**产出**：
- 项目目录结构
- 配置文件
- 基础脚本（init/prepare/masks/tile/rebuild）
- 前端地图浏览器

**状态**：✅ 已完成

---

## 阶段 2：真实 Land/Ocean Mask

**目标**：用更精确的颜色/亮度/饱和度算法区分陆地和海洋。

**方法**：
- 使用 LAB 色彩空间做颜色分析
- 人工标注部分海岸线作为 ground truth
- 用少量样本训练简单分类器
- 保留手动修正接口

**产出**：
- `data/masks/land_mask.png`（精确版）
- `data/masks/ocean_mask.png`（精确版）

---

## 阶段 3：山脉、森林、沙漠、河流 Mask 半自动化

**目标**：用颜色分析和纹理分析区分主要地形。

**方法**：
- 山脉：分析亮度 + 对比度，检测高亮/白色区域
- 森林：绿色通道分析 + NDVI 风格算法
- 沙漠：黄褐色调 + 低饱和度区域
- 河流：线性特征检测 + 蓝色调过滤

**产出**：
- `data/masks/mountain_mask.png`
- `data/masks/forest_mask.png`
- `data/masks/desert_mask.png`
- `data/masks/river_mask.png`

**预留接口**：`generate_masks.py` 中的 `is_mountain()`、`is_forest()` 等函数可直接替换算法。

---

## 阶段 4：政治图与卫星图配准

**目标**：统一政治图和卫星图的坐标系统。

**方法**：
- 手动选取两张图上的同名地标点（海岸线交叉点、山脉顶点）
- 计算仿射变换矩阵
- 将政治图上的城市、边界、道路坐标映射到卫星图坐标系统
- 写入 `config/registration.yaml`

**产出**：
- `config/registration.yaml`（配准参数）
- 统一坐标系统

---

## 阶段 5：城市坐标固定

**目标**：提取政治图上的城市坐标，写入结构化 JSON。

**产出**：
- `data/coordinates/cities.json`（城市坐标列表）
- `data/coordinates/factions.json`（势力范围）

**格式示例**：
```json
{
  "cities": [
    {
      "name": "奥瑞斯",
      "x": 627,
      "y": 627,
      "faction": "auld",
      "type": "capital"
    }
  ]
}
```

---

## 阶段 6：矢量化边界和道路

**目标**：将政治图上的边界线、道路线转换为 SVG 矢量格式。

**方法**：
- 边缘检测 + 霍夫变换提取直线
- 手动描绘关键边界段落
- 保存为 `01_vector_base/` 下的 SVG 文件

**产出**：
- `01_vector_base/borders.svg`
- `01_vector_base/roads.svg`
- `01_vector_base/rivers.svg`

---

## 阶段 7：AI 分块高清增强

**目标**：用 AI 模型对每个 tile 进行局部高清增强。

**方法**：
- 使用 Stable Diffusion / ControlNet 做 tile 增强
- 保持地理特征一致性
- 分批处理，避免 API 限流

**配置**：
- 输入：`data/tiles/terrain/tile_*.png`
- 输出：`data/tiles/enhanced/tile_*.png`
- 模型：待选（可配置）

**接口**：`scripts/ai_enhance.py`（预留）

---

## 阶段 8：多级 Zoom Tiles

**目标**：生成 z0 ~ z6 多级缩放瓦片，替代单级平铺。

**方法**：
- 对高清底图做 2x 下采样生成多级
- 每级按对应 tile_size 切片
- 目录结构：`data/tiles/terrain/z0/`, `z1/`, ..., `z6/`

**前端适配**：Leaflet 支持多级瓦片，只需修改 `main.js` 中的路径逻辑。

---

## 阶段 9：前端图层系统

**目标**：完善前端图层面板，所有图层均可切换。

**方法**：
- 为每个 mask 生成彩色叠加图
- 用 Leaflet layerGroup 控制显隐
- 添加城市 marker 标注
- 添加地点搜索功能

**产出**：
- 所有 8 个图层按钮可正常切换
- 城市名称 tooltip
- 地点搜索栏

---

## 阶段 10：世界观数据库接入

**目标**：将地图与世界观数据库关联，支持多维度查询。

**方法**：
- 接入外部 JSON/数据库
- 显示城市详情弹窗
- 显示势力信息面板
- 支持导出为多种格式

**产出**：
- 完整的世界观地图浏览系统
- 支持故事叙事功能
