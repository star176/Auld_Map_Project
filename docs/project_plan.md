# 奥尔德大陆高清卫星地图工程 - 项目计划

## 项目目标
制作类似 Google Earth / NASA Landsat 的真实卫星影像风格地图，支持缩放浏览。

## 项目结构
```
Auld_Map_Project/
├─ 00_reference/          # 参考图（卫星图 + 政治图）
├─ 01_vector_base/        # 矢量图层（SVG）
├─ 02_masks/              # 8192×8192 掩码图
├─ 03_heightmap/          # 高度图
├─ 04_satellite_render/   # 卫星渲染合成
├─ 05_city_detail/        # 城市高清细节
├─ 06_ai_refine/          # AI 局部增强
├─ 07_tiles/              # 瓦片切片
├─ 08_web_viewer/         # Leaflet 地图浏览器
└─ docs/                  # 文档
```

## 执行步骤
| Step | 任务 | 状态 |
|------|------|------|
| 1 | 整理参考图片 | ✅ |
| 2 | 矢量化大陆轮廓 coastline.svg | 🔄 进行中 |
| 3 | 绘制 rivers/mountains/cities/roads/biomes SVG | ⬜ |
| 4 | 生成 8192×8192 mask 图 | ⬜ |
| 5 | 合成 continent_base_8k.png | ⬜ |
| 6 | 制作三个核心城市高清图 | ⬜ |
| 7 | 切片 1024×1024 tiles，重叠128px | ⬜ |
| 8 | AI 局部增强每个 tile | ⬜ |
| 9 | 羽化拼接回 continent_refined_8k.png | ⬜ |
| 10 | 导出地图瓦片 z0-z6 | ⬜ |
| 11 | Leaflet 本地浏览器 | ⬜ |
| 12 | 验收检查 | ⬜ |

## 验收标准
1. 大陆轮廓与参考图一致
2. 奥尔德大河：东北→西南，中央大弯道
3. 奥瑞斯城：河流大弯道内侧河心岛
4. 东境半岛：向右突出，海岸线曲折
5. 北部：冰原+雪山
6. 西北：深绿色森林
7. 南部：大面积金黄色荒漠
8. 黎明港：东境半岛西侧大海湾
9. 赤砂城：南部荒漠绿洲
10. 支持缩放浏览
