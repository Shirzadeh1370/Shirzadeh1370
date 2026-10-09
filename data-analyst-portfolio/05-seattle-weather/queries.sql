-- Real observations pooled across 2012–2015; not a live weather forecast.
SELECT CAST(strftime('%m', date) AS INTEGER) AS month,
       COUNT(*) AS observations,
       ROUND(AVG(temp_max), 2) AS avg_daily_high_c,
       ROUND(SUM(precipitation), 2) AS total_precip_mm,
       SUM(CASE WHEN precipitation > 0 THEN 1 ELSE 0 END) AS observed_rain_days
FROM weather
GROUP BY strftime('%m', date)
ORDER BY month;
