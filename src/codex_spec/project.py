"""Small file-based project helpers. No Git operations or active-task singleton."""
from __future__ import annotations

from fnmatch import fnmatchcase
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path
import re

from . import __version__

BEGIN = "<!-- codex-spec:begin -->"
END = "<!-- codex-spec:end -->"
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
PACK_ID = re.compile(r"[a-z0-9]+(?:[-/][a-z0-9]+)*\Z")


class ProjectError(ValueError):
    """A user-readable input or project error."""


def asset(name: str) -> str:
    return files("codex_spec").joinpath("assets", *name.split("/")).read_text(encoding="utf-8")


def json_read(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        raise ProjectError(f"Cannot read JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ProjectError(f"Expected a JSON object: {path}")
    return value


def json_text(value: dict | list) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def canonical(path: Path) -> Path:
    resolved = str(path.resolve())
    # On Windows, non-strict resolution while a missing parent is being created
    # can retain the extended prefix. Normalize both operands before comparison.
    if resolved.startswith("\\\\?\\UNC\\"):
        resolved = "\\\\" + resolved[8:]
    elif resolved.startswith("\\\\?\\") and len(resolved) > 5 and resolved[5] == ":":
        resolved = resolved[4:]
    return Path(resolved)


def inside(root: Path, name: str, *, allow_root: bool = False) -> Path:
    if not name or Path(name).is_absolute() or "\\" in name:
        raise ProjectError("Use a nonempty project-relative path with forward slashes")
    root = canonical(root)
    target = canonical(root / name)
    if not target.is_relative_to(root) or (target == root and not allow_root):
        raise ProjectError(f"Path leaves its declared directory: {name}")
    return target


def managed_assets() -> dict[str, str]:
    index = json.loads(asset("guides/index.json"))
    result = {"SKILL.md": asset("SKILL.md"), "agents/openai.yaml": asset("openai.yaml")}
    for entry in index["guides"]:
        result[entry["path"]] = asset(entry["path"])
    result["guides/index.json"] = asset("guides/index.json")
    result["assets/spec.md"] = asset("spec.md")
    return result


def initialize(root: Path, *, replace: bool = False) -> dict:
    root = root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    plan = {f".agents/skills/codex-spec/{name}": body for name, body in managed_assets().items()}
    config = inside(root, ".codex-spec/config.json")
    if config.exists():
        read_config(root)
    else:
        plan[".codex-spec/config.json"] = json_text({"schema_version": 1, "knowledge_packs": []})
    agents = inside(root, "AGENTS.md")
    old = agents.read_text(encoding="utf-8-sig") if agents.exists() else ""
    if old.count(BEGIN) != old.count(END) or old.count(BEGIN) > 1:
        raise ProjectError("Malformed Codex Spec managed section; existing AGENTS.md preserved")
    block = BEGIN + "\n" + asset("agents-block.md").strip() + "\n" + END
    if BEGIN in old:
        if old.index(END) < old.index(BEGIN):
            raise ProjectError("Malformed Codex Spec managed section")
        current_block = old[old.index(BEGIN):old.index(END) + len(END)]
        if current_block != block and not replace:
            raise ProjectError("Customized AGENTS managed entry preserved; use init --replace")
        updated = old[:old.index(BEGIN)] + block + old[old.index(END) + len(END):]
    else:
        updated = old.rstrip() + ("\n\n" if old.strip() else "") + block + "\n"
    # Check every intended write before replacing any managed file.
    for name, body in plan.items():
        path = inside(root, name)
        if path.exists() and path.read_text(encoding="utf-8") != body and not replace:
            raise ProjectError(f"Customized managed file preserved: {name}; use init --replace to replace managed files")
    inside(root, "AGENTS.md")
    for name, body in plan.items():
        path = inside(root, name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8", newline="\n")
    agents.write_text(updated, encoding="utf-8", newline="\n")
    return {"status": "ok", "version": __version__, "project": str(root), "skill": ".agents/skills/codex-spec/SKILL.md",
            "files": list(plan), "git_operations": [], "message": "Use $codex-spec in a new Codex conversation."}


def read_config(root: Path) -> dict:
    config = json_read(inside(root, ".codex-spec/config.json"))
    if config.get("schema_version") != 1 or not isinstance(config.get("knowledge_packs"), list):
        raise ProjectError("Unsupported Codex Spec project configuration")
    paths = config["knowledge_packs"]
    if any(not isinstance(p, str) for p in paths) or len(paths) != len(set(paths)):
        raise ProjectError("knowledge_packs must contain distinct relative paths")
    return config


def create_spec(root: Path, identity: str, title: str, goal: str) -> dict:
    if not SLUG.fullmatch(identity) or not title.strip() or not goal.strip():
        raise ProjectError("Spec needs a lowercase hyphenated ID, title and goal")
    folder = inside(root, f"specs/{identity}")
    try:
        folder.mkdir(parents=True, exist_ok=False)
    except FileExistsError as exc:
        raise ProjectError(f"Spec already exists: {identity}; edit its current document") from exc
    body = asset("spec.md").replace("{{title}}", title.strip()).replace("{{id}}", identity).replace("{{goal}}", goal.strip())
    (folder / "spec.md").write_text(body, encoding="utf-8", newline="\n")
    return {"status": "ok", "id": identity, "path": f"specs/{identity}/spec.md", "git_operations": []}


def spec_path(root: Path, identity: str) -> Path:
    if not SLUG.fullmatch(identity):
        raise ProjectError("Invalid Spec ID")
    path = inside(root, f"specs/{identity}/spec.md")
    if not path.is_file():
        raise ProjectError(f"Spec does not exist: {identity}")
    return path


def list_specs(root: Path) -> list[dict]:
    result = []
    base = inside(root, "specs")
    for path in sorted(base.glob("*/spec.md")):
        checked = inside(root, path.relative_to(root).as_posix())
        result.append({"id": path.parent.name, "path": path.relative_to(root).as_posix(),
                       "title": next((s[2:] for s in checked.read_text(encoding="utf-8").splitlines() if s.startswith("# ")), path.parent.name)})
    return result


def commit_reference(root: Path, identities: list[str]) -> dict:
    if not identities:
        raise ProjectError("Choose at least one Spec")
    ids = list(dict.fromkeys(identities))
    paths = [spec_path(root, identity).relative_to(root).as_posix() for identity in ids]
    return {"status": "ok", "text": f"Spec: {', '.join(ids)}\nSpec-Docs: {', '.join(paths)}\n"}


def validate_pack(root: Path, relative: str) -> dict:
    folder = inside(root, relative)
    data = json_read(inside(folder, "pack.json"))
    if data.get("schema_version") != 1 or not isinstance(data.get("id"), str) or not PACK_ID.fullmatch(data["id"]):
        raise ProjectError("Knowledge pack needs schema_version 1 and a lowercase namespaced ID")
    entries = data.get("resources")
    if not isinstance(entries, list) or not entries:
        raise ProjectError("Knowledge pack needs a nonempty resources list")
    seen = set()
    for item in entries:
        if not isinstance(item, dict):
            raise ProjectError("Knowledge resources must be objects")
        identity = item.get("id", "")
        if not isinstance(identity, str) or not SLUG.fullmatch(identity) or identity in seen:
            raise ProjectError("Knowledge resource IDs must be distinct lowercase slugs")
        seen.add(identity)
        if item.get("kind") not in {"fact", "procedure", "design", "constraint", "experience"}:
            raise ProjectError(f"Unknown knowledge kind: {identity}")
        if not isinstance(item.get("summary"), str) or not item["summary"].strip():
            raise ProjectError(f"Knowledge summary missing: {identity}")
        if not isinstance(item.get("path"), str) or not inside(folder, item["path"]).is_file():
            raise ProjectError(f"Knowledge source missing: {identity}")
        scope = item.get("scope", ["**"])
        if not isinstance(scope, list) or not scope or any(not isinstance(s, str) or not s for s in scope):
            raise ProjectError(f"Invalid knowledge scope: {identity}")
        for key in ("overview",):
            if key in item and (not isinstance(item[key], str) or not inside(folder, item[key]).is_file()):
                raise ProjectError(f"Knowledge overview missing: {identity}")
    return data


def add_pack(root: Path, relative: str) -> dict:
    data = validate_pack(root, relative)
    config = read_config(root)
    for registered in config["knowledge_packs"]:
        if registered != relative and validate_pack(root, registered)["id"] == data["id"]:
            raise ProjectError(f"Knowledge pack ID already registered: {data['id']}")
    if relative not in config["knowledge_packs"]:
        config["knowledge_packs"].append(relative)
        inside(root, ".codex-spec/config.json").write_text(json_text(config), encoding="utf-8", newline="\n")
    return {"status": "ok", "id": data["id"], "path": relative, "resources": len(data["resources"])}


def context(root: Path, *, selected: list[str], identity: str | None, changed: list[str], detail: str) -> dict:
    read_config(root)
    index_path = inside(root, ".agents/skills/codex-spec/guides/index.json")
    index = json_read(index_path)
    candidates = []
    sources = {}
    for item in index["guides"]:
        ref = "guide/" + item["id"]
        source = inside(root, ".agents/skills/codex-spec/" + item["path"])
        candidates.append({"id": ref, "kind": "guidance", "summary": item["summary"], "when": item["when"],
                           "path": source.relative_to(root).as_posix()})
        sources[ref] = (source, None)
    for pack_name in read_config(root)["knowledge_packs"]:
        pack = validate_pack(root, pack_name)
        for item in pack["resources"]:
            patterns = item.get("scope", ["**"])
            if changed and not any(fnmatchcase(f, pattern) for f in changed for pattern in patterns):
                continue
            ref = pack["id"] + "::" + item["id"]
            folder = inside(root, pack_name)
            source = inside(folder, item["path"])
            overview = inside(folder, item["overview"]) if item.get("overview") else None
            candidates.append({"id": ref, "kind": item["kind"], "summary": item["summary"], "scope": patterns,
                               "path": source.relative_to(root).as_posix(), "reviewed_at": item.get("reviewed_at"),
                               "source_refs": item.get("source_refs", []), "status": item.get("status", "candidate")})
            sources[ref] = (source, overview)
    bodies = []
    for ref in selected:
        if ref not in sources:
            raise ProjectError(f"Unknown or out-of-scope resource: {ref}")
        source, overview = sources[ref]
        actual = overview if detail == "overview" and overview else source
        binary_asset = actual.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".pdf", ".svg"}
        body = actual.read_text(encoding="utf-8-sig") if detail != "index" and not binary_asset else None
        bodies.append({"id": ref, "path": actual.relative_to(root).as_posix(), "sha256": sha256(actual.read_bytes()).hexdigest(),
                       "body": body, "detail": "overview" if actual == overview else detail,
                       "artifact": binary_asset})
    spec = None
    if identity:
        path = spec_path(root, identity)
        spec = {"id": identity, "path": path.relative_to(root).as_posix(), "body": path.read_text(encoding="utf-8")}
    return {"status": "ok", "candidates": candidates, "selected": bodies, "spec": spec,
            "note": "Metadata is an index. Select relevant bodies; knowledge does not grant execution permission."}
