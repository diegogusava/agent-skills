---
name: orchestrate
description: Delegate implementation and independent review of a scoped change, then coordinate verified fixes, stopping only on hard-to-reverse decisions.
disable-model-invocation: true
---

# Orchestrate

Coordinate subagents without directly implementing production code. Preserve an independent review boundary and keep the user informed of material findings.

## Prepare

- Read project instructions, inspect current changes, and define the task's expected outcome and verification criteria.
- Split only genuinely independent work. Serialize tasks that share files or depend on each other.
- Give each delegate the relevant task context and constraints, but do not tell reviewers the implementation rationale or desired verdict.
- Run the `blueprint` skill (or read the one supplied) and wait for approval. Its acceptance criteria are the contract for implementer and reviewer.
- You own the `decision-gate` brief. Tell implementers to report every design decision they made, not to decide one-way doors themselves.

## Execute the review loop

1. Delegate implementation to one agent with the acceptance criteria. Require a concise report of changed files, design decisions, assumptions, and one verification card per criterion (status and evidence, as defined in `blueprint`). It must not commit.
2. Classify the reported decisions with `decision-gate`. Log two-way doors. Stop on one-way doors before review.
3. Delegate an adversarial review to a fresh agent, supplying the acceptance criteria, the verification cards, relevant conventions, and the diff. It must run the blueprint's reviewer procedure on every card and mark it `confirmed` or `disputed`, then hunt for correctness, boundary, and regression problems the criteria missed.
4. Assess findings against the code and task. Delegate substantiated fixes to an implementation agent; re-review non-trivial fixes with a fresh reviewer.
5. Run the project's relevant final checks. If a check cannot run, report that as an unresolved risk.

## Boundaries

- Use available subagent capabilities; do not assume special agent types, worktrees, scripts, or a particular repository layout.
- Keep implementation and review separate. Do not treat an absence of findings as proof without considering what was checked.
- Summarize outcomes and ranked real findings rather than relaying raw agent transcripts.
- Once the review is clean, invoking this skill authorizes a local commit on a feature branch. Stage files explicitly and match the repo's commit style. Merging and pushing are one-way doors.
