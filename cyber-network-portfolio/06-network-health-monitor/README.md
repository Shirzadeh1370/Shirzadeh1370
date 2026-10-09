# 06 — Network Health / SLA Monitor (Offline)

**Scenario:** A network support technician wants a daily health summary from periodic ping probe records instead of manually reading long console output.

**What it calculates:** Per-device probe counts, packet loss percentage and 95th-percentile successful-probe latency (nearest-rank rule). Marks devices DEGRADED if packet loss exceeds 5% or p95 latency exceeds 100 ms (demonstration thresholds only).

## Run
~~~powershell
python monitor.py
python -m unittest test_monitor.py -v
~~~

Output: outputs/health.json.

**Example:** 60 simulated observations across router-A, switch-B and wifi-AP. router-A is healthy; switch-B has 20% packet loss; wifi-AP shows loss and a high-latency outlier.

**Skills:** packet loss, latency, p95 statistics, basic SLA/SLO definitions, CSV validation, automation and reporting.

**Important:** This does **not** ping devices, scan IP addresses or collect real traffic. Sample probes are synthetic. Packet loss/ICMP response alone does not measure complete application availability; thresholds must be based on operational requirements.

**Interview talking point:** "I transformed structured probe records into network health indicators and tested edge cases such as failed probes with missing latency."
