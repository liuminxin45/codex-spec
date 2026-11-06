# Codex Spec

Lightweight engineering guidance for complex software changes with Codex.

Four habits: define what success looks like, understand the relevant system, observe actual behavior, and revise hypotheses after failure. One Skill and seven on-demand guides support product reasoning, UI consistency, system modeling, incremental delivery, diagnosis, verification and project knowledge.

## Install

Python 3.11+ and Git are required for the source installation. A dedicated Python environment is recommended.

```sh
python -m pip install "codex-spec @ git+https://github.com/liuminxin45/codex-spec.git@v0.1.1"
codex-spec init --project-dir /path/to/project
```

Alternatively install the wheel from [Releases](https://github.com/liuminxin45/codex-spec/releases/latest). This project is not published to PyPI. Start a new Codex conversation in the initialized project and invoke `$codex-spec`.

```sh
codex-spec spec create checkout --title "Reliable checkout" --goal "Keep totals correct across retries"
codex-spec context --select guide/system --detail full --spec checkout
codex-spec spec commit-reference checkout
```

Initialization adds the project-local `.agents/skills/codex-spec/` Skill, a short managed entry in `AGENTS.md`, and `.codex-spec/config.json`. It preserves user content. `init --replace` explicitly refreshes managed assets, not Specs or project knowledge.

Independent Specs live in `specs/<id>/spec.md`. Multiple conversations can work in the current checkout. There is no branch policy, dirty-tree gate, singleton task, ownership registry, session lock or concurrency protection. Commit bodies reference `Spec:` and `Spec-Docs:`. Small fixes may update an existing Spec without creating another document.

The CLI only manages files and reads context. Native file, terminal and browser tools remain available. Guidance depth follows risk, with no mandatory phase sequence, test expansion, agent orchestration or human approval ceremony. Real human feedback must never be inferred from automated checks.

See the [Chinese documentation](README.md), [CLI reference](docs/cli.md), [knowledge format](docs/knowledge.md), [evaluation protocol](docs/behavior-evaluation.md) and [release notes](docs/releases/0.1.1.md).

Version 0.1.0 replaces the former Spec Kit interface without compatibility aliases. Existing installations require deliberate removal of old project entries; the installer does not delete old or global user files. Prior history and original MIT copyright are retained in [LICENSE](LICENSE).
