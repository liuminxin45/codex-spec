"""Portable CLI; never commits, switches branches, runs agents or gates coding."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from . import __version__
from .project import (ProjectError, add_pack, commit_reference, context, create_spec, initialize,
                      json_text, list_specs, spec_path, validate_pack)


def parser() -> argparse.ArgumentParser:
    top = argparse.ArgumentParser(prog="codex-spec", description="Lightweight engineering guidance for Codex")
    top.add_argument("--version", action="version", version=__version__)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--project-dir", type=Path, default=Path.cwd())
    common.add_argument("--json", action="store_true")
    commands = top.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", parents=[common], help="Install the Skill and a short AGENTS entry")
    init.add_argument("--replace", action="store_true", help="Replace managed Skill files; preserve project knowledge and specs")
    specs = commands.add_parser("spec", help="Independent, human-readable Specs")
    sub = specs.add_subparsers(dest="action", required=True)
    new = sub.add_parser("create", parents=[common])
    new.add_argument("id")
    new.add_argument("--title", required=True)
    new.add_argument("--goal", required=True)
    sub.add_parser("list", parents=[common])
    show = sub.add_parser("show", parents=[common])
    show.add_argument("id")
    commit = sub.add_parser("commit-reference", parents=[common])
    commit.add_argument("ids", nargs="+")
    ctx = commands.add_parser("context", parents=[common], help="List metadata or read explicitly selected context")
    ctx.add_argument("--select", action="append", default=[])
    ctx.add_argument("--spec")
    ctx.add_argument("--file", action="append", default=[])
    ctx.add_argument("--detail", choices=["index", "overview", "full"], default="full")
    knowledge = commands.add_parser("knowledge", help="Local, user-maintained knowledge packs")
    sub = knowledge.add_subparsers(dest="action", required=True)
    for verb in ("add", "validate"):
        action = sub.add_parser(verb, parents=[common])
        action.add_argument("path", help="Project-relative pack directory")
    check = commands.add_parser("check", parents=[common], help="Optional read-only diagnostics")
    check.add_argument("--kind", choices=["installed", "source", "generated-context", "knowledge-index", "context-budget"], default="installed")
    check.add_argument("--repo-root", type=Path)
    return top


def dispatch(args: argparse.Namespace) -> dict:
    root = args.project_dir.resolve()
    if args.command == "init":
        return initialize(root, replace=args.replace)
    if args.command == "spec":
        if args.action == "create":
            return create_spec(root, args.id, args.title, args.goal)
        if args.action == "list":
            return {"status": "ok", "specs": list_specs(root)}
        if args.action == "show":
            path = spec_path(root, args.id)
            return {"status": "ok", "path": path.relative_to(root).as_posix(), "text": path.read_text(encoding="utf-8")}
        return commit_reference(root, args.ids)
    if args.command == "context":
        return context(root, selected=args.select, identity=args.spec, changed=args.file, detail=args.detail)
    if args.command == "knowledge":
        if args.action == "add":
            return add_pack(root, args.path)
        data = validate_pack(root, args.path)
        return {"status": "ok", "id": data["id"], "resources": len(data["resources"])}
    from .checks import check
    return check(root, args.kind, args.repo_root)


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        result = dispatch(args)
    except (ProjectError, OSError, UnicodeError, KeyError, TypeError, ValueError) as exc:
        result = {"status": "error", "message": str(exc)}
    if args.json:
        print(json_text(result), end="")
    elif "text" in result:
        print(result["text"], end="" if result["text"].endswith("\n") else "\n")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "ok" else 1
