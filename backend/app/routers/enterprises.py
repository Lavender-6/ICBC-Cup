import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.enterprise import Enterprise
from app.models.patent import Patent
from app.models.team import TeamMember
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


@router.get("", response_model=list[EnterpriseResponse])
async def list_enterprises(db: Session = Depends(get_db)):
    return db.query(Enterprise).order_by(Enterprise.created_at.desc()).all()


@router.post("", response_model=EnterpriseResponse)
async def create_enterprise(data: EnterpriseBase, db: Session = Depends(get_db)):
    enterprise = Enterprise(id=str(uuid.uuid4()), **data.model_dump())
    db.add(enterprise)
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
