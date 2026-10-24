---
name: decision-gate
description: Classify each design decision as reversible or hard to reverse; decide and log the reversible ones, stop on the rest with a visual brief the user can read on a phone. Used by dev, bugfix, and orchestrate.
---

# Decision gate

Interrupt the user only for decisions that are hard to undo. Everything else, decide and keep moving.

## Classify

**Two-way door** (undo = `git revert` and nothing else): function bodies behind a tested interface, private names, file layout inside a module, which test to write first, refactors that keep the suite green, log messages, UI copy, CSS, local commits on a feature branch.

→ Decide. Append one line to the brief's **Decided** log. Continue.

**One-way door** (undo needs more than a revert):

- Schema, migration, or any persisted format another system reads
- Public contract: URL (SEO), API shape, CLI flag, event or file format other code consumes
- Process or concurrency model: worker count, in-process vs. scheduled work, locking
- Deploy topology: services, timers, proxy config, infra files
- New runtime dependency or external service
- Deleting or rewriting data; auth, permissions, secrets
- Merging to the default branch or pushing

→ Stop. Update the brief. Notify. Wait for the user's answer.

When unsure, it is a one-way door.

## The brief

One brief per task, one file, republished as the task grows so the URL stays the same. When a `blueprint` exists, the brief is that same page: add decisions to it rather than publishing a second one. Keep it to one phone screen per decision. Use the blueprint skill's type sizes (body 19px, nothing below 15px):

- **Title** and a tag saying which one-way category it hits
- **Before / after**: two small Mermaid `flowchart TD` diagrams of the parts that change. Vertical, 3 to 6 nodes each, so they fit a phone.
- **Why**: the evidence that forced the decision, with numbers when there are any
- **Cost**: what gets coupled, removed, or harder later
- **Undo**: the concrete steps to reverse it
- **Your call**: the question, the options, and your recommendation
- **Decided**: every two-way decision taken so far, one line each

Publish it as a private Artifact when the harness has one. Otherwise write `.briefs/<feature-slug>/<task-slug>.html` (the whole `.briefs/` folder is gitignored) and print the path. Never commit a brief.

## Notify and resume

- Send a push notification with the one-line question when the harness supports it. Send one only for one-way doors.
- Accept the answer from a comment on the brief or a chat reply. Record it in the brief, then resume.
- At the end of the task, fill the blueprint's **Verification** section (or, without a blueprint, list files changed and checks run with their outcome). The final ask is always the merge.
