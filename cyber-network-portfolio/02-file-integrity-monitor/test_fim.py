import json
from pathlib import Path
import tempfile
import unittest
from fim import snapshot, compare, hash_file


class FimTests(unittest.TestCase):
    def test_added_removed_modified_unchanged(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "keep.txt").write_text("hello")
            (root / "change.txt").write_text("before")
            (root / "gone.txt").write_text("old")
            baseline = {"files": snapshot(root)}
            (root / "change.txt").write_text("after")
            (root / "gone.txt").unlink()
            (root / "new.txt").write_text("new")
            report = compare(baseline, snapshot(root))
            self.assertEqual(report["added"], ["new.txt"])
            self.assertEqual(report["removed"], ["gone.txt"])
            self.assertEqual(report["modified"], ["change.txt"])
            self.assertEqual(report["unchanged"], 1)

    def test_sha256_matches_known_digest(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x"
            p.write_bytes(b"abc")
            self.assertEqual(hash_file(p),
                "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")

    def test_empty_tree(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(snapshot(d), {})


if __name__ == "__main__":
    unittest.main()
