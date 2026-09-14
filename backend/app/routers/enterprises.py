import uuid
import random
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.enterprise import Enterprise
from app.models.patent import Patent, PatentCitation
from app.models.team import TeamMember
from app.models.milestone import Milestone, MILESTONE_STAGES
from app.schemas.enterprise import (
    EnterpriseBase,
    EnterpriseResponse,
    ValuationResponse,
    TeamPortraitResponse,
    PatentNetworkResponse,
)
from app.services.valuation import estimate_valuation
from app.services.team_portrait import get_team_portrait
from app.services.patent_network import get_enterprise_patent_network

router = APIRouter()


def _generate_enterprise_data(db: Session, enterprise: Enterprise, patent_count: int = 10):
    eid = enterprise.id
    patent_ids = []
    for i in range(patent_count):
        pid = str(uuid.uuid4())
        patent_ids.append(pid)
        db.add(Patent(
            id=pid, enterprise_id=eid,
            patent_number=f"CN{random.randint(10000000, 99999999)}A",
            title=f"{enterprise.industry}核心专利-{i+1}",
            ipc_class=f"H0{random.randint(1,9)}L{random.randint(1,99)}/{random.randint(1,99)}",
            cited_count=random.randint(0, 30), cites_count=random.randint(0, 15),
            family_size=random.randint(1, 8), has_international=random.random() > 0.5,
            litigation_risk=random.random() * 0.3,
            filed_at=datetime.now() - timedelta(days=random.randint(100, 1000)),
        ))
    for _ in range(patent_count * 2):
        if len(patent_ids) >= 2:
            src, tgt = random.sample(patent_ids, 2)
            db.add(PatentCitation(source_patent_id=src, target_patent_id=tgt))

    member_count = random.randint(5, 12)
    roles = ["CEO", "CTO", "首席科学家", "研发总监", "高级工程师", "算法研究员"]
    for i in range(member_count):
        db.add(TeamMember(
            id=str(uuid.uuid4()), enterprise_id=eid, name=f"成员{i+1}",
            role=roles[i % len(roles)] if i < len(roles) else "工程师",
            education=random.choice(["博士", "硕士", "博士后"]),
            is_founder=i < 2, paper_count=random.randint(0, 60),
            citation_count=random.randint(0, 800), h_index=random.randint(0, 35),
            patent_count=random.randint(0, 25), experience_years=random.randint(3, 20),
        ))

    base_date = datetime(2026, 10, 1)
    current_stage_idx = MILESTONE_STAGES.index(enterprise.stage) if enterprise.stage in MILESTONE_STAGES else 0
    for idx, stage in enumerate(MILESTONE_STAGES):
        progress, status = 0.0, "pending"
        expected_date, actual_date = None, None
        if idx < current_stage_idx:
            progress, status = 1.0, "completed"
            expected_date = base_date - timedelta(days=(current_stage_idx - idx) * 120)
            actual_date = expected_date + timedelta(days=random.randint(-10, 30))
        elif idx == current_stage_idx:
            progress, status = random.uniform(0.3, 0.8), "in_progress"
            expected_date = base_date + timedelta(days=random.randint(-30, 30))
        else:
            expected_date = base_date + timedelta(days=(idx - current_stage_idx) * 120)
        db.add(Milestone(
            id=str(uuid.uuid4()), enterprise_id=eid, name=f"{stage}阶段里程碑",
            stage=stage, description=f"{enterprise.name}的{stage}阶段关键节点",
            expected_date=expected_date, actual_date=actual_date,
            progress=round(progress, 4), status=status, is_verified=status == "completed",
        ))


@router.get("", response_model=list[EnterpriseResponse])
async def list_enterprises(db: Session = Depends(get_db)):
    return db.query(Enterprise).order_by(Enterprise.created_at.desc()).all()


@router.post("", response_model=EnterpriseResponse)
async def create_enterprise(data: EnterpriseBase, db: Session = Depends(get_db)):
    patent_count = data.patent_count or 10
    create_data = {k: v for k, v in data.model_dump().items() if k != "patent_count"}
    enterprise = Enterprise(id=str(uuid.uuid4()), **create_data)
    db.add(enterprise)
    db.flush()
    _generate_enterprise_data(db, enterprise, patent_count)
    db.commit()
    db.refresh(enterprise)
    return enterprise


@router.get("/{enterprise_id}", response_model=EnterpriseResponse)
async def get_enterprise(enterprise_id: str, db: Session = Depends(get_db)):
    enterprise = db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
    if not enterprise:
        raise HTTPException(status_code=404, detail="Enterprise not found")
    return enterprise


@router.get("/{enterprise_id}/valuation", response_model=ValuationResponse)
async def get_valuation(enterprise_id: str, db: Session = Depends(get_db)):
    result = estimate_valuation(db, enterprise_id)
    if not result:
        raise HTTPException(status_code=404, detail="Enterprise not found")
    return result


@router.get("/{enterprise_id}/team", response_model=TeamPortraitResponse)
async def get_team(enterprise_id: str, db: Session = Depends(get_db)):
    result = get_team_portrait(db, enterprise_id)
    return result


@router.get("/{enterprise_id}/patents", response_model=PatentNetworkResponse)
async def get_patents(enterprise_id: str, db: Session = Depends(get_db)):
    result = get_enterprise_patent_network(db, enterprise_id)
    return result


@router.delete("/{enterprise_id}")
async def delete_enterprise(enterprise_id: str, db: Session = Depends(get_db)):
    enterprise = db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
    if not enterprise:
        raise HTTPException(status_code=404, detail="Enterprise not found")
    db.delete(enterprise)
    db.commit()
    return {"message": "Deleted"}
