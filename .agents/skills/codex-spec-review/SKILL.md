---
name: codex-spec-review
description: "Review Codex Spec after a completed development increment or revisit a proposed Codex Spec PR. Use when explicitly invoked to assess evidence, separate guidance problems from execution or project constraints, and prepare justified changes or PR dispositions. Not a general business-code review."
---

# Codex Spec Review

Judge whether Codex Spec needs a useful correction based on actual development.
An evidence-supported "no material issue; no change" is a complete result.
This is an explicitly invoked maintenance skill, not a gate on normal coding.

## Establish the review target

Identify the development increment, its intended outcome and preserved behavior,
the Codex Spec version actually used, and any PR under review. Use the current
conversation, relevant Spec, commits and selected original observations; expand
reading only to resolve a consequential uncertainty. If the loaded guidance
version cannot be established, state that limit rather than assigning blame.

Locate the Codex Spec source repository from the user's path or verified remote.
The business project's repository is evidence, not automatically the repository
to change or push. For an existing PR, inspect its current base/head, diff,
checks and subsequent use; do not rely on an old review summary.

Assess relevant outcomes: product acceptance, system understanding, real behavior,
diagnosis after failure, UI consistency, convergent slices, credible knowledge
and developer effort. These are lenses, not eight mandatory report sections.
Passing tests, commit trailers and elapsed time alone do not establish quality.

## Decide whether a correction is warranted

For a material concern connect the observation and its impact to the applicable
guidance or tool behavior. Distinguish:

- A missing, misleading or conflicting instruction, or a reproducible tool bug.
- Sound guidance that was not followed, or a check that did not test its claim.
- A project-specific rule, environment limitation or changed product requirement.
- A plausible concern without enough evidence to decide.

Look for evidence that weakens the proposed explanation. A normal repair, a
stylistic preference, an empty optional knowledge pack or one unknown is not by
itself a Codex Spec defect. An execution lapse may justify a clearer example if
it exposes a specific decision ambiguity; repeating existing advice is not a fix.
Do not infer improved success or reduced rework from one successful use.

Keep findings that affect outcomes, reliability, misleading acceptance or repeated
effort. Explain the likely benefit and cost of a proposed correction. Prefer a
small change at the relevant decision point over new universal rules, mandatory
artifacts, broad testing quotas, Harness controllers or concurrency gates.
If no worthwhile correction is supported, stop with that conclusion and any
material evidence limits. Do not create a PR merely to show activity.

## Validate and propose

Follow the invoking request and existing authorization. A request to run the
review-to-PR workflow includes preparing and pushing supported corrections;
an analysis-only request stops at findings. Do not request the same approval
again or treat this skill as authority for unrelated repository changes.

Use the actual Codex Spec repository's conventions and current checkout. Reuse
an existing relevant Spec and PR when suitable; keep unrelated proposals separate.
Preserve other work and review the exact commit scope. Do not require a new
branch, clean tree, session lock or fixed stage sequence as a condition to work.

Verify a correction before committing and pushing it. Reproduce tool bugs where
applicable; run relevant repository checks. For guidance, inspect realistic
decisions and counterexamples, not just whether new wording exists. Report
structural checks, qualitative trials and controlled model comparisons separately.
Use ordinary Git delivery and confirm the pushed SHA, then create or update the
authorized PR with the problem, evidence, change, validation and remaining limits.
Keep raw business data, private logs and screenshots out of a public proposal.

## Revisit an open proposal

The user may leave a PR open for several days or a week and invoke this skill
again. Observation time is context, not an automatic acceptance rule or a timer.
Do not schedule monitoring, enable auto-merge or merge merely because no issue
was reported. Merging or releasing requires the user's request for that action.

If later evidence exposes a problem, determine whether a small amendment retains
the proposal's value. Validate and push an authorized amendment, or close the
specific open PR when the user requested withdrawal or authorized that disposition
and its premise no longer holds. Without that authority, report the recommendation.
Closing an unmerged PR does not revert installed guidance or a merged commit;
handle those as separate requested changes. Do not force-push or delete history
just to withdraw a proposal.

Report the actual conclusion, decisive evidence and limits, what changed or why
no change was needed, and the exact PR state and next useful action. Distinguish
"no material issue found in this review" from proof that no defect exists.
