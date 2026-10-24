# Agent skills

Shared local skills for Claude Code and Codex. Edit each skill once in this repository; both agents read the same files through symbolic links.

## Setup

```sh
git clone https://github.com/diegogusava/agent-skills.git ~/desenv/agent-skills
cd ~/desenv/agent-skills
python3 scripts/install.py --dry-run
python3 scripts/install.py
```

The installer links every `skills/<name>` directory into `~/.claude/skills` and `~/.agents/skills`. If the latter already points to the Claude skills directory, it keeps that setup. Existing matching directories are backed up under `~/.local/state/agent-skills/backups/<timestamp>`. Different local versions stop installation before changes occur. Unrelated skills stay in place. Matching legacy copies in `~/.codex/skills` are backed up to prevent duplicate discovery. Repeating installation is safe.

Open a new Claude Code or Codex session after the first installation. These links configure local agents; they do not configure hosted Claude or ChatGPT sessions. A shared skill can still require tools or connectors that only one agent provides. Claude-specific frontmatter and tool names remain as imported; sharing files does not make those features portable.

## Daily use

Edit `skills/<name>/SKILL.md` and its supporting files here. Updates reach both local agents through the links. Commit and push changes to keep GitHub current. On another machine, pull this repository and run the installer again when skills are added.

To add a skill, create `skills/<name>/SKILL.md`, include YAML `name` and `description`, then run `python3 scripts/install.py`.

To undo the initial migration, remove the links created by the installer and move the original skill directories from the timestamped backup to their original paths. Keep this checkout at its installed path while its links are active.

## Included skills

- `blueprint`
- `breakdown`
- `bugfix`
- `commit`
- `decision-gate`
- `dev`
- `frontend-design`
- `humanizer`
- `lavish`
- `markline-review`
- `morador-tempor-rio`
- `orchestrate`
- `owasp-security`
- `po`
- `qa`
- `rails`
- `roteiro-esfregado`
- `seo-geo-aeo`
- `verbete-de-avalia-o-franca`

`sources.json` records each skill's original local path. Supporting files and existing license notices are preserved. No repository-wide license is added for imported third-party material.

## Managed skills

Claude's `synced/` directory, Codex's `.system/` directory, and plugin caches stay under their original managers. They are not copied into this repository. ai-memory skills stay local. The `skills/ai-memory-*/` ignore rule keeps their files out of Git while the installer still links them for both agents. Install these skills separately on another machine. To keep another skill local, add its directory to `.gitignore` before staging it. Ignoring an already tracked skill also requires `git rm --cached -r skills/<name>`; this preserves its local files.

## Discovery references

- [Codex local skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
