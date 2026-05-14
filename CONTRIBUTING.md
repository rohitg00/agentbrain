# Contributing

Agent Brain contributions should improve agent judgment, evidence quality, verification, or portability.

## Contribution principles

- Prefer small, reviewable changes.
- Keep public copy runtime-agnostic.
- Add examples for new commands and skills.
- Add verification steps for every workflow.
- Add eval cases when changing behavior.
- Avoid hype, unsupported claims, and broad superiority language.

## Skill contribution checklist

A skill must include:

- trigger,
- required inputs,
- procedure,
- questions,
- anti-rationalization table,
- verification,
- output artifact,
- failure modes,
- at least one example.

## Command contribution checklist

A command spec must include:

- purpose,
- when to use,
- input contract,
- workflow,
- required output,
- stop conditions,
- quality bar.

## Public copy rules

- Do not position Agent Brain by attacking named alternatives.
- Do not include private credentials, tokens, or internal connection strings.
- Treat public discussion as leads, not proof.
- Separate facts, assumptions, and opinions.

## Validation

Run:

```bash
python3 scripts/validate_repo.py
```

If the script is not available yet, check manually:

- all markdown links are sane,
- JSON schemas parse,
- skills have required sections,
- no obvious placeholder text remains.
