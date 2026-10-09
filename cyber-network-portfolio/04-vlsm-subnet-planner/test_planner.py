import ipaddress
from pathlib import Path
import unittest
from planner import allocate, read_requirements


class PlannerTests(unittest.TestCase):
    def test_fixture_is_nonoverlapping_and_adequate(self):
        root = Path(__file__).parent
        items = read_requirements(root / "data/requirements.csv")
        plan = allocate("192.168.50.0/24", items)
        self.assertEqual(len(plan), 5)
        networks = [ipaddress.ip_network(row["subnet"]) for row in plan]
        base = ipaddress.ip_network("192.168.50.0/24")
        for index, current in enumerate(networks):
            self.assertTrue(current.subnet_of(base))
            self.assertGreaterEqual(current.num_addresses - 2, plan[index]["required_hosts"])
            for other in networks[index + 1:]:
                self.assertFalse(current.overlaps(other))
        self.assertEqual(plan[0]["subnet"], "192.168.50.0/26")

    def test_insufficient_space_is_rejected(self):
        with self.assertRaises(ValueError):
            allocate("10.0.0.0/28", [("a", 10), ("b", 10)])

    def test_reject_duplicate_names(self):
        with self.assertRaises(ValueError):
            allocate("10.0.0.0/24", [("LAN", 10), ("LAN", 3)])

    def test_reject_zero_hosts_and_ipv6(self):
        with self.assertRaises(ValueError):
            allocate("10.0.0.0/24", [("LAN", 0)])
        with self.assertRaises(ValueError):
            allocate("2001:db8::/64", [("LAN", 4)])

    def test_point_to_point_uses_four_address_block(self):
        self.assertEqual(allocate("192.0.2.0/30", [("p2p", 2)])[0]["subnet"],"192.0.2.0/30")


if __name__ == "__main__":
    unittest.main()
