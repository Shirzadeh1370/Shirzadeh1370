"""Historical weather analytics using the credited Vega/NOAA sample."""
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

df = pd.read_csv(ROOT / "data.csv", parse_dates=["date"])
assert df.date.is_unique and df.date.notna().all()
assert df.precipitation.ge(0).all()
df["month"] = df.date.dt.month
df["rain_day"] = df.precipitation.gt(0)
monthly = (df.groupby("month", as_index=False)
           .agg(observations=("date", "count"),
                avg_daily_high_c=("temp_max", "mean"),
                total_precip_mm=("precipitation", "sum"),
                observed_rain_days=("rain_day", "sum")))
monthly["rain_day_pct"] = (100 * monthly.observed_rain_days /
                           monthly.observations).round(1)
monthly = monthly.round(2)
monthly.to_csv(OUTPUT / "kpis.csv", index=False)
summary = {
    "rows": len(df),
    "start_date": str(df.date.min().date()),
    "end_date": str(df.date.max().date()),
    "rain_day_pct": round(100 * float(df.rain_day.mean()), 1),
    "warmest_month_by_avg_daily_high": int(
        monthly.loc[monthly.avg_daily_high_c.idxmax(), "month"]),
    "wettest_month_by_pooled_precipitation": int(
        monthly.loc[monthly.total_precip_mm.idxmax(), "month"]),
}
with sqlite3.connect(":memory:") as conn:
    df.to_sql("weather", conn, index=False, if_exists="replace")
    pd.read_sql_query((ROOT / "queries.sql").read_text(), conn).to_csv(
        OUTPUT / "sql_results.csv", index=False)
(OUTPUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
ax = monthly.plot.line(x="month", y="avg_daily_high_c", marker="o",
                       legend=False, title="Seattle average daily high by month",
                       color="#2766be")
ax.set_xticks(range(1, 13))
ax.set_ylabel("Temperature (°C)")
plt.tight_layout()
plt.savefig(OUTPUT / "chart.png", dpi=140)
plt.close()
print(summary)
