"""Security event aggregation: triage flags are not attack determinations."""
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

df = pd.read_csv(ROOT / "data.csv", parse_dates=["timestamp"])
assert df.event_id.is_unique and df.result.isin(["SUCCESS", "FAIL"]).all()
df["event_date"] = df.timestamp.dt.strftime("%Y-%m-%d")
df["failed"] = df.result.eq("FAIL").astype(int)
flags = (df.groupby(["event_date", "username"], as_index=False)
         .agg(failures=("failed", "sum"), events=("event_id", "count")))
flags = flags.loc[flags.failures >= 8].sort_values(
    ["failures", "event_date"], ascending=[False, True])
flags.to_csv(OUTPUT / "kpis.csv", index=False)
by_country = (df.groupby("country")["failed"].sum()
              .sort_values(ascending=False))
summary = {
    "rows": len(df),
    "failed_logins": int(df.failed.sum()),
    "failure_rate_pct": round(100 * float(df.failed.mean()), 1),
    "flagged_user_days_gte_8_failures": len(flags),
    "distinct_users": int(df.username.nunique()),
    "distinct_source_ranges": int(df.source_ip_range.nunique()),
}
with sqlite3.connect(":memory:") as conn:
    df.to_sql("events", conn, index=False, if_exists="replace")
    pd.read_sql_query((ROOT / "queries.sql").read_text(), conn).to_csv(
        OUTPUT / "sql_results.csv", index=False)
(OUTPUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
ax = by_country.plot.bar(title="Failed login events by country",
                         color="#c5624e")
ax.set_ylabel("Failed events")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT / "chart.png", dpi=140)
plt.close()
print(summary)
