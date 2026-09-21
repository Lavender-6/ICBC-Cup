# 工银科创桥 部署指南

## 架构

- **前端** → Vercel (免费)
- **后端** → Render (免费)
- **数据库** → SQLite (随后端部署，每次重启自动重新播种数据)

## 步骤一：部署后端到 Render

1. 访问 https://dashboard.render.com 并登录（可用 GitHub 登录）
2. 点击 **New +** → **Web Service**
3. 选择 GitHub 仓库 `Lavender-6/ICBC-Cup`
4. 配置：
   - **Name**: `icbc-cup-api`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. 点击 **Create Web Service**
6. 等待部署完成，记下后端 URL，例如：`https://icbc-cup-api.onrender.com`
7. 验证：访问 `https://icbc-cup-api.onrender.com/api/health` 应返回 `{"status":"ok"}`

## 步骤二：部署前端到 Vercel

1. 访问 https://vercel.com 并登录（用 GitHub 登录）
2. 点击 **Add New** → **Project**
3. 选择 GitHub 仓库 `Lavender-6/ICBC-Cup`
4. 配置：
   - **Root Directory**: `frontend`
   - **Framework Preset**: Vite
   - **Build Command**: `npm install && npm run build`
   - **Output Directory**: `dist`
5. **环境变量**（关键步骤）：
   - **Settings** → **Environment Variables**
   - 添加：`VITE_API_BASE_URL` = `https://icbc-cup-api.onrender.com/api`
   - （把 `icbc-cup-api.onrender.com` 替换为你的实际 Render URL）
6. 点击 **Deploy**
7. 等待部署完成，获得前端 URL，例如：`https://icbc-cup.vercel.app`

## 步骤三：验证

- 访问前端 URL，应看到首页
- 点击企业进入详情页，数据应正常加载
- 测试导出功能、对比功能等

## 注意事项

- Render 免费 tier 会在 15 分钟无请求后休眠，首次唤醒需等待 ~30 秒
- SQLite 数据在 Render 重启后会重置，但启动时自动重新播种演示数据
- AI 模型文件（.joblib）已包含在仓库中，无需额外配置
- 如需自定义域名，在 Vercel/Render 的 Settings → Domains 中添加
