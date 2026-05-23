"""
report.py
─────────
Operations summary report generator for trade surveillance.
"""

import pandas as pd


def print_summary(model_df: pd.DataFrame, auc: float, threshold: float = 0.7) -> None:
    high_risk      = model_df[model_df["anomaly_prob"] > threshold]
    confirmed_hits = model_df[
        (model_df["anomaly_prob"] > threshold) & (model_df["is_suspicious"] == 1)
    ]
    total_susp = int(model_df["is_suspicious"].sum())

    print("=" * 60)
    print("       TRADE SURVEILLANCE — OPERATIONS SUMMARY REPORT")
    print("=" * 60)
    print(f"  Total orders monitored       : {len(model_df):>12,}")
    print(f"  Unique traders tracked       : {model_df['trader_id'].nunique():>12,}")
    print(f"  Orders flagged (>{threshold}) : {len(high_risk):>12,}")
    print(f"  Confirmed suspicious orders  : {total_susp:>12,}")
    print(f"  True positives detected      : {len(confirmed_hits):>12,}")
    print(f"  Detection rate               : {len(confirmed_hits)/total_susp:.2%}")
    print(f"  ROC AUC                      : {auc:>12.4f}")
    print("=" * 60)
