-- SQLite: returned orders contribute zero net sales and zero gross profit.
SELECT category,
       COUNT(*) AS order_count,
       ROUND(SUM(quantity * unit_price * (1 - discount_pct) * (1 - returned)), 2) AS net_sales_usd,
       ROUND(SUM(quantity * (unit_price * (1 - discount_pct) - unit_cost) * (1 - returned)), 2) AS gross_profit_usd
FROM orders
GROUP BY category
ORDER BY net_sales_usd DESC;
