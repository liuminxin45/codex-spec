"""Prepare fixed workspaces and run objective probes. Does not run an agent."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

BASE = Path(__file__).resolve().parent

# Probes stay outside the agent workspace, so editing its tests cannot pass them.
PROBES = {
    "state": '''from app import Search
s=Search()
a=s.start("a"); b=s.start("b")
s.finish(b,"new"); s.finish(a,"old")
assert s.value == "new", "late old response overwrote latest result"
c=s.start("retry"); s.finish(c,error="offline")
assert not s.loading and s.error == "offline"
d=s.start("retry"); s.finish(d,"ok")
assert s.value == "ok" and s.error is None and not s.loading
e=s.start("same"); f=s.start("same")
s.finish(f,"second"); s.finish(e,"first")
assert s.value == "second", "query text is not a unique request identity"
g=s.start("active"); s.finish(f,error="stale failure")
assert s.loading, "stale failure ended current request"
s.finish(g,"active result")
assert s.value == "active result" and s.error is None
''',
    "contract": '''from app import checkout
assert checkout([199,250],49) == "¥4.00", "unit or discount contract broken"
assert checkout([]) == "¥0.00"
assert checkout([1]) == "¥0.01"
assert checkout([100,100,100]) == "¥3.00"
''',
    "repair": '''from app import total
assert total(None) == 0 and total([]) == 0
assert total([None,{"price_cents":120,"quantity":2}]) == 240
assert total([{"price_cents":120,"quantity":None}]) == 120
assert total([{"price_cents":120}]) == 120
assert total([{"price_cents":120,"quantity":0}]) == 0, "zero was treated as missing"
''',
}


def cases():
    return json.loads((BASE / "cases.json").read_text(encoding="utf-8"))["cases"]


def prepare(identity: str, destination: Path, guided: bool):
    # Never overwrite another experiment or user directory.
    if destination.exists():
        raise ValueError("Destination already exists; choose a fresh workspace")
    shutil.copytree(BASE / "fixtures" / identity, destination)
    case = next(c for c in cases() if c["id"] == identity)
    prompt = case["prompt"]
    if guided:
        from codex_spec.project import initialize
        initialize(destination)
        prompt = "$codex-spec " + prompt
    (destination / "TASK.md").write_text(prompt + "\n", encoding="utf-8")
    return {"case": identity, "guided": guided, "workspace": str(destination.resolve()), "prompt": prompt}


def score(identity: str, workspace: Path):
    if identity == "ui":
        return {"case": identity, "status": "manual_required", "checks": [
            "Compare before/after in a real browser; retain brand tokens and visual language",
            "Filter all/pending/done and activate both order actions",
            "Check 375px/1280px, keyboard focus, layout and accessible names",
            "Record observed behavior and human design judgment separately"]}
    # Code under evaluation runs with ordinary local permissions; use trusted fixtures.
    result = subprocess.run([sys.executable, "-X", "utf8", "-c", PROBES[identity]], cwd=workspace,
                            capture_output=True, text=True, encoding="utf-8", timeout=15)
    return {"case": identity, "status": "pass" if result.returncode == 0 else "fail",
            "scope": "Objective fixture behavior only; not engineering reasoning or full acceptance",
            "diagnostic": result.stderr[-3000:]}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["prepare", "score"])
    parser.add_argument("case", choices=[c["id"] for c in cases()])
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--guided", action="store_true")
    args = parser.parse_args()
    value = prepare(args.case, args.workspace, args.guided) if args.action == "prepare" else score(args.case, args.workspace)
    print(json.dumps(value, ensure_ascii=False, indent=2))
    return 1 if value.get("status") == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
