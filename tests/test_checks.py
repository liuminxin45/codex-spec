from pathlib import Path
import tempfile
import unittest

from codex_spec.checks import check
from codex_spec.project import initialize


class CheckTests(unittest.TestCase):
    def test_installed_drift_is_reported_without_repair(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            initialize(root)
            self.assertEqual(check(root, "installed")["status"], "ok")
            target = root / ".agents/skills/codex-spec/guides/ui.md"
            target.write_text("custom", encoding="utf-8")
            result = check(root, "installed")
            self.assertEqual(result["status"], "error")
            self.assertEqual(target.read_text(encoding="utf-8"), "custom")

    def test_source_contract(self):
        root = Path(__file__).resolve().parents[1]
        result = check(root, "source", root)
        self.assertEqual(result["problems"], [])
