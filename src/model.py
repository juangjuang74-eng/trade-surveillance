"""
model.py
────────
Isolation Forest wrapper for trade surveillance anomaly detection.
"""

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


class SurveillanceModel:
    def __init__(self, contamination: float = 0.035, n_estimators: int = 300):
        self.contamination = contamination
        self.n_estimators  = n_estimators
        self.scaler        = StandardScaler()
        self.model         = IsolationForest(
            n_estimators  = n_estimators,
            contamination = contamination,
            max_samples   = 0.8,
            random_state  = 42,
            n_jobs        = -1,
        )

    def fit_predict(self, X: np.ndarray) -> tuple:
        """Fit model and return (anomaly_flag, anomaly_prob)."""
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)

        flags = self.model.predict(X_scaled)
        flags = np.where(flags == -1, 1, 0)           # 1 = anomaly

        raw   = -self.model.score_samples(X_scaled)
        probs = (raw - raw.min()) / (raw.max() - raw.min())  # normalize [0,1]

        return flags, probs
