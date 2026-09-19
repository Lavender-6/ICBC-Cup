import uuid
from sqlalchemy.orm import Session
from app.models.enterprise import Enterprise
from app.models.milestone import Milestone
from app.models.credit import CreditRecord
from app.services.valuation import estimate_valuation


def compute_credit_amount(
    base_valuation: float, progress_factor: float, risk_factor: float
) -> dict:
    base_amount = base_valuation * 0.3
    final_amount = base_amount * progress_factor * risk_factor

    return {
        "base_amount": round(base_amount, 2),
        "progress_factor": round(progress_factor, 4),
        "risk_factor": round(risk_factor, 4),
        "final_amount": round(final_amount, 2),
    }


def get_dynamic_credit(db: Session, enterprise_id: str, milestone_progress: float = 0.0) -> dict:
    enterprise = db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
    if not enterprise:
        return {}

    valuation = estimate_valuation(db, enterprise_id)
    base_valuation = valuation.get("current_valuation", 0)
    risk_score = valuation.get("risk_score", 0.5)

    progress_factor = max(0.0, min(1.0, milestone_progress))
    risk_factor = 1.0 - risk_score * 0.5

    credit = compute_credit_amount(base_valuation, progress_factor, risk_factor)

    record = CreditRecord(
        id=str(uuid.uuid4()),
        enterprise_id=enterprise_id,
        base_amount=credit["base_amount"],
        progress_factor=credit["progress_factor"],
        risk_factor=credit["risk_factor"],
        final_amount=credit["final_amount"],
        status="simulated",
    )
    db.add(record)
    db.commit()

    return {
        **credit,
        "enterprise_name": enterprise.name,
        "base_valuation": base_valuation,
        "risk_score": risk_score,
    }


def generate_risk_alerts(db: Session, enterprise_id: str) -> list[dict]:
    from app.services.milestone_trigger import check_milestone_alerts
    from app.models.milestone import MILESTONE_STAGES

    milestones = db.query(Milestone).filter(Milestone.enterprise_id == enterprise_id).all()
    alerts = []

    for ms in milestones:
        ms_alerts = check_milestone_alerts(ms)
        alerts.extend(ms_alerts)

    stage_map = {}
    for ms in milestones:
        if ms.stage in MILESTONE_STAGES:
            stage_map[MILESTONE_STAGES.index(ms.stage)] = ms

    for i, stage in enumerate(MILESTONE_STAGES):
        ms = stage_map.get(i)
        if not ms or ms.status == "pending":
            continue
        if i > 0:
            prev_ms = stage_map.get(i - 1)
            if not prev_ms or prev_ms.status != "completed":
                alerts.append({
                    "type": "tech_route_change",
                    "severity": "critical",
                    "message": f"技术路线变更：'{stage}'已启动但前置阶段'{MILESTONE_STAGES[i-1]}'未完成",
                })

    return alerts


def get_credit_history(db: Session, enterprise_id: str) -> list[CreditRecord]:
    return (
        db.query(CreditRecord)
        .filter(CreditRecord.enterprise_id == enterprise_id)
        .order_by(CreditRecord.created_at.desc())
        .all()
    )
