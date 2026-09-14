import numpy as np
from sqlalchemy.orm import Session
from app.models.team import TeamMember


def compute_member_score(member: TeamMember) -> float:
    paper_score = min((member.paper_count or 0) / 50.0, 1.0)
    citation_score = min((member.citation_count or 0) / 500.0, 1.0)
    h_score = min((member.h_index or 0) / 30.0, 1.0)
    patent_score = min((member.patent_count or 0) / 20.0, 1.0)
    exp_score = min((member.experience_years or 0) / 15.0, 1.0)
    founder_bonus = 0.1 if member.is_founder else 0.0

    score = (
        0.20 * paper_score
        + 0.20 * citation_score
        + 0.15 * h_score
        + 0.25 * patent_score
        + 0.20 * exp_score
        + founder_bonus
    )
    return round(max(0.0, min(1.0, score)), 4)


def get_team_portrait(db: Session, enterprise_id: str) -> dict:
    members = db.query(TeamMember).filter(TeamMember.enterprise_id == enterprise_id).all()
    if not members:
        return {"members": [], "team_score": 0, "total_papers": 0, "total_patents": 0, "avg_h_index": 0}

    total_papers = 0
    total_patents = 0
    total_citations = 0
    h_indices = []
    member_list = []

    for m in members:
        m.portrait_score = compute_member_score(m)
        total_papers += m.paper_count or 0
        total_patents += m.patent_count or 0
        total_citations += m.citation_count or 0
        h_indices.append(m.h_index or 0)
        member_list.append({
            "id": m.id,
            "name": m.name,
            "role": m.role or "",
            "education": m.education or "",
            "is_founder": m.is_founder,
            "paper_count": m.paper_count or 0,
            "citation_count": m.citation_count or 0,
            "h_index": m.h_index or 0,
            "patent_count": m.patent_count or 0,
            "experience_years": m.experience_years or 0,
            "portrait_score": m.portrait_score,
        })

    db.commit()

    team_score = np.mean([m["portrait_score"] for m in member_list])
    avg_h = np.mean(h_indices) if h_indices else 0

    return {
        "members": member_list,
        "team_score": round(team_score, 4),
        "total_papers": total_papers,
        "total_patents": total_patents,
        "total_citations": total_citations,
        "avg_h_index": round(avg_h, 2),
    }
