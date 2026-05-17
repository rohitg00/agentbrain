# Harness-effect end-to-end example: AKBP search

This example shows how to run `scripts/harness_effect.py` against the real
AKBP reference CLI so the inline-versus-file presentation parity claim has
a measured artifact behind it.

The doctrine is documented in [`docs/harness-effect.md`](../../docs/harness-effect.md).
The eval gate is at [`evals/cases/tool-output-presentation.md`](../../evals/cases/tool-output-presentation.md).
The shipped report is at [`harness-effect-report.akbp-search.json`](harness-effect-report.akbp-search.json).

## Prerequisites

- Python 3.11.
- A local clone of AKBP that exposes `cli/akbp.py` with `output_mode`
  (AKBP main branch on or after PR rohitg00/akbp#48).
- An initialized AKBP knowledge base with at least one cited claim and a
  built FTS5 index. The recipe below builds a throw-away one.

## Build a throw-away knowledge base

```bash
AKBP_REPO=/path/to/akbp
KB=$(mktemp -d)/kb

python3 "$AKBP_REPO/cli/akbp.py" --path "$KB" init
echo "Each release window declares a rollback owner before deployment." > "$KB/notes.md"
python3 "$AKBP_REPO/cli/akbp.py" --path "$KB" source add notes.md --type file --title "Release notes"
python3 "$AKBP_REPO/cli/akbp.py" --path "$KB" remember \
  "Each release window must declare a rollback owner before deployment." \
  --type decision --evidence notes.md
python3 "$AKBP_REPO/cli/akbp.py" --path "$KB" index
```

## Render the fixture

Copy `fixture.template.json` and replace the two placeholders. The script
substitutes `{output_dir}` itself; only the absolute paths and Python
interpreter are filled in here.

```bash
RUN_DIR=$(mktemp -d)
sed \
  -e "s|{{python}}|$(command -v python3.11)|g" \
  -e "s|{{akbp_cli}}|$AKBP_REPO/cli/akbp.py|g" \
  -e "s|{{kb_path}}|$KB|g" \
  examples/harness-effect/fixture.template.json > "$RUN_DIR/fixture.json"
```

## Run the parity measurement

```bash
python3 scripts/harness_effect.py \
  "$RUN_DIR/fixture.json" \
  --output-dir "$RUN_DIR/out" \
  --out "$RUN_DIR/report.json" \
  --fail-on-mismatch
```

A `--fail-on-mismatch` exit code of `0` means file mode preserved the same
retrieved claim ids and citations as inline mode. The committed report at
`harness-effect-report.akbp-search.json` is the canonical pass shape; a
fresh run on the throw-away KB above produces the same retrieved id set
(`claim_<sha-prefix>` and `wiki/log.md`) and the same byte budget pattern
(file envelope smaller than inline because no `results[]` array is
inlined).

## Why the committed report has redacted paths

`examples/harness-effect/harness-effect-report.akbp-search.json` keeps the
verdict, parity diff, envelope hashes, and byte budget from a real run but
replaces machine-specific absolute paths with `{python}`, `{akbp_cli}`,
`{kb_path}`, and `{output_dir}` placeholders. That keeps the artifact
deterministic across machines so `scripts/validate_repo.py` can stay
strict.

## Re-run cadence

Re-run this script whenever:

- the AKBP `output_mode` schema changes,
- agentbrain `scripts/harness_effect.py` changes,
- a new harness tool wires the same parity contract.

A failed verdict is a harness regression and blocks the tool from being
exposed to the model, regardless of byte savings.
