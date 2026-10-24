#!/usr/bin/env python3
"""Link this checkout's skills into Claude Code and Codex. Keep backups."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--home', type=Path, default=Path.home(), help='Home directory (also useful for an isolated test)')
parser.add_argument('--dry-run', action='store_true')
args = parser.parse_args()
repo = Path(__file__).resolve().parents[1]
home = args.home.expanduser().resolve()
claude = home / '.claude/skills'
agents = home / '.agents/skills'
legacy = home / '.codex/skills'
backup = home / '.local/state/agent-skills/backups' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
skills = sorted(p for p in (repo / 'skills').iterdir() if (p / 'SKILL.md').is_file())

# Check all conflicts before changing any files. Unknown skills stay untouched.
for source in skills:
    for root in [claude, agents, legacy]:
        target = root / source.name
        if not target.exists() and not target.is_symlink():
            continue
        if target.resolve() == source.resolve():
            continue
        if target.is_symlink():
            raise SystemExit(f'Refusing to replace an unrelated symlink: {target}')
        if not target.is_dir():
            raise SystemExit(f'Expected a skill directory: {target}')
        current = {p.relative_to(target): p.read_bytes() for p in target.rglob('*') if p.is_file()}
        expected = {p.relative_to(source): p.read_bytes() for p in source.rglob('*') if p.is_file()}
        if current != expected:
            raise SystemExit(f'Local skill differs from the repository: {target}. Merge it first.')

operations = []
def save(path):
    dest = backup / path.relative_to(home)
    operations.append(f'Backup {path} -> {dest}')
    if not args.dry_run:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), str(dest))

def link(target, source):
    if target.is_symlink() and target.resolve() == source.resolve():
        return
    if target.exists() or target.is_symlink():
        save(target)
    operations.append(f'Link {target} -> {source}')
    if not args.dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(source, target_is_directory=True)

# Claude and Codex use the same source files. A separate agents root is also supported.
shared_root = agents.resolve() == claude.resolve()
for source in skills:
    # Remove legacy Codex copies to prevent duplicate discovery. Preserve originals.
    old = legacy / source.name
    if (old.exists() or old.is_symlink()) and old.resolve() != source.resolve():
        save(old)
    link(claude / source.name, source)
    if not shared_root:
        link(agents / source.name, source)

print('\n'.join(operations) if operations else 'All skill links are already current.')
print(f'{len(skills)} skills; ' + ('dry run, no changes made.' if args.dry_run else 'installation complete.'))
