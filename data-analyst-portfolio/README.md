# Entry-Level Data Analyst Portfolio: Five Reproducible Projects

This portfolio demonstrates introductory, job-relevant analytics workflows: turning CSV datasets into clean tables, defining meaningful KPIs, checking results with SQL, and visualizing findings with Python.

| # | Project | Analytics strengths | Data |
|---|---|---|---|
| 01 | [Retail Sales & Profit](01-retail-sales/) | Net sales, gross margin, missing values, SQL aggregation | 480 synthetic orders |
| 02 | [Subscription Churn](02-customer-churn/) | Segmentation, churn-rate denominators, interpretation | 360 synthetic customers |
| 03 | [IT Help Desk SLA](03-helpdesk-sla/) | Backlog, median resolution, SLAs, CSAT coverage | 420 synthetic tickets |
| 04 | [Login Security Analytics](04-login-security/) | Timestamps, failure counts, transparent detection thresholds | 744 synthetic events |
| 05 | [Seattle Weather Trends](05-seattle-weather/) | Real public daily measurements, monthly seasonality | 1,461 historical observations |

## Quick start (Windows PowerShell)

~~~powershell
git clone https://github.com/Shirzadeh1370/Shirzadeh1370.git
cd Shirzadeh1370/data-analyst-portfolio
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run_all.py
python -m unittest discover -s tests -v
~~~

On macOS/Linux: create the virtual environment with python3 -m venv .venv, activate with source .venv/bin/activate, and use python thereafter.

Generated per-project outputs: **outputs/kpis.csv**, **outputs/sql_results.csv**, **outputs/summary.json**, **outputs/chart.png**. All five folders contain a self-contained analysis script, a real executable SQL query, sample findings and an SVG preview that can be viewed directly on GitHub.

## Skills demonstrated
- Python data analysis (pandas), CSV ingestion, data type conversion, grouping and aggregation
- SQL aggregation with SQLite: GROUP BY, CASE WHEN, NULLIF, date grouping
- Data quality: uniqueness checks, missing-value handling, numeric range checks
- KPI definitions and denominator discipline
- Charts with matplotlib and reproducible programmatic reporting
- Basic automated project smoke tests with unittest and GitHub Actions

## Important transparency notes
**Projects 01–04 use synthetic datasets explicitly designed for demonstration, not client or employer records.** Figures derived from them should never be presented as measured business outcomes or personal work history. Project 05 uses historical observations attributed to NOAA via [Vega Datasets](https://github.com/vega/vega-datasets/blob/main/data/seattle-weather.csv), with the source's instructional transformation and license metadata described in that project's README.

The portfolio proves reproducible analysis work on training samples. It does not claim production deployments, paid business results, Power BI reports, or advanced machine learning.

## Resume-friendly truthful description

**Data Analytics Portfolio | Independent Projects**  
- Built five reproducible Python/SQL portfolio analyses covering retail KPIs, subscription churn, IT support SLA reporting, security log triage, and Seattle historical weather patterns.
- Cleaned and validated CSV datasets; automated KPI reporting and charts using pandas, matplotlib and SQLite.
- Wrote SQL queries to aggregate category performance, segment churn, measure SLA attainment, identify login-failure bursts, and explore monthly weather trends.
- Published documented analyses, example findings, and automated end-to-end tests on GitHub.

## What to explain in an interview
For any project, be ready to describe: (1) the business question; (2) data origins, grain, and limitations; (3) cleaning checks; (4) exact KPI numerators and denominators; (5) one finding, and why it may not generalize; (6) one next step with a larger real dataset.

Each project folder contains a short interview talking point. Projects are intended to be reviewed and extended, not simply copied without understanding.
