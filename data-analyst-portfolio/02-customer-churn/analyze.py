"""Analyze synthetic subscription churn as a descriptive (not causal) study."""
from pathlib import Path
import json
import sqlite3

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "outputs"
OUTPUT.mkdir(exist_ok=True)

df = pd.read_csv(ROOT / "data.csv")
assert df.customer_id.is_unique and df.churned.isin([0, 1]).all()
assert df.tenure_months.ge(1).all()
segment = (df.groupby("plan", as_index=False)
           .agg(customers=("customer_id", "count"),
                churned_customers=("churned", "sum"),
                monthly_fees_usd=("monthly_fee_usd", "sum")))
segment["churn_rate_pct"] = (100 * segment.churned_customers /
                             segment.customers).round(1)
segment.to_csv(OUTPUT / "kpis.csv", index=False)
high = df[df.tickets_90d >= 4]
low = df[df.tickets_90d < 4]
summary = {
    "rows": len(df),
    "churned_customers": int(df.churned.sum()),
    "churn_rate_pct": round(100 * float(df.churned.mean()), 1),
    "high_ticket_churn_pct": round(100 * float(high.churned.mean()), 1),
    "low_ticket_churn_pct": round(100 * float(low.churned.mean()), 1),
    "churned_customer_monthly_fees_usd": int(
        df.loc[df.churned == 1, "monthly_fee_usd"].sum()),
}
with sqlite3.connect(":memory:") as conn:
    df.to_sql("customers", conn, index=False, if_exists="replace")
    pd.read_sql_query((ROOT / "queries.sql").read_text(), conn).to_csv(
        OUTPUT / "sql_results.csv", index=False)
(OUTPUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
ax = segment.plot.bar(x="plan", y="churn_rate_pct", legend=False,
                      title="Observed churn by plan", color="#8b62bd")
ax.set_ylabel("Churn rate (%)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT / "chart.png", dpi=140)
plt.close()
print(summary)
