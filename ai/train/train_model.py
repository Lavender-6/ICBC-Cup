"""训练 XGBoost 估值预测模型。

使用 ColumnTransformer 做特征预处理（OneHot + passthrough），
训练 XGBRegressor 预测 base_valuation 和 current_valuation，
训练单独的 XGBRegressor 预测 risk_score。
最终将三个模型 + 预处理器打包为 Pipeline 保存为 joblib。
"""
import os
import sys
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "train_dataset.csv")
EXPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "export")
MODEL_FILE = os.path.join(EXPORT_DIR, "valuation_model.joblib")

CATEGORICAL_FEATS = ["industry", "stage"]
NUMERIC_FEATS = ["patent_count", "avg_patent_quality", "team_score", "rd_ratio", "employee_count", "founded_year"]
ALL_FEATURES = CATEGORICAL_FEATS + NUMERIC_FEATS

TARGETS = ["base_valuation", "current_valuation", "risk_score"]


def train_target_pipeline(df: pd.DataFrame, target: str) -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATS),
            ("num", "passthrough", NUMERIC_FEATS),
        ]
    )
    xgb_params = {
        "n_estimators": 300,
        "max_depth": 6,
        "learning_rate": 0.05,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "reg_alpha": 0.1,
        "reg_lambda": 1.0,
        "random_state": 42,
    }
    if target == "risk_score":
        xgb_params["objective"] = "reg:squarederror"
        xgb_params["n_estimators"] = 200

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", XGBRegressor(**xgb_params)),
    ])
    pipeline.fit(df[ALL_FEATURES], df[target])
    return pipeline


def evaluate(pipeline: Pipeline, X_test: pd.DataFrame, y_test: pd.Series, target: str):
    y_pred = pipeline.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"  [{target}] R²={r2:.4f}  MAE={mae:.2f}  RMSE={rmse:.2f}")
    return r2


def main():
    if not os.path.exists(DATA_FILE):
        print("训练数据不存在，先运行 generate_data.py")
        sys.exit(1)

    df = pd.read_csv(DATA_FILE)
    print(f"加载数据集: {len(df)} 条样本")
    print(f"特征: {ALL_FEATURES}")
    print(f"目标: {TARGETS}\n")

    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    print(f"训练集: {len(train_df)}  测试集: {len(test_df)}\n")

    models = {}
    print("训练模型:")
    for target in TARGETS:
        pipeline = train_target_pipeline(train_df, target)
        evaluate(pipeline, test_df[ALL_FEATURES], test_df[target], target)
        models[target] = pipeline

    os.makedirs(EXPORT_DIR, exist_ok=True)
    joblib.dump(models, MODEL_FILE)
    print(f"\n模型已保存: {MODEL_FILE}")
    print(f"文件大小: {os.path.getsize(MODEL_FILE) / 1024:.1f} KB")

    sample = test_df.iloc[:3]
    print("\n推理示例:")
    for target in TARGETS:
        preds = models[target].predict(sample[ALL_FEATURES])
        for i, (pred, actual) in enumerate(zip(preds, sample[target])):
            print(f"  [{target}] 样本{i}: 预测={pred:.2f}  实际={actual:.2f}  误差={abs(pred-actual):.2f}")


if __name__ == "__main__":
    main()
