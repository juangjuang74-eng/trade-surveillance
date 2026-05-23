# Column Mapping — IEEE-CIS → Trade Surveillance

## Core Columns

| IEEE-CIS Column  | Trade Surveillance Context        | Notes                              |
|------------------|-----------------------------------|------------------------------------|
| `TransactionAmt` | `order_notional`                  | Trade size in USD                  |
| `card1`          | `trader_id`                       | Unique trader identifier           |
| `card2`          | `desk_id`                         | Trading desk / team                |
| `D1`             | `order_lifetime_d1`               | Days since last order (proxy)      |
| `D2`             | `order_lifetime_d2`               | Settlement lag (proxy)             |
| `C1`             | `cancel_count`                    | Number of cancelled orders         |
| `C2`             | `order_count`                     | Total orders submitted             |
| `ProductCD`      | `instrument_type`                 | W=equity, H=FX, C=derivative, etc. |
| `isFraud`        | `is_suspicious`                   | Ground truth surveillance flag     |

## Engineered Features

| Feature               | Formula                                      | Signal                        |
|-----------------------|----------------------------------------------|-------------------------------|
| `notional_velocity`   | order / trader_median                        | Sudden size spike             |
| `cancel_aggression`   | cancel_count / order_count                   | Layering / spoofing risk      |
| `desk_notional_zscore`| (order - desk_mean) / desk_std               | Outlier vs peers              |
| `settlement_lag`      | D1 (fillna 0)                                | Dormancy / burst pattern      |
| `lag_acceleration`    | D2 - D1                                      | Sudden behavioral shift       |
| `is_large_order`      | order > 95th percentile per instrument       | Block trade anomaly           |
| `notional_cov`        | trader_std / trader_mean                     | Erratic sizing behavior       |
