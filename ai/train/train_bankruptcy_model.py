"""训练企业破产风险预测模型（XGBoost 二分类）。

数据集：台湾企业破产数据，6819 条样本，95 个财务特征，破产率 3.23%。
处理类别不平衡：scale_pos_weight = neg/pos。
输出：破产概率（0-1），作为企业 risk_score。
"""
import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report, roc_auc_score, accuracy_score,
    recall_score, f1_score, confusion_matrix,
)
from xgboost import XGBClassifier

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "bankruptcy_data.csv")
EXPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "export")
MODEL_FILE = os.path.join(EXPORT_DIR, "bankruptcy_model.joblib")
STATS_FILE = os.path.join(EXPORT_DIR, "feature_stats.json")

LABEL_COL = "Bankrupt?"


def main():
    if not os.path.exists(DATA_FILE):
        print("数据集不存在:", DATA_FILE)
        sys.exit(1)

    df = pd.read_csv(DATA_FILE)
    print(f"数据集: {df.shape[0]} 行 x {df.shape[1]} 列")

    y = df[LABEL_COL].astype(int)
    X = df.drop(columns=[LABEL_COL])
    feature_names = list(X.columns)
    print(f"特征数: {len(feature_names)}")
    print(f"类别分布: 未破产={sum(y==0)}, 破产={sum(y==1)}, 破产率={y.mean():.2%}\n")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"训练集: {len(X_train)}  测试集: {len(X_test)}")

    scale_pos_weight = sum(y_train == 0) / sum(y_train == 1)
    print(f"scale_pos_weight: {scale_pos_weight:.1f}\n")

    model = XGBClassifier(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.6,
        scale_pos_weight=scale_pos_weight,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=42,
        eval_metric="auc",
        use_label_encoder=False,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("评估结果:")
    print(f"  Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"  AUC:       {roc_auc_score(y_test, y_proba):.4f}")
    print(f"  Recall:    {recall_score(y_test, y_pred):.4f}")
    print(f"  F1:        {f1_score(y_test, y_pred):.4f}")
    print(f"\n混淆矩阵:")
    print(confusion_matrix(y_test, y_pred))
    print(f"\n分类报告:")
    print(classification_report(y_test, y_pred, target_names=["未破产", "破产"]))

    os.makedirs(EXPORT_DIR, exist_ok=True)
    joblib.dump({"model": model, "feature_names": feature_names}, MODEL_FILE)
    print(f"\n模型已保存: {MODEL_FILE}")
    print(f"文件大小: {os.path.getsize(MODEL_FILE) / 1024:.1f} KB")

    stats = {}
    for col in feature_names:
        stats[col] = {
            "mean": float(X[col].mean()),
            "std": float(X[col].std()),
            "min": float(X[col].min()),
            "max": float(X[col].max()),
            "median": float(X[col].median()),
        }
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False)
    print(f"特征统计已保存: {STATS_FILE}")

    importances = model.feature_importances_
    idx = np.argsort(importances)[::-1][:15]
    print("\nTop 15 重要特征:")
    for i in idx:
        print(f"  {feature_names[i].strip():60s}  {importances[i]:.4f}")


if __name__ == "__main__":
    main()
