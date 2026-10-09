# 04 — IPv4 VLSM Subnet Planner

**Scenario:** A network technician must split an IPv4 network into right-sized subnets for an office LAN, lab, guest Wi-Fi, management, and a point-to-point link.

**What it does:** Uses Python's standard ipaddress library to allocate non-overlapping subnets, in largest-request-first order, from an input CIDR. It validates usable host capacity and returns network/mask, first and last usable, gateway **suggestion**, broadcast, and spare hosts.

## Run
~~~powershell
python planner.py --base 192.168.50.0/24
python -m unittest test_planner.py -v
~~~

Generated files: outputs/plan.csv and outputs/plan.json.

## Sample plan
| Segment | Requested hosts | Allocated block |
| --- | ---: | --- |
| Office LAN | 50 | 192.168.50.0/26 |
| Lab LAN | 25 | 192.168.50.64/27 |
| Guest WiFi | 15 | 192.168.50.96/27 |
| Management | 8 | 192.168.50.128/28 |
| Point-to-Point | 2 | 192.168.50.144/30 |

**Skills:** IPv4 addressing, VLSM, CIDR, Python ipaddress, capacity planning, automated overlap and capacity tests.

**Design limitations:** IPv4 only; default point-to-point allocation uses /30 rather than /31; gateway is a suggested convention, not an actual device setting; no DHCP, VLAN, routing or switch changes are made.

**Interview talking point:** "I automated repeatable VLSM subnet planning and tested every allocation for address capacity and overlap."

Reference: https://docs.python.org/3/library/ipaddress.html
