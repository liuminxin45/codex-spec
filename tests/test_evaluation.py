"""Test evaluation sensitivity, not simulated model improvement."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("evaluation", ROOT / "evals/evaluate.py")
evaluation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluation)

FIXES = {
    "state": '''class Search:
    def __init__(self):
        self.value=None; self.error=None; self.loading=False; self.generation=0
    def start(self, query):
        self.generation+=1; self.error=None; self.loading=True
        return self.generation
    def finish(self, token, value=None, error=None):
        if token != self.generation: return
        self.value=value; self.error=error; self.loading=False
''',
    "contract": '''from pricing import total_cents
def checkout(prices, discount_cents=0):
    return f"¥{(total_cents(prices)-discount_cents)/100:.2f}"
''',
    "repair": '''def total(rows):
    return sum(r["price_cents"] * (1 if r.get("quantity") is None else r["quantity"])
               for r in (rows or []) if r is not None)
''',
}


class EvaluationTests(unittest.TestCase):
    def test_all_defects_fail_and_effective_fixes_pass(self):
        for identity, fix in FIXES.items():
            with self.subTest(case=identity), tempfile.TemporaryDirectory() as temp:
                workspace = Path(temp) / "work"
                evaluation.prepare(identity, workspace, False)
                self.assertEqual(evaluation.score(identity, workspace)["status"], "fail")
                (workspace / "app.py").write_text(fix, encoding="utf-8")
                self.assertEqual(evaluation.score(identity, workspace)["status"], "pass")

    def test_prepare_preserves_existing_workspace(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                evaluation.prepare("state", Path(temp), True)

    def test_guided_prepare_and_ui_never_fakes_acceptance(self):
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp) / "work"
            evaluation.prepare("ui", workspace, True)
            self.assertTrue((workspace / ".agents/skills/codex-spec/SKILL.md").is_file())
            self.assertEqual(evaluation.score("ui", workspace)["status"], "manual_required")

    def test_plausible_but_wrong_null_fix_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp) / "work"
            evaluation.prepare("repair", workspace, False)
            (workspace / "app.py").write_text('def total(rows):\n return sum(r["price_cents"]*(r.get("quantity") or 1) for r in (rows or []) if r)\n', encoding="utf-8")
            self.assertEqual(evaluation.score("repair", workspace)["status"], "fail")
