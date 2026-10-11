# 🚀 Muse 视频专业提示词工坊 · 一键部署与运行指南

本项目为 **100% 纯前端零外部依赖架构**，支持任何云平台、Docker 容器以及本地多平台一键运行。

---

## 选项 1：Docker / Docker Compose（推荐云服务器、NAS 或 VPS）

本项目自带生产级轻量 Nginx Alpine 镜像，资源占用极低（< 15MB 内存）：

```bash
# 1. 启动容器
docker compose up -d --build

# 2. 查看状态
docker compose ps

# 3. 停止容器
docker compose down
```
启动后直接访问：`http://服务器IP:8080`

---

## 选项 2：免费云端静态托管（全球 CDN，无需服务器）

### A. Vercel
1. 安装 Vercel CLI：`npm i -g vercel`
2. 在项目根目录执行：`vercel --prod`
3. 30 秒内获得全球 HTTPS 访问域名。

### B. Cloudflare Pages
1. 登录 Cloudflare Dashboard -> **Workers & Pages** -> **Create application** -> **Pages**。
2. 连接 GitHub 仓库 `Wisely88/muse`。
3. 构建设置保持默认（无需 Build Command），根目录填 `/`，点击部署即可。

### C. GitHub Pages
1. 在仓库页面进入：`https://github.com/Wisely88/muse/settings/pages`
2. **Source** 选择 **Deploy from a branch** -> 分支选择 `main` -> 保存。
3. 永久域名：`https://wisely88.github.io/muse/`

---

## 选项 3：本地一键双击运行

- **macOS / Linux**：
  ```bash
  chmod +x run.sh
  ./run.sh
  ```
  自动检测 Docker 或 Python 环境并自动在浏览器拉起。

- **Windows**：
  双击根目录下的 `run.bat` 即可一键拉起。

---

## 包含文件清单
- `index.html`：工坊单页核心代码（包含全部 22 种中英视觉风格、双向翻译字典、离线历史与收藏）
- `Dockerfile`：生产级容器定义
- `docker-compose.yml`：Docker 一键编排
- `nginx.conf`：Gzip 高性能静态服务配置
- `run.sh` / `run.bat`：跨平台一键启动脚本
- `vercel.json` / `netlify.toml`：无服务器云平台配置
