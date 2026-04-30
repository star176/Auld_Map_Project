# 奥尔德大陆 Auld 地图工程

小说世界观用的高清卫星风格地图制作工程，支持切片缩放浏览、图层叠加、后续 AI 增强。

---

## 一、项目能做什么（当前 MVP）

- ✅ 加载卫星地形图作为主底图
- ✅ 生成 8 种 Mask 图层（陆地/海洋/山脉/森林/沙漠/河流/城市/政治）
- ✅ 将大图切成 tiles 并记录索引
- ✅ 从 tiles 拼回完整图片
- ✅ 网页浏览器缩放拖拽浏览地图
- ✅ 预留图层开关面板

---

## 二、安装依赖

```bash
pip install -r requirements.txt
```

---

## 三、放置参考图

将两张参考图放入 `data/input/`：

```
Auld_Map_Project/
└─ data/
   └─ input/
      ├─ terrain_reference.png   ← 卫星地形图（主底图）
      └─ political_reference.png ← 政治全景图（参考图层）
```

---

## 四、项目初始化

```bash
python scripts/init_project.py
```

检查目录结构，输出配置摘要。

---

## 五、准备参考图

```bash
python scripts/prepare_reference.py
```

效果：
- 将 `terrain_reference.png` 复制为 `data/output/base_terrain.png`
- 将 `political_reference.png` 复制为 `data/output/political_reference.png`
- 自动更新 `config/project.yaml` 中的图片尺寸

---

## 六、生成 Mask 图层

```bash
python scripts/generate_masks.py --input data/output/base_terrain.png --output data/masks
```

输出 8 个 PNG mask（尺寸与 base_terrain.png 一致）：
- `land_mask.png`
- `ocean_mask.png`
- `mountain_mask.png`
- `forest_mask.png`
- `desert_mask.png`
- `river_mask.png`
- `city_mask.png`
- `political_mask.png`

---

## 七、图片切片

```bash
python scripts/tile_image.py --input data/output/base_terrain.png --output data/tiles/terrain --tile-size 512 --overlap 64
```

输出：
- 多个 `tile_X_Y.png` 文件
- `tile_index.json` 记录每个 tile 的坐标信息

---

## 八、从 Tiles 重建图片

```bash
python scripts/rebuild_from_tiles.py --index data/tiles/terrain/tile_index.json --output data/output/rebuilt_terrain.png
```

验证切片过程是否无损。

---

## 九、启动网页浏览器

```bash
python -m http.server 8000
```

然后访问：

```
http://localhost:8000/web/
```

**注意**：如果浏览器因为本地文件限制导致 `tile_index.json` 加载失败，请使用上述 HTTP 服务方式打开，不要直接双击 HTML 文件。

---

## 十、浏览器显示"瓦片加载失败"怎么办

**问题原因**：`file://` 协议下浏览器安全限制阻止加载 JSON 文件。

**解决方案**：

```bash
# 方法 1：使用 Python 内置 HTTP 服务器（推荐）
cd Auld_Map_Project
python -m http.server 8000
# 浏览器打开 http://localhost:8000/web/

# 方法 2：使用 VS Code Live Server 插件
# 右键 index.html → "Open with Live Server"

# 方法 3：使用 Node.js 的 http-server
npx http-server . -p 8000
# 然后访问 http://localhost:8000/web/
```

---

## 十一、当前阶段只做 Terrain 图层

右上角面板预留了 8 个图层按钮，但第一阶段只有 **Terrain** 可用，其他为 disabled 占位。后续按 pipeline.md 路线逐个实现。

---

## 十二、后续扩展方向

详见 `docs/pipeline.md` 和 `docs/task_list.md`。

---

## 项目结构

```
Auld_Map_Project/
├─ README.md
├─ requirements.txt
├─ config/
│  └─ project.yaml
├─ scripts/
│  ├─ init_project.py
│  ├─ prepare_reference.py
│  ├─ generate_masks.py
│  ├─ tile_image.py
│  └─ rebuild_from_tiles.py
├─ data/
│  ├─ input/
│  ├─ output/
│  ├─ masks/
│  └─ tiles/
├─ web/
│  ├─ index.html
│  ├─ main.js
│  └─ style.css
└─ docs/
   ├─ pipeline.md
   └─ task_list.md
```
