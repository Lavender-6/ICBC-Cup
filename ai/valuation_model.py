import numpy as np

FEATURE_NAMES = [
    "patent_count", "avg_patent_quality", "team_score",
    "rd_ratio", "employee_count", "industry_multiplier", "stage_multiplier",
]


def predict_valuation(features: dict) -> dict:
    patent_count = features.get("patent_count", 0)
    avg_quality = features.get("avg_patent_quality", 0)
    team_score = features.get("team_score", 0)
    rd_ratio = features.get("rd_ratio", 0)
    employee_count = features.get("employee_count", 0)
    industry_mult = features.get("industry_multiplier", 1.0)
    stage_mult = features.get("stage_multiplier", 0.5)

    patent_val = patent_count * avg_quality * 500 * industry_mult
    team_val = team_score * max(employee_count, 1) * 0.1 * 300 * industry_mult
    rd_val = rd_ratio * employee_count * 100

    base_valuation = patent_val + team_val + rd_val
    current_valuation = base_valuation * stage_mult

    risk = 0.3 * (1 - avg_quality) + 0.3 * (1 - team_score) + 0.2 * (1 / (1 + patent_count * 0.1)) + 0.2 * (1 - min(rd_ratio, 1))
    risk = max(0, min(1, risk))

    return {
        "base_valuation": round(base_valuation, 2),
        "current_valuation": round(current_valuation, 2),
        "risk_score": round(risk, 4),
        "components": {
            "patent_valuation": round(patent_val, 2),
            "team_valuation": round(team_val, 2),
            "rd_valuation": round(rd_val, 2),
        },
    }


if __name__ == "__main__":
    sample = {
        "patent_count": 15, "avg_patent_quality": 0.7, "team_score": 0.8,
        "rd_ratio": 0.35, "employee_count": 120, "industry_multiplier": 1.5, "stage_multiplier": 1.0,
    }
    result = predict_valuation(sample)
    print(f"Base: {result['base_valuation']}, Current: {result['current_valuation']}, Risk: {result['risk_score']}")
