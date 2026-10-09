-- Investigation candidates: >=8 failed logins per user per calendar day.
-- This threshold is a demonstration rule, not a proof of credential attacks.
SELECT DATE(timestamp) AS event_date, username,
       SUM(CASE WHEN result = 'FAIL' THEN 1 ELSE 0 END) AS failures,
       COUNT(*) AS events
FROM events
GROUP BY DATE(timestamp), username
HAVING SUM(CASE WHEN result = 'FAIL' THEN 1 ELSE 0 END) >= 8
ORDER BY failures DESC, event_date ASC;
