"""Exercise the built wheel and an sdist rebuild, outside the source checkout."""
from pathlib import Path
import os
import subprocess
import sys
import tempfile
import venv


def run(*args, cwd=None, env=None):
    return subprocess.run(args, cwd=cwd, env=env, check=True, capture_output=True, text=True, encoding="utf-8").stdout


def main():
    root = Path(__file__).resolve().parents[1]
    wheels = list((root / "dist").glob("codex_spec-*.whl"))
    sdists = list((root / "dist").glob("codex_spec-*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        raise SystemExit("Expected exactly one new wheel and sdist in dist")
    # build checks the sdist by default before building the wheel.
    with tempfile.TemporaryDirectory(prefix="codex-spec-smoke-") as temp:
        base = Path(temp)
        venv.create(base / "env", with_pip=True)
        python = base / "env" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        env = dict(os.environ, PYTHONUTF8="1")
        env.pop("PYTHONPATH", None)
        run(str(python), "-m", "pip", "install", "--no-deps", str(wheels[0]), cwd=base, env=env)
        target = base / "项目 with spaces"
        target.mkdir()
        run(str(python), "-m", "codex_spec", "init", "--project-dir", str(target), "--json", cwd=base, env=env)
        run(str(python), "-m", "codex_spec", "check", "--project-dir", str(target), "--json", cwd=base, env=env)
        run(str(python), "-m", "codex_spec", "spec", "create", "smoke", "--title", "真实安装", "--goal", "验证离线可用", "--project-dir", str(target), "--json", cwd=base, env=env)
        run(str(python), "-m", "codex_spec", "context", "--select", "guide/ui", "--spec", "smoke", "--project-dir", str(target), "--json", cwd=base, env=env)
        exe = python.parent / ("codex-spec.exe" if os.name == "nt" else "codex-spec")
        assert run(str(exe), "--version", cwd=base, env=env).strip() == "0.1.0"
        print("PASS: isolated wheel install, console entry, Chinese path, Skill, Spec and selected guide")


if __name__ == "__main__":
    main()
