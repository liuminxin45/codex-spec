import concurrent.futures
import contextlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from codex_spec.checks import check
from codex_spec.cli import main
from codex_spec.project import (BEGIN, END, ProjectError, add_pack, commit_reference, context,
                                create_spec, initialize, list_specs, validate_pack)


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def init(self):
        return initialize(self.root)

    def pack(self):
        folder = self.root / "knowledge/project"
        folder.mkdir(parents=True)
        (folder / "map.md").write_text("Source: src/state.py\nState belongs to SearchStore.", encoding="utf-8")
        (folder / "overview.md").write_text("State ownership overview", encoding="utf-8")
        value = {"schema_version": 1, "id": "team/project", "resources": [
            {"id": "map", "kind": "fact", "summary": "State map", "path": "map.md", "overview": "overview.md", "scope": ["src/*"]}]}
        (folder / "pack.json").write_text(json.dumps(value), encoding="utf-8")
        return folder, value

    def test_install_preserves_user_agents_and_is_idempotent(self):
        (self.root / "AGENTS.md").write_text("# My project\nKeep my policy.\n", encoding="utf-8")
        self.init()
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.init()
        self.assertEqual(before, {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
        self.assertTrue((self.root / "AGENTS.md").read_text().startswith("# My project\nKeep my policy."))
        self.assertEqual(check(self.root, "installed")["status"], "ok")

    def test_customized_asset_rejected_before_any_other_write(self):
        self.init()
        guide = self.root / ".agents/skills/codex-spec/guides/ui.md"
        guide.write_text("my customization", encoding="utf-8")
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        with self.assertRaises(ProjectError):
            self.init()
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
        initialize(self.root, replace=True)
        self.assertNotEqual(guide.read_text(), "my customization")

    def test_replace_preserves_specs_and_knowledge_registration(self):
        self.init()
        self.pack()
        add_pack(self.root, "knowledge/project")
        create_spec(self.root, "search", "Search", "Preserve current results")
        spec = self.root / "specs/search/spec.md"
        spec.write_text("user edited", encoding="utf-8")
        initialize(self.root, replace=True)
        self.assertEqual(spec.read_text(), "user edited")
        self.assertEqual(len(context(self.root, selected=[], identity=None, changed=[], detail="index")["candidates"]), 8)

    def test_malformed_agents_preserved(self):
        (self.root / "AGENTS.md").write_text(BEGIN, encoding="utf-8")
        with self.assertRaises(ProjectError):
            self.init()
        self.assertFalse((self.root / ".agents").exists())

    def test_customized_managed_entry_requires_replace(self):
        self.init()
        path = self.root / "AGENTS.md"
        path.write_text(path.read_text().replace("## Codex Spec", "## My custom entry"), encoding="utf-8")
        with self.assertRaises(ProjectError):
            self.init()
        self.assertIn("My custom entry", path.read_text())

    def test_dirty_nondefault_checkout_and_multiple_specs(self):
        subprocess.run(["git", "init", "-b", "feature"], cwd=self.root, check=True, capture_output=True)
        (self.root / "product.txt").write_text("uncommitted work")
        self.init()
        before = subprocess.check_output(["git", "symbolic-ref", "HEAD"], cwd=self.root)
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(lambda n: create_spec(self.root, f"feature-{n}", f"Feature {n}", "A user outcome"), range(4)))
        self.assertEqual(len(list_specs(self.root)), 4)
        self.assertEqual(before, subprocess.check_output(["git", "symbolic-ref", "HEAD"], cwd=self.root))
        self.assertEqual((self.root / "product.txt").read_text(), "uncommitted work")
        self.assertFalse((self.root / ".codex-spec/feature.json").exists())
        self.assertFalse(list(self.root.rglob("*.lock")))

    def test_duplicate_spec_preserves_document(self):
        create_spec(self.root, "search", "Search", "Current request wins")
        path = self.root / "specs/search/spec.md"
        path.write_text("current human edit")
        with self.assertRaises(ProjectError):
            create_spec(self.root, "search", "Other", "Other")
        self.assertEqual(path.read_text(), "current human edit")

    def test_invalid_id_and_traversal(self):
        for identity in ("../escape", "UPPER", "a/b", "", "a\\b"):
            with self.subTest(identity=identity), self.assertRaises(ProjectError):
                create_spec(self.root, identity, "Title", "Goal")

    def test_commit_references_real_documents(self):
        create_spec(self.root, "one", "One", "Goal")
        create_spec(self.root, "two", "Two", "Goal")
        self.assertEqual(commit_reference(self.root, ["one", "two", "one"])["text"],
                         "Spec: one, two\nSpec-Docs: specs/one/spec.md, specs/two/spec.md\n")
        with self.assertRaises(ProjectError):
            commit_reference(self.root, ["missing"])

    def test_context_lists_metadata_without_bodies(self):
        self.init()
        result = context(self.root, selected=[], identity=None, changed=[], detail="full")
        self.assertEqual(result["selected"], [])
        self.assertTrue(all("body" not in item for item in result["candidates"]))
        selected = context(self.root, selected=["guide/ui"], identity=None, changed=[], detail="full")
        self.assertEqual(len(selected["selected"]), 1)
        self.assertIn("Design inheritance", selected["selected"][0]["body"])

    def test_pack_scope_overview_and_current_source(self):
        self.init()
        folder, value = self.pack()
        add_pack(self.root, "knowledge/project")
        result = context(self.root, selected=["team/project::map"], identity=None, changed=["src/state.py"], detail="overview")
        self.assertEqual(result["selected"][0]["body"], "State ownership overview")
        with self.assertRaises(ProjectError):
            context(self.root, selected=["team/project::map"], identity=None, changed=["docs/readme.md"], detail="full")
        (folder / "map.md").write_text("new verified fact")
        result = context(self.root, selected=["team/project::map"], identity=None, changed=[], detail="full")
        self.assertEqual(result["selected"][0]["body"], "new verified fact")

    def test_invalid_pack_does_not_change_config(self):
        self.init()
        folder, value = self.pack()
        path = self.root / ".codex-spec/config.json"
        before = path.read_bytes()
        value["resources"][0]["path"] = "../../../private.txt"
        (folder / "pack.json").write_text(json.dumps(value))
        with self.assertRaises(ProjectError):
            add_pack(self.root, "knowledge/project")
        self.assertEqual(before, path.read_bytes())

    def test_binary_design_asset_is_referenced_not_decoded(self):
        self.init()
        folder, value = self.pack()
        (folder / "design.png").write_bytes(b"\x89PNG\r\n\x1a\n")
        value["resources"][0].update(path="design.png", kind="design")
        (folder / "pack.json").write_text(json.dumps(value))
        add_pack(self.root, "knowledge/project")
        item = context(self.root, selected=["team/project::map"], identity=None, changed=[], detail="full")["selected"][0]
        self.assertTrue(item["artifact"])
        self.assertIsNone(item["body"])

    def test_path_symlink_escape(self):
        outside = tempfile.TemporaryDirectory()
        self.addCleanup(outside.cleanup)
        try:
            (self.root / ".agents").symlink_to(outside.name, target_is_directory=True)
        except OSError:
            self.skipTest("OS does not permit creating a test symlink")
        with self.assertRaises(ProjectError):
            self.init()
        self.assertEqual(list(Path(outside.name).iterdir()), [])

    @unittest.skipUnless(__import__("os").name == "nt", "Windows extended path syntax")
    def test_extended_path_prefix_during_parent_creation(self):
        from unittest.mock import patch
        from codex_spec.project import inside
        root = self.root.resolve()
        target = Path("\\\\?\\" + str(root / "specs/feature"))
        with patch.object(Path, "resolve", side_effect=[root, target]):
            self.assertEqual(inside(root, "specs/feature"), root / "specs/feature")

    def test_cli_errors_are_machine_readable(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["context", "--project-dir", str(self.root), "--json"])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(output.getvalue())["status"], "error")


if __name__ == "__main__":
    unittest.main()
