"""生成硬科技企业模拟训练数据集。

模拟 2000 家硬科技企业的特征与估值，包含非线性关系和交互项，
使 XGBoost 模型能学习到有意义的模式（而非简单线性回归可拟合）。
"""
import os
import numpy as np
import pandas as pd

np.random.seed(42)

N_SAMPLES = 2000
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "train_dataset.csv")

INDUSTRIES = ["半导体", "航天", "生物医药", "高端装备", "新材料", "人工智能"]
INDUSTRY_WEIGHTS = [0.20, 0.15, 0.20, 0.15, 0.15, 0.15]
INDUSTRY_MULT = {"半导体": 1.5, "航天": 1.3, "生物医药": 1.4, "高端装备": 1.2, "新材料": 1.1, "人工智能": 1.6}

STAGES = ["立项预研", "原型验证", "流片成功", "商业化量产", "上市预备"]
STAGE_WEIGHTS = [0.25, 0.25, 0.20, 0.20, 0.10]
STAGE_MULT = {"立项预研": 0.3, "原型验证": 0.6, "流片成功": 1.0, "商业化量产": 1.5, "上市预备": 2.0}


def generate_dataset(n: int = N_SAMPLES) -> pd.DataFrame:
    rows = []
    for _ in range(n):
        industry = np.random.choice(INDUSTRIES, p=INDUSTRY_WEIGHTS)
        stage = np.random.choice(STAGES, p=STAGE_WEIGHTS)
        ind_mult = INDUSTRY_MULT[industry]
        stg_mult = STAGE_MULT[stage]

        patent_count = int(np.random.randint(5, 51))
        avg_patent_quality = float(np.random.beta(2, 1.5))
        team_score = float(np.random.beta(2, 2))
        rd_ratio = float(np.random.uniform(0.10, 0.80))
        employee_count = int(np.random.randint(10, 501))
        founded_year = int(np.random.randint(2010, 2025))

        patent_val = patent_count ** 0.7 * avg_patent_quality * 500 * ind_mult
        team_val = team_score ** 1.5 * np.log(employee_count) * 300 * ind_mult
        rd_val = rd_ratio * employee_count ** 0.8 * 100
        synergy = (avg_patent_quality * team_score) ** 0.5 * 200 * ind_mult

        base_valuation = patent_val + team_val + rd_val + synergy
        noise = np.random.normal(0, 0.08)
        base_valuation *= (1.0 + noise)
        base_valuation = max(100.0, base_valuation)

        current_valuation = base_valuation * stg_mult * (1.0 + np.random.normal(0, 0.05))

        quality_risk = 1.0 - avg_patent_quality
        team_risk = 1.0 - team_score
        scale_risk = 1.0 / (1.0 + patent_count * 0.1)
        rd_risk = 1.0 - min(rd_ratio, 1.0)
        risk_score = 0.30 * quality_risk + 0.30 * team_risk + 0.20 * scale_risk + 0.20 * rd_risk
        risk_score = float(np.clip(risk_score + np.random.normal(0, 0.02), 0.0, 1.0))

        rows.append({
            "industry": industry,
            "stage": stage,
            "patent_count": patent_count,
            "avg_patent_quality": round(avg_patent_quality, 4),
            "team_score": round(team_score, 4),
            "rd_ratio": round(rd_ratio, 4),
            "employee_count": employee_count,
            "founded_year": founded_year,
            "base_valuation": round(base_valuation, 2),
            "current_valuation": round(current_valuation, 2),
            "risk_score": round(risk_score, 4),
        })

    return pd.DataFrame(rows)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = generate_dataset()
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"数据集已生成: {OUTPUT_FILE}")
    print(f"样本数: {len(df)}")
    print(f"\n估值统计 (万元):")
    print(df[["base_valuation", "current_valuation", "risk_score"]].describe().round(2))
    print(f"\n行业分布:")
    print(df["industry"].value_counts())
    print(f"\n阶段分布:")
    print(df["stage"].value_counts())


if __name__ == "__main__":
    main()
