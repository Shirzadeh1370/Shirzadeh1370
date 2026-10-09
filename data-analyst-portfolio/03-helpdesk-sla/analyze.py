"""Produce an IT support SLA report with correct resolved-ticket denominators."""
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

df = pd.read_csv(ROOT / "data.csv", parse_dates=["created_date"])
assert df.ticket_id.is_unique and df.resolved.isin([0, 1]).all()
assert df.loc[df.resolved == 0, "resolution_hours"].isna().all()
df["met_sla"] = ((df.resolved == 1) &
                 (df.resolution_hours <= df.sla_hours))
resolved = df.loc[df.resolved == 1].copy()
report = (df.groupby("priority", as_index=False)
          .agg(all_tickets=("ticket_id", "count"),
               resolved_tickets=("resolved", "sum"),
               met_sla=("met_sla", "sum")))
report["unresolved_tickets"] = report.all_tickets - report.resolved_tickets
report["sla_met_pct_resolved"] = (
    100 * report.met_sla / report.resolved_tickets).round(1)
report.to_csv(OUTPUT / "kpis.csv", index=False)
summary = {
    "rows": len(df),
    "open_tickets": int((df.resolved == 0).sum()),
    "resolved_tickets": len(resolved),
    "sla_met_pct_of_resolved": round(100 * float(resolved.met_sla.mean()), 1),
    "median_resolution_hours": round(float(
        resolved.resolution_hours.median()), 1),
    "csat_response_pct_of_resolved": round(
        100 * float(resolved.csat_score.notna().mean()), 1),
}
with sqlite3.connect(":memory:") as conn:
    df.to_sql("tickets", conn, index=False, if_exists="replace")
    pd.read_sql_query((ROOT / "queries.sql").read_text(), conn).to_csv(
        OUTPUT / "sql_results.csv", index=False)
(OUTPUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
ax = report.plot.bar(x="priority", y="unresolved_tickets", legend=False,
                     title="Unresolved tickets by priority", color="#178a82")
ax.set_ylabel("Ticket count")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT / "chart.png", dpi=140)
plt.close()
print(summary)
