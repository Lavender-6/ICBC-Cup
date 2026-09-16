import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.milestone import Milestone, FinancialTool, MILESTONE_STAGES
from app.models.enterprise import Enterprise
from app.schemas.enterprise import MilestoneResponse, FinancialToolResponse
from app.services.milestone_trigger import trigger_financial_tools

router = APIRouter()


@router.get("/{enterprise_id}", response_model=list[MilestoneResponse])
async def list_milestones(enterprise_id: str, db: Session = Depends(get_db)):
    milestones = db.query(Milestone).filter(Milestone.enterprise_id == enterprise_id).all()
    return sorted(milestones, key=lambda m: MILESTONE_STAGES.index(m.stage) if m.stage in MILESTONE_STAGES else 999)


@router.post("/{enterprise_id}", response_model=MilestoneResponse)
async def create_milestone(enterprise_id: str, data: dict, db: Session = Depends(get_db)):
    enterprise = db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
    if not enterprise:
        raise HTTPException(status_code=404, detail="Enterprise not found")

    milestone = Milestone(
        id=str(uuid.uuid4()),
        enterprise_id=enterprise_id,
        name=data.get("name", ""),
        stage=data.get("stage", MILESTONE_STAGES[0]),
        description=data.get("description", ""),
        progress=data.get("progress", 0.0),
        status=data.get("status", "pending"),
    )
    db.add(milestone)
    db.commit()
    db.refresh(milestone)
    return milestone


@router.put("/{milestone_id}/progress", response_model=MilestoneResponse)
async def update_progress(milestone_id: str, progress: float, db: Session = Depends(get_db)):
    milestone = db.query(Milestone).filter(Milestone.id == milestone_id).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    milestone.progress = max(0.0, min(1.0, progress))
    if milestone.progress >= 1.0:
        milestone.status = "completed"
        milestone.is_verified = True
    elif milestone.progress > 0.0:
        milestone.status = "in_progress"
        milestone.is_verified = False
    else:
        milestone.status = "pending"
        milestone.is_verified = False
    db.commit()
    db.refresh(milestone)
    return milestone


@router.get("/{milestone_id}/tools", response_model=list[FinancialToolResponse])
async def get_tools(milestone_id: str, db: Session = Depends(get_db)):
    milestone = db.query(Milestone).filter(Milestone.id == milestone_id).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    tools = trigger_financial_tools(db, milestone_id)
    return tools


@router.get("/stages/list")
async def get_stages():
    return MILESTONE_STAGES
