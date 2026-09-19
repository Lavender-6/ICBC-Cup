from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.enterprise import Enterprise
from app.models.milestone import Milestone
from app.models.patent import Patent
from app.models.team import TeamMember

router = APIRouter()


@router.get("/dashboard")
async def dashboard_stats(db: Session = Depends(get_db)):
    enterprises = db.query(Enterprise).all()
    total = len(enterprises)

    industry_dist = {}
    stage_dist = {}
    risk_levels = {"low": 0, "medium": 0, "high": 0}
    valuations = []

    for ep in enterprises:
        industry_dist[ep.industry] = industry_dist.get(ep.industry, 0) + 1
        stage_dist[ep.stage] = stage_dist.get(ep.stage, 0) + 1
        valuations.append(ep.current_valuation or 0)
        risk = ep.risk_score or 0
        if risk < 0.3:
            risk_levels["low"] += 1
        elif risk < 0.6:
            risk_levels["medium"] += 1
        else:
            risk_levels["high"] += 1

    avg_valuation = sum(valuations) / total if total else 0
    max_valuation = max(valuations) if valuations else 0
    min_valuation = min(valuations) if valuations else 0

    all_milestones = db.query(Milestone).all()
    ms_stats = {"completed": 0, "in_progress": 0, "pending": 0}
    for ms in all_milestones:
        ms_stats[ms.status] = ms_stats.get(ms.status, 0) + 1

    total_patents = db.query(Patent).count()
    total_members = db.query(TeamMember).count()

    return {
        "total_enterprises": total,
        "avg_valuation": round(avg_valuation, 2),
        "max_valuation": round(max_valuation, 2),
        "min_valuation": round(min_valuation, 2),
        "industry_dist": industry_dist,
        "stage_dist": stage_dist,
        "risk_levels": risk_levels,
        "milestone_stats": ms_stats,
        "total_patents": total_patents,
        "total_members": total_members,
    }
