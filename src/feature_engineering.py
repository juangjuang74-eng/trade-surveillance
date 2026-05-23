"""
feature_engineering.py
─────────────────────
Behavioral feature pipeline for trade surveillance.
Adapted from IEEE-CIS Fraud Detection dataset.
"""

import pandas as pd
import numpy as np


COLUMN_MAP = {
    "TransactionAmt": "order_notional",
    "card1":          "trader_id",
    "card2":          "desk_id",
    "D1":             "order_lifetime_d1",
    "D2":             "order_lifetime_d2",
    "C1":             "cancel_count",
    "C2":             "order_count",
    "ProductCD":      "instrument_type",
    "isFraud":        "is_suspicious",
}


def remap_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remap IEEE-CIS columns to trade surveillance context."""
    df = df.copy()
    for src, dst in COLUMN_MAP.items():
        if src in df.columns:
            df[dst] = df[src]

    df["order_type"] = np.where(
        df["order_notional"] > df["order_notional"].median(), "BUY", "SELL"
    )
    df["cancel_rate"] = df["cancel_count"] / (df["order_count"] + 1e-8)
    df["notional_bucket"] = pd.qcut(
        df["order_notional"], q=5, labels=["XS", "S", "M", "L", "XL"]
    )
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build behavioral profile features per trader.

    Features
    --------
    notional_velocity    : order size relative to trader's own median
    cancel_aggression    : cancel count / total orders
    desk_notional_zscore : z-score vs desk peers
    settlement_lag       : proxy for days since last order
    lag_acceleration     : change in settlement lag
    is_large_order       : top 5% notional per instrument (binary)
    notional_cov         : coefficient of variation per trader
    trader_*             : trader-level aggregates
    """
    df = df.copy()

    # Notional velocity
    trader_median = df.groupby("trader_id")["order_notional"].transform("median")
    df["notional_velocity"] = df["order_notional"] / (trader_median + 1e-8)

    # Cancel aggression
    df["cancel_aggression"] = df["cancel_count"] / (df["order_count"] + 1e-8)

    # Desk z-score
    desk_mean = df.groupby("desk_id")["order_notional"].transform("mean")
    desk_std  = df.groupby("desk_id")["order_notional"].transform("std").fillna(1)
    df["desk_notional_zscore"] = (df["order_notional"] - desk_mean) / (desk_std + 1e-8)

    # Settlement lag
    df["settlement_lag"]   = df["order_lifetime_d1"].fillna(0)
    df["lag_acceleration"] = (
        df["order_lifetime_d2"].fillna(0) - df["order_lifetime_d1"].fillna(0)
    )

    # Large order flag
    df["is_large_order"] = (
        df.groupby("instrument_type")["order_notional"]
        .transform(lambda x: x > x.quantile(0.95))
    ).astype(int)

    # Trader-level aggregates
    trader_agg = df.groupby("trader_id").agg(
        trader_avg_notional = ("order_notional",    "mean"),
        trader_std_notional = ("order_notional",    "std"),
        trader_cancel_rate  = ("cancel_aggression", "mean"),
        trader_large_orders = ("is_large_order",    "sum"),
        trader_order_count  = ("order_count",       "sum"),
    ).reset_index()

    df = df.merge(trader_agg, on="trader_id", how="left")
    df["notional_cov"] = df["trader_std_notional"] / (df["trader_avg_notional"] + 1e-8)

    return df


FEATURE_COLS = [
    "order_notional", "cancel_aggression", "notional_velocity",
    "desk_notional_zscore", "settlement_lag", "lag_acceleration",
    "is_large_order", "trader_avg_notional", "trader_std_notional",
    "trader_cancel_rate", "trader_large_orders", "trader_order_count",
    "notional_cov", "order_count", "cancel_count",
]
