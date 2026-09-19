from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.routers import enterprises, milestones, credit, stats

app = FastAPI(title="工银科创桥 API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(enterprises.router, prefix="/api/enterprises", tags=["enterprises"])
app.include_router(milestones.router, prefix="/api/milestones", tags=["milestones"])
app.include_router(credit.router, prefix="/api/credit", tags=["credit"])
app.include_router(stats.router, prefix="/api/stats", tags=["stats"])


@app.on_event("startup")
async def startup():
    await init_db()
    from app.database import SessionLocal
    from app.services.mock_data import seed_mock_data
    db = SessionLocal()
    try:
        seed_mock_data(db)
        print("[Mock] Sample enterprises seeded")
    finally:
        db.close()


@app.get("/")
async def root():
    return {
        "service": "工银科创桥 API",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/api/health")
async def health():
    return {"status": "ok"}
