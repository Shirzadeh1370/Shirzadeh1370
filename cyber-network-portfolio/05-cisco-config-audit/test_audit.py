from pathlib import Path
import unittest
from audit import review


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).parent / "samples"

    def test_insecure_fixture_flags_risks(self):
        result = review((self.root / "insecure_lab.cfg").read_text())
        rule_ids = [item["rule"] for item in result["findings"]]
        self.assertEqual(result["vty_blocks"], 2)
        self.assertIn("VTY_ALLOWS_TELNET", rule_ids)
        self.assertIn("SNMP_COMMUNITY_PRESENT", rule_ids)
        self.assertIn("ENABLE_PASSWORD_LEGACY", rule_ids)
        self.assertIn("VTY_AUTH_POLICY_REVIEW", rule_ids)
        self.assertGreaterEqual(result["finding_count"], 6)

    def test_hardened_fixture_has_no_flags(self):
        result = review((self.root / "hardened_lab.cfg").read_text())
        self.assertEqual(result["finding_count"], 0)

    def test_no_vty_is_reviewed(self):
        result = review("hostname lab\nip ssh version 2\n")
        self.assertIn("NO_VTY_BLOCK",
                      [f["rule"] for f in result["findings"]])

    def test_disabled_vty_not_flagged_for_missing_login(self):
        result = review("ip ssh version 2\nline vty 0 4\n transport input none\n!")
        self.assertNotIn("VTY_AUTH_POLICY_REVIEW",
                         [f["rule"] for f in result["findings"]])


if __name__ == "__main__":
    unittest.main()
