---
name: dev
description: Implement a scoped software change against an approved blueprint, using repository conventions and proportionate tests, stopping only on hard-to-reverse decisions.
disable-model-invocation: true
---

# Dev

Deliver the requested change with minimal scope, evidence-based design choices, and verification that fits the risk.

## Plan

- Given a blueprint URL or path, read it. Its acceptance criteria are the contract.
- Given anything else (a prompt, issue, or spec file), run the `blueprint` skill first and wait for approval before writing code.

## Discover

- Read applicable project instructions, inspect relevant implementation and tests, and identify existing patterns to reuse.
- Find the project's test command in its instructions, README, Makefile, or package manifest (`pyproject.toml`, `Gemfile`, `package.json`). Never chain fallback commands. A failing suite must report as failing.

## Decide

Apply the `decision-gate` skill to every design decision. Decide two-way doors and log them. Stop only on one-way doors not already approved in the blueprint.

## Implement

- Work through the acceptance criteria in order, one full TDD cycle per criterion:
  1. **RED**: write the test named in its **Verify** line. Run it. It must fail on the real production code for the reason the **Then** describes, not an import, syntax, or setup error.
  2. **GREEN**: write the minimum production code that passes it. Run it.
  3. **Prove it**: revert the production change, confirm the test fails again, restore. Record this as the criterion's evidence.
  4. **REFACTOR** only while green. Extract duplication on its third occurrence, not before.
  5. **Commit** the cycle.

  Each step changes tests or production code, never both.
- For documentation, mechanical configuration, or changes without a meaningful automated test seam, use the criterion's command or manual method.
- A criterion that turns out wrong or missing is a blueprint change: update the page and say so in chat. Do not silently build something else.
- Preserve existing conventions. Use repository-provided generators, worktrees, scripts, and tooling when they exist and fit; do not assume they exist.
- Keep unrelated local changes intact.
- Invoking this skill authorizes local commits on a feature branch. Branch first if on the default branch. Stage files explicitly, one logical change per commit, and match the style of the repo's recent commit subjects. Merging and pushing are one-way doors.

## Verify and hand off

- Run the full test suite and relevant lint, typecheck, or build checks when supported.
- Fill the blueprint's **Verification** section: one card per criterion with status and the evidence recorded during its cycle.
- Self-review the diff for accidental scope expansion and regressions.
- Republish the page and ask the merge question. Report criteria met / not met / not verified, and anything left unresolved.
