"""估值模型 + 破产风险模型推理模块。

加载训练好的 XGBoost 模型，提供 predict 函数供后端调用。
模型不存在时自动回退到规则公式（graceful degradation）。
"""
import os
import json
import joblib
import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

MODEL_FILE = os.path.join(os.path.dirname(__file__), "..", "export", "valuation_model.joblib")
BANKRUPTCY_MODEL_FILE = os.path.join(os.path.dirname(__file__), "..", "export", "bankruptcy_model.joblib")
FEATURE_STATS_FILE = os.path.join(os.path.dirname(__file__), "..", "export", "feature_stats.json")

FEATURE_COLUMNS = [
    "industry", "stage", "patent_count", "avg_patent_quality",
    "team_score", "rd_ratio", "employee_count", "founded_year",
]

_models: dict | None = None
_bankruptcy_model: dict | None = None
_feature_stats: dict | None = None


def _load_models() -> dict | None:
    global _models
    if _models is not None:
        return _models
    if os.path.exists(MODEL_FILE):
        try:
            _models = joblib.load(MODEL_FILE)
            logger.info("XGBoost 估值模型加载成功: %s", MODEL_FILE)
            return _models
        except Exception as e:
            logger.warning("模型加载失败，回退到规则公式: %s", e)
            return None
    logger.warning("模型文件不存在 (%s)，回退到规则公式", MODEL_FILE)
    return None


def predict_valuation(features: dict) -> dict | None:
    """用 XGBoost 模型预测估值。

    Args:
        features: 包含 industry, stage, patent_count, avg_patent_quality,
                  team_score, rd_ratio, employee_count, founded_year 的字典

    Returns:
        {"base_valuation": float, "current_valuation": float, "risk_score": float}
        或 None（模型不可用时）
    """
    models = _load_models()
    if models is None:
        return None

    row = pd.DataFrame([{
        "industry": features.get("industry", "default"),
        "stage": features.get("stage", "立项预研"),
        "patent_count": features.get("patent_count", 0),
        "avg_patent_quality": features.get("avg_patent_quality", 0.0),
        "team_score": features.get("team_score", 0.0),
        "rd_ratio": features.get("rd_ratio", 0.0),
        "employee_count": features.get("employee_count", 0),
        "founded_year": features.get("founded_year", 2020),
    }])

    try:
        base_val = float(models["base_valuation"].predict(row)[0])
        current_val = float(models["current_valuation"].predict(row)[0])
        risk = float(np.clip(models["risk_score"].predict(row)[0], 0.0, 1.0))

        base_val = max(100.0, base_val)
        current_val = max(100.0, current_val)

        return {
            "base_valuation": round(base_val, 2),
            "current_valuation": round(current_val, 2),
            "risk_score": round(risk, 4),
        }
    except Exception as e:
        logger.warning("模型推理失败，回退到规则公式: %s", e)
        return None


def is_model_available() -> bool:
    return _load_models() is not None


def _load_bankruptcy_model() -> dict | None:
    global _bankruptcy_model
    if _bankruptcy_model is not None:
        return _bankruptcy_model
    if os.path.exists(BANKRUPTCY_MODEL_FILE):
        try:
            _bankruptcy_model = joblib.load(BANKRUPTCY_MODEL_FILE)
            logger.info("破产风险模型加载成功: %s", BANKRUPTCY_MODEL_FILE)
            return _bankruptcy_model
        except Exception as e:
            logger.warning("破产模型加载失败: %s", e)
            return None
    logger.warning("破产模型文件不存在 (%s)", BANKRUPTCY_MODEL_FILE)
    return None


def _load_feature_stats() -> dict | None:
    global _feature_stats
    if _feature_stats is not None:
        return _feature_stats
    if os.path.exists(FEATURE_STATS_FILE):
        try:
            with open(FEATURE_STATS_FILE, "r", encoding="utf-8") as f:
                _feature_stats = json.load(f)
            return _feature_stats
        except Exception as e:
            logger.warning("特征统计加载失败: %s", e)
            return None
    return None


def generate_financial_metrics(industry: str = "半导体", stage: str = "立项预研") -> str:
    """根据训练数据集的分布，为企业生成模拟财务特征（JSON 字符串）。

    基于行业/阶段调整分布偏移：早期阶段企业财务指标偏低，成熟阶段偏高。
    """
    stats = _load_feature_stats()
    if stats is None:
        return json.dumps({})

    stage_bias = {
        "立项预研": -0.3, "原型验证": -0.1, "流片成功": 0.0,
        "商业化量产": 0.2, "上市预备": 0.4,
    }.get(stage, 0.0)

    metrics = {}
    for col, s in stats.items():
        mean = s["mean"]
        std = s["std"]
        val = np.random.normal(mean + mean * stage_bias * 0.1, std * 0.8)
        val = float(np.clip(val, s["min"], s["max"]))
        metrics[col] = round(val, 6)

    return json.dumps(metrics)


def predict_bankruptcy_risk(financial_metrics_json: str) -> float | None:
    """用破产风险模型预测企业破产概率（0-1）。

    Args:
        financial_metrics_json: JSON 字符串，包含 95 个财务特征

    Returns:
        破产概率 (0.0-1.0)，或 None（模型不可用时）
    """
    bk_model = _load_bankruptcy_model()
    if bk_model is None:
        return None

    try:
        metrics = json.loads(financial_metrics_json) if financial_metrics_json else {}
        if not metrics:
            return None

        model = bk_model["model"]
        feature_names = bk_model["feature_names"]

        row = pd.DataFrame([{col: metrics.get(col, 0.0) for col in feature_names}])
        proba = model.predict_proba(row)[0, 1]
        return round(float(np.clip(proba, 0.0, 1.0)), 4)
    except Exception as e:
        logger.warning("破产风险推理失败: %s", e)
        return None


def is_bankruptcy_model_available() -> bool:
    return _load_bankruptcy_model() is not None
