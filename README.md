# 🏦 Trade Surveillance — Behavioral Profile Drift Detection

> Unsupervised anomaly detection system for identifying suspicious trader behavior,  
> adapted from the [IEEE-CIS Fraud Detection](https://www.kaggle.com/competitions/ieee-fraud-detection) competition dataset.

---

## 📌 Project Overview

Most Kaggle participants approach IEEE-CIS as a supervised fraud classifier.  
This project takes a different angle: **reframing the dataset as a trade surveillance problem** —  
detecting traders with anomalous behavioral patterns (spoofing, layering, erratic order sizing)  
using **Isolation Forest** without relying on labels during inference.

This is directly analogous to systems used in **custody & treasury operations**  
to flag unusual client instructions, settlement anomalies, and compliance breaches.

---

## 🗂️ Repository Structure

```
trade-surveillance/
│
├── notebooks/
│   └── trade_surveillance_ieee.ipynb   ← Main notebook (run on Google Colab)
│
├── src/
│   ├── feature_engineering.py          ← Behavioral feature pipeline
│   ├── model.py                        ← Isolation Forest wrapper
│   └── report.py                       ← Operations summary report generator
│
├── reports/
│   └── surveillance_summary.txt        ← Sample output report
│
├── assets/
│   └── column_mapping.md               ← IEEE-CIS → Trade Surveillance mapping
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔄 Column Mapping (IEEE-CIS → Trade Surveillance)

| IEEE-CIS Column | Trade Surveillance Context |
|---|---|
| `TransactionAmt` | `order_notional` — trade size in USD |
| `card1` | `trader_id` — unique trader identifier |
| `card2` | `desk_id` — trading desk / team |
| `D1–D2` | `settlement_lag` — days since last order |
| `C1` | `cancel_count` — number of cancelled orders |
| `C2` | `order_count` — total orders submitted |
| `ProductCD` | `instrument_type` — equity, FX, derivative |
| `isFraud` | `is_suspicious` — ground truth surveillance flag |

---

## ⚙️ Feature Engineering

| Feature | Description | Surveillance Signal |
|---|---|---|
| `notional_velocity` | Order size vs trader's own median | Sudden spike in order size |
| `cancel_aggression` | Cancel count / order count | High cancel rate = layering risk |
| `desk_notional_zscore` | Z-score vs desk peers | Outlier vs team behavior |
| `settlement_lag` | Days since last activity | Unusual dormancy/burst pattern |
| `lag_acceleration` | Change in settlement lag | Sudden behavioral shift |
| `is_large_order` | Top 5% notional per instrument | Block trade anomaly |
| `notional_cov` | Coefficient of variation per trader | Erratic sizing behavior |

---
<img width="1005" height="700" alt="newplot" src="https://github.com/user-attachments/assets/34adb789-d86b-42b7-9aa5-9a67692f13f2" />


## 🧠 Model

**Algorithm:** Isolation Forest (unsupervised)  
**Why unsupervised:** In real surveillance ops, labeled data is rare.  
The model detects behavioral drift without requiring confirmed fraud labels.

```
n_estimators  : 300
contamination : ~3.5% (actual fraud rate from dataset)
max_samples   : 0.8
```

**Output per order:**
- `anomaly_flag` — binary (1 = flagged)
- `anomaly_prob` — normalized risk score [0, 1]

---

## 📊 Results

| Metric | Score |
|---|---|
| ROC AUC | ~0.72–0.75 |
| Alert Threshold | 0.70 |
| Model Type | Unsupervised (no labels used in training) |

> Note: AUC < 0.9 is expected for unsupervised methods on this dataset.  
> Supervised models (XGBoost) reach 0.93+ but require labels — not realistic in ops.

---

## 🖥️ Dashboard Output

Four interactive Plotly charts:
1. **Top 20 Highest-Risk Traders** — bar chart with alert threshold line
2. **Cancel Aggression vs Anomaly Probability** — scatter with ground truth overlay
3. **Notional Velocity Distribution** — normal vs suspicious overlay histogram
4. **Feature Importance** — correlation-based ranking

---

## 🚀 How to Run

### Option A — Google Colab (Recommended)
1. Open `notebooks/trade_surveillance.ipynb` in [Google Colab](https://colab.research.google.com)
2. Download data from [kaggle.com/competitions/ieee-fraud-detection](https://www.kaggle.com/competitions/ieee-fraud-detection) → Data tab
3. Upload `train_transaction.csv` and `train_identity.csv` when prompted
4. Run all cells top to bottom



> ⚠️ Data files are NOT included in this repo (Kaggle competition rules).  
> Download directly from the competition page after joining.

---

## 💼 Relevance to Treasury & Custody Operations

| Project Feature | Real-World Ops Equivalent |
|---|---|
| Behavioral drift detection | Surveillance of unusual client instructions |
| Cancel aggression scoring | Spoofing / layering detection |
| Settlement lag analysis | Failed settlement / T+2 breach monitoring |
| Desk z-score | Peer comparison in compliance review |
| Operations summary report | Daily surveillance report to compliance team |

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-orange)
![Plotly](https://img.shields.io/badge/Plotly-5.x-purple)
![Pandas](https://img.shields.io/badge/Pandas-2.x-green)

---

## 📄 License

MIT License — data belongs to Vesta Corporation / Kaggle IEEE-CIS competition.
