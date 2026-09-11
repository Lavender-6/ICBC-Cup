# 频谱智瞳 — AI 无线信号识别与频谱监测平台

> 基于 AI 的无线信号调制识别、参数估计与频谱可视化平台

## 项目简介

频谱智瞳是一个端到端的无线信号智能识别平台，支持用户上传 IQ 数据集（.npy/.wav），
通过 AI 模型自动识别调制方式（AM/FM/BPSK/QPSK/16QAM/64QAM 等）、估计 SNR 等参数，
并以频谱瀑布图、星座图等形式可视化展示识别结果。

## 技术栈

| 层级 | 技术选型 |
|------|---------|
| 前端 | Vue3 + TypeScript + Vite + ECharts + WebSocket |
| 后端 | FastAPI + SQLAlchemy + Redis |
| AI | PyTorch + ONNX（信号分类 + 参数估计） |
| 数据库 | MySQL + Redis |

## 项目结构

```
ICT/
├── frontend/          # Vue3 前端（可视化 Demo 页）
├── backend/           # FastAPI 后端（API 网关 + 任务调度）
├── ai/                # AI 模块（训练 / 导出 / 推理）
└── docs/              # 项目文档
```

## 快速开始

### 后端

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

### AI 模块

```bash
cd ai
pip install -r requirements.txt
```

## 文档

- [系统架构方案](docs/频谱智瞳_系统架构方案.md)
