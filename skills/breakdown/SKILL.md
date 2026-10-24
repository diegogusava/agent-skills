---
name: breakdown
description: "Decompose a PRD phase, plan, or large feature into small, codebase-grounded implementation tasks grouped into parallel batches by file overlap and dependency. Produces a breakdown file whose tasks feed /blueprint one at a time. Use when: break down, breakdown, split into tasks, decompose, parallelize work, task breakdown, split this phase, chunk the work, plan tasks."
---

# Breakdown

Turn a large piece of scope (a PRD phase, a feature, a plan) into a numbered list of small tasks, each
independently buildable, then group them into **parallel batches** based on what actually conflicts:
file overlap and inter-task dependencies. Output is a working plan in `.briefs/{feature-slug}/breakdown.md`,
designed to be picked up one task at a time with `/blueprint .briefs/{feature-slug}/breakdown.md task N`,
then `/dev <blueprint url>` once the blueprint is approved.

A breakdown is scaffolding for one piece of work, not a record. A later breakdown can override its
decisions and nothing would mark it stale, so it never goes in the repo. Decisions that outlive the work
go to ADRs (Phase 6); what was built is recorded by code, tests, and commit messages.

The job is not "list the work." It is to find the **dependency and file-conflict graph** so work can fan
out safely, and to ground every task in code that already exists (reuse over rebuild).

## Usage

- `/breakdown <path-to-PRD-or-plan>` — break the referenced doc (or a named section/phase) into tasks
- `/breakdown <description>` — break down a feature described inline
- `/breakdown` — ask the user what to break down

## Workflow

### Phase 1: Read the source

Read the full scope to be split:
- The PRD section / phase (Must Have, Should Have, Out of Scope, Acceptance Criteria, appendices).
- Any prototype, mockup, or design doc it references — these pin down UI states and copy.
- If the user named a "phase," read the **other phases too**: they reveal what's already built that this
  phase consumes, and the conventions to match.

### Phase 2: Match existing conventions

Find how this project already records planned work and **copy that format**:
- Look for sibling plan files (e.g. prior phase folders, `docs/prd/phases/*`). Match their section shape,
  their task-numbering scheme, their Status table.
- A breakdown that doesn't match house style creates friction. Mirror it.

**Write the breakdown to `.briefs/{feature-slug}/breakdown.md`**, next to the `/blueprint` pages for the
same feature. Leave the source PRD or phase doc where it is. If `.briefs/` is not in `.gitignore` yet,
add `/.briefs/` in its own commit. Committed breakdowns from before this rule stay as history; don't move
them unless asked.

### Phase 3: Ground in the codebase (the important part)

Do not split from the PRD alone. Survey the real code so tasks reference real files and reuse real
infrastructure. For each capability the scope needs, find:
- **Models / tables** that already exist (don't propose a new model when a column or scope will do).
- **Services / jobs / mailers** to reuse or extend. A prior phase often already built the exact service
  this phase needs (e.g. a coverage stat, a queue, a recurring-job pattern). Call it out explicitly.
- **Hook points** — where progress/events are already emitted, where new behavior should attach.
- **Shared/central files** — `routes.rb`, locale files (`en.yml`), config (`recurring.yml`), a shared
  partial, a base controller. These are the parallelism killers (see Phase 5).

Reuse-first, per the deletion-beats-addition principle: if two tasks would duplicate logic, make one
extract a shared piece and the other consume it, and say so in the task.

Use Explore/Grep/Read directly. Spawn agents only if the user asks.

### Phase 4: Define tasks

Each task is the smallest unit that delivers one coherent, testable change and **fits comfortably in a
single focused session** (rule of thumb: ~50% of a Sonnet context). Prefer more small tasks over fewer
big ones. Every task gets:

- **What** — one paragraph. The behavior, not the keystrokes. Name the service/model it adds or changes.
- **Files** — the concrete paths to create or edit (incl. migration, model, service, controller, view,
  routes, locales).
- **Tests** — the specific cases that prove it, in the project's test style. Lead with the behavior, then
  edge cases (empty/zero, boundary, unauthenticated, no-divide-by-zero).
- **Dependencies** — which task numbers must land first, or "none."

Order so that data/services come before the pages/integration that consume them.

### Phase 5: Build the parallel batches

This is what makes a breakdown worth doing. Two tasks may run in parallel **only if both hold**:
1. **No dependency** — neither needs the other's output.
2. **No file overlap** — they create/edit disjoint files.

Group tasks into ordered batches (A, B, C…). Within a batch, everything runs concurrently; each batch
waits on the prior. Then **audit for shared-file traps** and state them plainly:

- Locale files (`en.yml`), `routes.rb`, a central config, or a shared partial are often touched by many
  UI tasks. Additive edits to *different namespaces* are logically independent but **still collide in the
  same working tree**. Call this out: either run each parallel task in its own **worktree**, or serialize
  just that one file's edit. Don't pretend the conflict isn't there.

If a task touches a file another "parallel" task also touches, it is **not** parallel — move it to a later
batch or note the worktree requirement.

### Phase 6: Decisions, not guesses

Where the scope leaves a genuine choice (premium gating, an approximation when no data source exists, a
naming collision), **flag it inline as a note** in the relevant task. Pick a sensible v1 default, state
it, and move on. Do not silently invent infrastructure (new preference systems, new tracking tables) when
the constraint is "reuse what exists" — say "check X first."

**Decisions that outlive the work become ADRs.** If a decision will still constrain future work after the
task ships (a data-model change, a changed meaning of stored data, an irreversible migration, a chosen
dependency), add to that task: "Record ADR: {one-line decision}". The task writes `docs/adr/NNNN-{slug}.md`
in the project's ADR format when it lands. If it reverses an earlier ADR, the new ADR says
"Supersedes NNNN" and the old one's status becomes "Superseded by NNNN". Skip ADRs for choices that only
matter while building (task order, v1 defaults a later task replaces).

### Phase 7: Write the plan file

Write `.briefs/{feature-slug}/breakdown.md` (Phase 2). Match the discovered house format for the file's
internals. Use the structure below, then tell the user the batch layout and the command to start:
`/blueprint .briefs/{feature-slug}/breakdown.md task N`.

```markdown
# {Feature} — Phase {N}: {Title}

PRD: `docs/prd/.../{source}.md` §{section}
Prototype: `{path}` (if any)

{One paragraph: task count, the "fits one session" claim, the consume-order rule, and any global
constraint that shapes every task (perf budget, no-new-services, reuse of a prior-phase service).}

## Parallelization

**Batch A — {theme} (tasks X–Y).** {Why they're independent.} **Run in parallel.**
**Batch B — {theme} (tasks …).** {Depends on A.} **Run in parallel after A.**
...

> **{shared-file} caveat.** {Which tasks touch it, why it's additive, and the worktree-or-serialize rule.}

## Task N.M — {title}

**What:** ...
**Files:** ...
**Tests:** ...
**Dependencies:** {task numbers | none}
**Record ADR:** {one-line decision} (only when Phase 6 applies)

...

## Status

| Task | Description | Batch | Status |
|------|-------------|-------|--------|
| N.1  | ...         | A     | todo   |
```

## Rules

- Ground every task in real files. A task that names no concrete path is not ready.
- Reuse before adding. Point at the existing service/model/job/pattern by name.
- Parallel means **disjoint files AND no dependency** — both, every time. When in doubt, serialize.
- Always surface shared-file traps (locales, routes, config). Silent conflicts waste a whole parallel run.
- Tests are part of the task, not an afterthought. Specify the cases.
- Flag real decisions; don't guess and don't over-engineer a default.
- Match the project's existing plan-file format. Don't impose a new one.
- The breakdown lives in `.briefs/{feature-slug}/`, never in the repo. Lasting decisions go to `docs/adr/`.
- Keep it concrete and terse. No filler. Never use em dashes.
