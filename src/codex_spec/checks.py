"""Optional read-only diagnostics. These are not development-stage gates."""
from __future__ import annotations

import json
from pathlib import Path
import re
import tomllib

from . import __version__
from .project import BEGIN, END, ProjectError, asset, inside, json_read, managed_assets, read_config, validate_pack


def check(project: Path, kind: str, repo_root: Path | None = None) -> dict:
    root = (repo_root or project).resolve()
    problems = []
    facts = {}
    if kind == "installed":
        read_config(project)
        for name, expected in managed_assets().items():
            path = inside(project, ".agents/skills/codex-spec/" + name)
            if not path.is_file() or path.read_text(encoding="utf-8") != expected:
                problems.append(f"Missing or customized managed asset: {name}")
        agents = project / "AGENTS.md"
        text = agents.read_text(encoding="utf-8") if agents.exists() else ""
        expected = BEGIN + "\n" + asset("agents-block.md").strip() + "\n" + END
        if expected not in text or text.count(BEGIN) != 1 or text.count(END) != 1:
            problems.append("AGENTS.md has a missing or outdated managed entry")
        for relative in read_config(project)["knowledge_packs"]:
            validate_pack(project, relative)
        facts["version"] = __version__
    elif kind == "knowledge-index":
        index = json.loads(asset("guides/index.json"))
        ids = [g["id"] for g in index["guides"]]
        if len(ids) != len(set(ids)):
            problems.append("Duplicate guidance ID")
        for entry in index["guides"]:
            if not entry.get("summary") or not entry.get("when") or not asset(entry["path"]).strip():
                problems.append("Guidance lacks metadata or content: " + entry["id"])
        config = project / ".codex-spec/config.json"
        if config.exists():
            for relative in read_config(project)["knowledge_packs"]:
                validate_pack(project, relative)
        facts["guides"] = ids
    elif kind == "context-budget":
        # Character limits also work for Chinese; line count alone does not.
        limits = {"SKILL.md": 6500, "agents-block.md": 800, "guides/index.json": 2800}
        limits.update({g["path"]: 5000 for g in json.loads(asset("guides/index.json"))["guides"]})
        facts["characters"] = {}
        for name, limit in limits.items():
            count = len(asset(name))
            facts["characters"][name] = {"actual": count, "limit": limit}
            if count > limit:
                problems.append(f"Context exceeds budget: {name}: {count} > {limit}")
    elif kind == "generated-context":
        bodies = managed_assets()
        for name, body in bodies.items():
            if not name.endswith(".md"):
                continue
            for link in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", body):
                if "://" in link or link.startswith("#"):
                    continue
                target = (Path(name).parent / link.split("#")[0]).as_posix()
                if target not in bodies:
                    problems.append(f"Broken guidance link: {name} -> {link}")
        if (project / ".codex-spec/config.json").exists():
            result = check(project, "installed")
            problems.extend(result["problems"])
        facts["managed_files"] = len(bodies)
    elif kind == "source":
        data = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
        if data["project"]["name"] != "codex-spec" or data["project"]["version"] != __version__:
            problems.append("Package identity/version differs from executable")
        if data["project"].get("dependencies"):
            problems.append("The lightweight runtime must have no external dependencies")
        for sub in ("generated-context", "knowledge-index", "context-budget"):
            result = check(root, sub)
            problems.extend(result["problems"])
        for directory in ("src/codex_spec/assets/packs", "knowledge-packs"):
            if (root / directory).exists():
                problems.append("Bundled project knowledge is not a source default: " + directory)
        for path in (root / "docs").rglob("*.md"):
            for link in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", path.read_text(encoding="utf-8")):
                if "://" in link or link.startswith("#") or "{" in link:
                    continue
                if not (path.parent / link.split("#")[0]).is_file():
                    problems.append(f"Broken documentation link: {path.relative_to(root)} -> {link}")
        facts["version"] = __version__
    else:
        raise ProjectError("Unknown check kind")
    return {"status": "ok" if not problems else "error", "kind": kind, "facts": facts, "problems": problems,
            "scope": "Read-only structural diagnostics, not product or AI behavior acceptance"}
