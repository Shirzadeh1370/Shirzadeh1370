-- SLA attainment denominator: resolved tickets only. Open tickets are backlog.
SELECT priority,
       COUNT(*) AS all_tickets,
       SUM(CASE WHEN resolved = 0 THEN 1 ELSE 0 END) AS unresolved_tickets,
       SUM(CASE WHEN resolved = 1 THEN 1 ELSE 0 END) AS resolved_tickets,
       ROUND(100.0 * SUM(CASE WHEN resolved = 1 AND resolution_hours <= sla_hours THEN 1 ELSE 0 END)
           / NULLIF(SUM(resolved), 0), 1) AS sla_met_pct_resolved
FROM tickets
GROUP BY priority
ORDER BY priority;
