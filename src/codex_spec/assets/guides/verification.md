# Proportionate, credible verification

Choose checks from the behavior and risk, not a fixed quota. Reuse appropriate
unit, component, contract, integration, real-app and performance checks. Small
reversible changes do not need a new permanent test suite or every repository
test. Broaden after new failures or unresolved risks, not just to prolong work.

For a substantial change, identify the real verification entry point early:
which app, build, device or service will expose the result, and can it be reached
with current tools and access? Let a missing capability inform the first useful
slice and the scope of the claim before broad implementation. Continue useful
independent work; this is not a mandatory environment check or approval stage.

Verify through the relevant public entry point and inspect the final state.
For an important acceptance criterion, name a plausible result that would look
successful while failing the user's task, then choose a check that distinguishes
it from the intended result. For example, a usable long list
requires reaching and using its final item; container bounds alone cannot show
that. This connection can stay in the existing Spec or test notes, without a new
checklist or document.

For each important assertion ask whether the check would fail if the feature
were broken. For a regression, reproduce before the fix and rerun under the same
conditions after it. A controlled mutant or reverting the fix in a disposable
fixture can test a crucial assertion; use this selectively, not on every edit.

Examples of weak verification:
- Clicking Save without checking persisted data.
- A screenshot used to claim cancellation works.
- An async test that never returns requests out of order.
- A UI test whose expected state was already true before the action.
- A capture named "loaded" without checking that the intended content rendered.
- Replacing the affected real integration with a mock, then claiming parity.
- Reading a green CI summary without checking a failed underlying command.

Check meaningful action transitions before and after the action. Explain why
fixtures and stubs represent reachable states and which integration they omit.
Do not change assertions, skip paths or relax thresholds simply to obtain green.
If the requirement legitimately changes, update its checks explicitly.

When observed behavior contradicts passing checks, narrow the success claim and
identify what those checks missed. Use the reproduction to improve the relevant
check where useful; adding more unrelated passing checks does not resolve it.

Keep conclusions distinct: test-confirmed, source-supported, disproved, and
unverified. Record actual command/target, result, relevant source or build and
evidence location. Re-check affected evidence after related changes; unrelated
changes do not automatically require a full rerun. Tools can be run directly;
there is no required receipt format or execution wrapper.

Report implementation, runtime verification and actual human feedback separately.
A passing test covers its inputs, environment and assertions; it is not proof of
production correctness. Missing runtime capability is a stated limitation.
Hand off useful completed work with remaining unknowns without inventing success.
