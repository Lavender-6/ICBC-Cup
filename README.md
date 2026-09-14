# 工银科创桥 — 硬科技企业里程碑式投贷联动平台

> AI 驱动的硬科技企业动态估值与投贷联动平台

## 项目简介

工银科创桥是一个面向硬科技企业（半导体/航天/生物医药/高端装备）的里程碑式投贷联动平台。
通过 AI 评估引擎（专利引用网络建模 + 研发团队画像）对轻资产科创企业进行动态估值，
以研发里程碑为触发器，动态匹配金融工具包（知识产权质押贷/投贷联动/供应链金融等），
将传统「静态审批」变为「动态授信」。

## 技术栈

| 层级 | 技术选型 |
|------|---------|
| 前端 | Vue3 + TypeScript + Vite + ECharts + Element Plus |
| 后端 | FastAPI + SQLAlchemy + SQLite + Redis(可选) |
| AI | NetworkX(专利引用网络) + 估值模型 |
| 数据库 | SQLite(开发) / MySQL(生产) + Redis |

## 项目结构

```
ICT/
├── frontend/          # Vue3 前端
├── backend/           # FastAPI 后端
├── ai/                # AI 模块（专利网络 + 估值模型）
└── docs/              # 项目文档
```

## 快速开始

### 后端

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 前端

```bash
cd frontend
pnpm install
npx vite --host 0.0.0.0 --port 3000
```

## 文档

- [工银科创桥方案文档](docs/工银科创桥_硬科技企业里程碑式投贷联动平台.md)
