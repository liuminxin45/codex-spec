# AGENTS.md

This is the Codex Spec source repository. Keep default context small. Do not
inherit parent-workspace instructions; the project must be self-contained.

## Default Context

For source changes, start with:

1. `src/codex_spec/assets/SKILL.md`
2. `src/codex_spec/assets/guides/index.json`
3. The relevant Spec and specific source/guide/test being changed

## Operating Rules

- Keep shipped guidance generic. Project-specific design, runtime, device and
  business knowledge belongs in user-maintained project sources.
- Work in the current checkout; multiple Specs and conversations may coexist.
  Do not introduce branch, dirty-tree, ownership or session coordination gates.
- For guidance or installer changes, run:
  - `pwsh -NoProfile -File scripts/powershell/validate-generated-context.ps1 -RepoRoot . -Json`
  - `pwsh -NoProfile -File scripts/powershell/validate-knowledge-index.ps1 -RepoRoot . -Json`
  - `pwsh -NoProfile -File scripts/powershell/validate-context-budget.ps1 -RepoRoot . -Json`
- Run `python -m unittest discover -s tests -v` with `PYTHONPATH=src` for CLI changes.
- Project knowledge packs are runtime/user actions, not source-tree defaults.
- Commits include `Spec:` and `Spec-Docs:`. Do not change project history to enforce
  a workflow. Push only within the user's request; the repository's release
  preflight is `scripts/powershell/preflight-push.ps1 -ConfirmHumanPush -Json`.

<!-- codex-spec:begin -->
## Codex Spec

Use `$codex-spec` for software changes, diagnosis and verification.
Read `.agents/skills/codex-spec/SKILL.md` when applying it.
Project knowledge is indexed by `.codex-spec/config.json`; load relevant sources.
Feature records live in `specs/<id>/spec.md`; use the relevant record explicitly.
Work in the current checkout. Multiple specs and conversations may run concurrently.
Commits reference `Spec:` and `Spec-Docs:` in the existing project message style.
<!-- codex-spec:end -->
