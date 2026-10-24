---
name: bugfix
description: Diagnose and fix a bounded software defect with a minimal, verified change, stopping only on hard-to-reverse decisions.
disable-model-invocation: true
---

# Bugfix

Fix the reported defect without expanding it into feature work or overwriting unrelated user changes.

## Establish the problem

- Read the relevant project instructions and inspect the affected code, tests, and recent local changes.
- Resolve issue URLs or report files only when supplied and accessible.
- Restate the observed/expected behavior when that clarification would affect the fix. Do not require a confirmation round for an adequately specified bug.
- If the report contains distinct defects, isolate them and address one at a time unless the user asks otherwise.
- Find the project's test command in its instructions, README, Makefile, or package manifest. Never chain fallback commands. A failing suite must report as failing.

## Reproduce and repair

- Write the reproduction as a card in the `blueprint` acceptance-criteria format: **Given** concrete state, **When** the triggering action, **Then** the one correct outcome, **Verify** the test that will prove it. Show the card in chat before writing the test.
- **RED**: add or adjust the smallest automated test that implements the card. Run it. It must fail on the real production code because of the defect, not an import, syntax, or setup error. Never patch out behavior to force the failure.
- **Can't reproduce? Stop.** Report what you tried and what evidence you have, and wait for the user. Do not fix what you have not reproduced.
- Apply the `decision-gate` skill. Most fixes are two-way doors. A fix that touches a schema, public contract, process model, or deploy unit stops for the user.
- **GREEN**: make the smallest production change consistent with established project patterns. Run the test. Do not touch the test in the same step. Do not refactor adjacent code or fix newly discovered issues without direction; list them in the report.
- **Prove it**: revert the fix, confirm the test fails again, restore.
- Use a worktree only when the repository provides or the user requests a suitable workflow. Never assume a path, helper script, database setup, or branch convention.

## Verify and report

- Re-run the focused test and proportionate nearby checks. Run broader checks when affordable and supported by the project; state any checks that could not run.
- Invoking this skill authorizes a local commit on a feature branch. Branch first if on the default branch, stage files explicitly, and match the repo's commit style. Merging and pushing are one-way doors.
- Report the root cause, changed files, and the card's verification in the `blueprint` format: status, evidence (test id, pass after the fix, commit), and whether it failed with the fix reverted. Then any remaining risk or follow-up.
