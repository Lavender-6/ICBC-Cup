from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.enterprise import (
    CreditSimulateRequest,
    CreditResponse,
    RiskAlertResponse,
)
from app.services.credit_engine import (
    get_dynamic_credit,
    generate_risk_alerts,
    get_credit_history,
)

router = APIRouter()


@router.post("/simulate", response_model=CreditResponse)
async def simulate_credit(req: CreditSimulateRequest, db: Session = Depends(get_db)):
    result = get_dynamic_credit(db, req.enterprise_id, req.milestone_progress)
    if not result:
        raise HTTPException(status_code=404, detail="Enterprise not found")
    return result


@router.get("/history/{enterprise_id}")
async def credit_history(enterprise_id: str, db: Session = Depends(get_db)):
    records = get_credit_history(db, enterprise_id)
    return [
        {
            "id": r.id,
            "base_amount": r.base_amount,
            "progress_factor": r.progress_factor,
            "risk_factor": r.risk_factor,
            "final_amount": r.final_amount,
            "status": r.status,
            "created_at": r.created_at.isoformat(),
        }
        for r in records
    ]


@router.get("/alerts/{enterprise_id}", response_model=list[RiskAlertResponse])
async def get_alerts(enterprise_id: str, db: Session = Depends(get_db)):
    from app.models.credit import RiskAlert
    alerts = db.query(RiskAlert).filter(RiskAlert.enterprise_id == enterprise_id).order_by(RiskAlert.created_at.desc()).all()
    return alerts


@router.post("/alerts/{enterprise_id}/check")
async def check_alerts(enterprise_id: str, db: Session = Depends(get_db)):
    alerts = generate_risk_alerts(db, enterprise_id)
    return {"generated": len(alerts), "alerts": alerts}
