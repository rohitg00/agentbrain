#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

for path in sorted((ROOT / 'schemas').glob('*.json')):
    try:
        json.loads(path.read_text())
    except Exception as exc:
        errors.append(f'invalid json schema {path.relative_to(ROOT)}: {exc}')

required_root = ['README.md', 'AGENTBRAIN.md', 'PRINCIPLES.md', 'ANTI_RATIONALIZATION.md']
for rel in required_root:
    if not (ROOT / rel).exists():
        errors.append(f'missing {rel}')

required_skill_sections = ['## Trigger', '## Inputs', '## Procedure', '## Verification', '## Failure Modes', '## Example']
for skill in sorted((ROOT / 'skills').glob('*/SKILL.md')):
    text = skill.read_text(errors='ignore')
    for section in required_skill_sections:
        if section not in text:
            errors.append(f'{skill.relative_to(ROOT)} missing {section}')

for command in sorted((ROOT / 'commands').glob('*.md')):
    text = command.read_text(errors='ignore')
    for section in ['## Purpose', '## When to use', '## Input contract', '## Workflow', '## Output', '## Stop conditions']:
        if section not in text:
            errors.append(f'{command.relative_to(ROOT)} missing {section}')

banned = ['Garry', 'GBrain', 'GStack', 'Hermes vs', 'OpenClaw vs', 'Claude vs', 'Codex vs']
for md in sorted(ROOT.rglob('*.md')):
    if '.git' in md.parts:
        continue
    text = md.read_text(errors='ignore')
    for term in banned:
        if term in text:
            errors.append(f'{md.relative_to(ROOT)} contains banned public-copy term: {term}')

if errors:
    print('Validation failed:')
    for err in errors:
        print(f'- {err}')
    sys.exit(1)

print('Validation passed')
