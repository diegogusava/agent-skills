---
name: blueprint
description: Publish a visual, phone-readable plan for a change (change map, Given/When/Then acceptance criteria with edge cases, files, steps) and stop for approval. Used before dev and orchestrate, or alone when the user asks for a plan.
---

# Blueprint

Show what will change and how success will be proven, before any code is written. The blueprint is the contract: the implementer builds against its acceptance criteria and the reviewer checks against them.

## Discover

- Read project instructions and the code around the change. Reuse existing patterns.
- Classify decisions with `decision-gate`. Do not write production code or tests.

## The page

One page per task, republished to the same URL as it evolves. Publish it as a private Artifact when the harness has one; otherwise write `.briefs/<feature-slug>/<task-slug>.html` (the whole `.briefs/` folder is gitignored) and print the path. Design for a phone: single column, no wide tables, cards over grids. Type size: body text 19px, secondary text (captions, criterion fields, file notes) at least 17px, small uppercase labels and chips at least 15px, inline code at least 16px. Never go below 15px anywhere; the user reads these pages on a phone.

Sections, in order:

1. **Goal**: one sentence.
2. **Change map**: one Mermaid `flowchart TD` of the affected components. Color nodes with `classDef`: new (green), changed (amber), removed (red, dashed border), untouched context (grey). Only the neighborhood of the change, at most about 12 nodes.
3. **One-way doors**: per `decision-gate`, each with before/after diagrams and a "Your call" question.
4. **Acceptance criteria**: see below. This is the section the user reviews most closely.
5. **Files**: path, add / change / delete, one-line reason. A stacked list, not a table.
6. **Steps**: the commits expected, in order, each naming the criteria it satisfies.
7. **Out of scope**: what was noticed and will not be touched, including edge cases deliberately left unhandled and why.
8. **Verification**: empty until implementation ends (see below).

## Acceptance criteria

Each criterion is a card:

```
AC-3 · Stale hotels are re-queued when the queue is empty
Given  no WAITING rows and 40 hotels crawled more than 7 days ago
When   the queue watchdog ticks
Then   the 20 oldest are promoted to WAITING
Verify test: tests/test_queue.py::test_promotes_oldest_when_empty
```

Rules:

- Group into **Main flow**, **Edge cases**, **Failure cases**. Number continuously (AC-1, AC-2, ...) so ids never repeat.
- One observable outcome per **Then**. If you need "and", write a second criterion.
- **Given** uses concrete values, not "some data".
- Consider every edge case that applies and list only those: empty / zero / missing input, boundaries, duplicates and repeats, ordering, concurrency, external failure (timeout, block, bad response), existing data written by the old code, permissions. Do not pad.
- **Verify** names exactly one method, in order of preference:
  - `test:` the test file and name that will be written
  - `command:` a command and its expected output
  - `manual:` numbered steps, only when there is no automated seam, and say why
- Tests are written in the order of the criteria. The criteria replace a separate test list.

## Verification

Filled in by the implementer when the work is done, then checked by the reviewer. One card per criterion:

```
AC-3 · met
Evidence  tests/test_queue.py::test_promotes_oldest_when_empty passed (commit a1b2c3d)
          failed with the change reverted: yes
Reviewer  confirmed
```

- **Status**: `met`, `not met`, or `not verified`. A criterion without evidence is `not verified`, never `met`.
- **Evidence**: the test id with its run result and the commit, or the command with an excerpt of its output, or the manual steps and what was observed. For test-verified criteria, say whether the test failed with the production change reverted.
- **Reviewer**: `confirmed` or `disputed: <reason>`. The reviewer, whether a fresh agent or the user, must for each card:
  1. Read the test and check that it sets up the **Given**, performs the **When**, and asserts the **Then**. A weaker assertion counts as disputed.
  2. Re-run it.
  3. For at least one main-flow criterion, revert the production change and confirm the test fails.

## Approval

Stop after publishing. The user answers with a comment on the page or in chat. Revise and republish until approved. Record the approval in the page, then hand off: `/dev <page url or path>`.
