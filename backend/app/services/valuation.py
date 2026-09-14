import numpy as np
from sqlalchemy.orm import Session
from app.models.enterprise import Enterprise
from app.models.patent import Patent
from app.models.team import TeamMember
from app.services.patent_network import get_enterprise_patent_network
from app.services.team_portrait import get_team_portrait


INDUSTRY_MULTIPLIERS = {
    "半导体": 1.5,
    "航天": 1.3,
    "生物医药": 1.4,
    "高端装备": 1.2,
    "新材料": 1.1,
    "人工智能": 1.6,
    "default": 1.0,
}

STAGE_MULTIPLIERS = {
    "立项预研": 0.3,
    "原型验证": 0.6,
    "流片成功": 1.0,
    "商业化量产": 1.5,
    "上市预备": 2.0,
}


def estimate_valuation(db: Session, enterprise_id: str) -> dict:
    enterprise = db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
    if not enterprise:
        return {}

    patents = db.query(Patent).filter(Patent.enterprise_id == enterprise_id).all()
    members = db.query(TeamMember).filter(TeamMember.enterprise_id == enterprise_id).all()

    patent_network = get_enterprise_patent_network(db, enterprise_id)
    team_portrait = get_team_portrait(db, enterprise_id)

    patent_count = len(patents)
    avg_patent_quality = np.mean([p.quality_score or 0 for p in patents]) if patents else 0
    industry_mult = INDUSTRY_MULTIPLIERS.get(enterprise.industry, INDUSTRY_MULTIPLIERS["default"])
    stage_mult = STAGE_MULTIPLIERS.get(enterprise.stage, 0.5)
    team_score = team_portrait.get("team_score", 0)
    rd_ratio = enterprise.rd_ratio or 0.0

    patent_valuation = patent_count * avg_patent_quality * 500 * industry_mult
    team_valuation = team_score * len(members) * 300 * industry_mult
    rd_valuation = rd_ratio * enterprise.employee_count * 100

    base_valuation = patent_valuation + team_valuation + rd_valuation
    current_valuation = base_valuation * stage_mult

    risk_score = compute_risk_score(
        avg_patent_quality, team_score, patent_count, enterprise.rd_ratio or 0
    )

    enterprise.base_valuation = round(base_valuation, 2)
    enterprise.current_valuation = round(current_valuation, 2)
    enterprise.risk_score = round(risk_score, 4)
    db.commit()

    return {
        "base_valuation": round(base_valuation, 2),
        "current_valuation": round(current_valuation, 2),
        "risk_score": round(risk_score, 4),
        "patent_count": patent_count,
        "avg_patent_quality": round(avg_patent_quality, 4),
        "team_score": round(team_score, 4),
        "industry_multiplier": industry_mult,
        "stage_multiplier": stage_mult,
        "components": {
            "patent_valuation": round(patent_valuation, 2),
            "team_valuation": round(team_valuation, 2),
            "rd_valuation": round(rd_valuation, 2),
        },
    }


def compute_risk_score(
    patent_quality: float, team_score: float, patent_count: int, rd_ratio: float
) -> float:
    quality_risk = 1.0 - patent_quality
    team_risk = 1.0 - team_score
    scale_risk = 1.0 / (1.0 + patent_count * 0.1)
    rd_risk = 1.0 - min(rd_ratio, 1.0)

    risk = 0.30 * quality_risk + 0.30 * team_risk + 0.20 * scale_risk + 0.20 * rd_risk
    return max(0.0, min(1.0, risk))
