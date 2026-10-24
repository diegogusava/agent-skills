---
name: commit
description: Stage the files of one logical change explicitly and commit them with a message in the repository's own style.
argument-hint: "[files or intent]"
disable-model-invocation: true
---

# Commit

Typing `/commit` is the authorization to commit. Do not ask again unless something below says stop.

## Current state

!`git status --short`

!`git log -12 --format=%s`

## Workflow

1. **Pick the files.** Use the files named in the arguments, or the ones already staged, or the working-tree changes that belong to one logical change. Stage each one explicitly with `git add <file>`. Never `git add .` or `-A`.
2. **Check the scope.** Read `git diff --cached`. If it mixes unrelated changes, stage only one of them and say what was left out. If nothing is left to commit, say so and stop.
3. **Check for secrets.** Stop if the diff contains credentials, `.env` files, or keys.
4. **Write the message** in the style of the recent subjects above: same prefix convention or lack of one, same case, same tense. If the repo has no clear style, use present tense imperative and lowercase. Keep the subject under about 72 characters. Describe the change itself. Add a body only when the reason is not obvious from the diff.
5. **Commit** on the current branch. Show `git log -1 --stat`.

Never push, amend a pushed commit, or skip hooks unless the user asks.
