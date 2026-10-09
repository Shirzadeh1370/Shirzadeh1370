"""Analyze retail orders and publish reproducible business KPIs."""
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

df = pd.read_csv(ROOT / "data.csv", parse_dates=["order_date"])
required = {"order_id", "order_date", "region", "category", "quantity",
            "unit_price", "unit_cost", "discount_pct", "returned"}
assert required.issubset(df.columns) and df.order_id.is_unique
assert df["discount_pct"].between(0, 1).all()
missing_regions = int(df.region.isna().sum())
df["region"] = df.region.fillna("Unknown")
df["net_sales"] = (df.quantity * df.unit_price *
                   (1 - df.discount_pct) * (1 - df.returned))
df["gross_profit"] = df.net_sales - (df.quantity * df.unit_cost * (1 - df.returned))
summary = {
    "rows": len(df),
    "net_sales_usd": round(float(df.net_sales.sum()), 2),
    "gross_profit_usd": round(float(df.gross_profit.sum()), 2),
    "gross_margin_pct": round(100 * float(df.gross_profit.sum()) /
                              float(df.net_sales.sum()), 2),
    "returned_orders": int(df.returned.sum()),
    "missing_regions_cleaned": missing_regions,
}
category = (df.groupby("category", as_index=False)
            .agg(order_count=("order_id", "count"),
                 net_sales_usd=("net_sales", "sum"),
                 gross_profit_usd=("gross_profit", "sum"))
            .sort_values("net_sales_usd", ascending=False))
category = category.round(2)
category.to_csv(OUTPUT / "kpis.csv", index=False)
with sqlite3.connect(":memory:") as conn:
    df.to_sql("orders", conn, index=False, if_exists="replace")
    pd.read_sql_query((ROOT / "queries.sql").read_text(), conn).to_csv(
        OUTPUT / "sql_results.csv", index=False)
(OUTPUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
ax = category.plot.bar(x="category", y="net_sales_usd", legend=False,
                       title="Net sales by category", color="#2766be")
ax.set_ylabel("Net sales (USD)")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.savefig(OUTPUT / "chart.png", dpi=140)
plt.close()
print(summary)
