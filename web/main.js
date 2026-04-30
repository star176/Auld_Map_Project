/**
 * main.js - 奥尔德大陆地图浏览器
 *
 * 功能：
 * - 使用 Leaflet CRS.Simple 加载瓦片
 * - 从 tile_index.json 读取瓦片信息
 * - 支持鼠标拖拽、滚轮缩放、鼠标坐标显示
 * - 预留 8 个图层控制按钮（第一阶段仅 Terrain 可用）
 */

let map;
let tiles = [];
let tileIndex = null;
let loadedTileCount = 0;
let totalTileCount = 0;

// ========================
// 初始化地图
// ========================
async function initMap() {
    const loadingEl = document.getElementById("loading");

    try {
        // 1. 加载 tile_index.json
        const indexUrl = "../data/tiles/terrain/tile_index.json";
        const resp = await fetch(indexUrl);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        tileIndex = await resp.json();
    } catch (err) {
        loadingEl.innerHTML = `
            <div style="color:#ff8080">
                ❌ 瓦片索引加载失败<br>
                <small>请使用 HTTP 服务方式打开：<br>
                python -m http.server 8000</small><br><br>
                <small>错误: ${err.message}</small>
            </div>`;
        return;
    }

    const W = tileIndex.image_width;
    const H = tileIndex.image_height;
    totalTileCount = tileIndex.tile_count;
    tiles = tileIndex.tiles;

    // 2. 计算边界
    // Leaflet CRS.Simple: 南西角为 [0,0]，北东角为 [H, W]
    const southWest = [0, 0];
    const northEast = [H, W];
    const bounds = L.latLngBounds(southWest, northEast);

    // 3. 创建地图
    map = L.map("map", {
        crs: L.CRS.Simple,
        minZoom: -2,
        maxZoom: 4,
        zoomControl: true,
        attributionControl: false,
        dragging: true,
        scrollWheelZoom: true,
    });

    // 4. 设置初始视图（显示完整大陆）
    map.fitBounds(bounds);

    // 5. 加载瓦片（作为 ImageOverlay）
    await loadTiles(tileIndex.tiles, W, H);

    // 6. 隐藏加载提示
    loadingEl.style.display = "none";

    // 7. 更新坐标显示
    map.on("mousemove", (e) => {
        const { lat, lng } = e.latlng;
        document.getElementById("coords").textContent =
            `x: ${Math.round(lng)}, y: ${Math.round(lat)}`;
    });

    map.on("zoomend", () => {
        document.getElementById("zoom-level").textContent =
            `Zoom: ${map.getZoom()}`;
    });

    // 8. 初始显示
    document.getElementById("zoom-level").textContent = `Zoom: ${map.getZoom()}`;
}

// ========================
// 加载瓦片
// ========================
async function loadTiles(tiles, imageWidth, imageHeight) {
    const loadingEl = document.getElementById("loading");
    const tileDir = "../data/tiles/terrain/";

    // 按行列分批加载，避免一次性请求过多
    const BATCH_SIZE = 20;
    for (let i = 0; i < tiles.length; i += BATCH_SIZE) {
        const batch = tiles.slice(i, i + BATCH_SIZE);
        await Promise.all(
            batch.map((tile) => loadTile(tile, tileDir, imageWidth, imageHeight))
        );
        loadedTileCount += batch.length;
        loadingEl.textContent = `加载地图瓦片中... ${loadedTileCount}/${totalTileCount}`;
    }
}

function loadTile(tile, tileDir, imageWidth, imageHeight) {
    return new Promise((resolve) => {
        const imgUrl = tileDir + tile.filename;
        const img = new Image();
        img.crossOrigin = "anonymous";

        img.onload = () => {
            // 将像素坐标映射到 Leaflet CRS.Simple 坐标
            // lat = imageHeight - y - height（翻转 Y 轴）
            const north = imageHeight - tile.y;
            const south = imageHeight - tile.y - tile.height;
            const west = tile.x;
            const east = tile.x + tile.width;

            L.imageOverlay(imgUrl, [[south, west], [north, east]], {
                interactive: false,
            }).addTo(map);

            resolve();
        };

        img.onerror = () => resolve(); // 单个瓦片失败不阻塞
        img.src = imgUrl;
    });
}

// ========================
// 启动
// ========================
document.addEventListener("DOMContentLoaded", initMap);
