-- Customer-level snapshot; not a longitudinal survival model.
SELECT plan, COUNT(*) AS customers, SUM(churned) AS churned_customers,
       ROUND(100.0 * AVG(churned), 1) AS churn_rate_pct
FROM customers
GROUP BY plan
ORDER BY churn_rate_pct DESC;
