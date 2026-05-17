#!/usr/bin/env python3
"""Minimal fake tool for harness-effect parity tests.

Emits the same logical result set in two presentation modes:
- inline: returns the full results array in the response body.
- file: writes a JSONL artifact (meta header + one line per item) and
  returns only an envelope with the artifact path.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

RESULTS = [
    {
        "id": "claim_release_rollback_owner",
        "snippet": "Each release window must declare a rollback owner",
        "evidence": ["source_release_rollback_runbook", "source_operator_review"],
    },
    {
        "id": "claim_release_deployment_window",
        "snippet": "Deployment window must be declared before the release",
        "evidence": ["source_release_rollback_runbook"],
    },
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def emit_inline() -> dict[str, object]:
    return {
        "query": "rollback owner",
        "output_mode": "inline",
        "results": [dict(item) for item in RESULTS],
        "warnings": [],
    }


def emit_file(output_dir: Path, mismatch: bool, drop_citations: bool) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    items = [dict(item) for item in RESULTS]
    if mismatch:
        items = items[:-1]
    if drop_citations:
        for entry in items:
            entry.pop("evidence", None)
    lines = [json.dumps({"meta": {"query": "rollback owner", "kind": "search", "item_count": len(items)}})]
    for index, entry in enumerate(items):
        line = dict(entry)
        line["__index"] = index
        lines.append(json.dumps(line))
    text = "\n".join(lines) + "\n"
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    timestamp = now_iso().replace(":", "").replace("-", "")
    artifact = output_dir / f"fake-tool-{timestamp}-{digest[:8]}.jsonl"
    artifact.write_text(text, encoding="utf-8")
    return {
        "query": "rollback owner",
        "output_mode": "file",
        "artifact": {
            "path": str(artifact),
            "sha256": digest,
            "bytes": len(text.encode("utf-8")),
            "lines": len(lines),
            "format": "jsonl",
            "kind": "search",
        },
        "result_count": len(items),
        "warnings": [],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-mode", choices=["inline", "file"], required=True)
    parser.add_argument("--output-dir")
    parser.add_argument("--mismatch", action="store_true", help="emit one less item in file mode")
    parser.add_argument("--drop-citations", action="store_true", help="strip evidence from file mode items")
    args = parser.parse_args(argv)
    if args.output_mode == "inline":
        sys.stdout.write(json.dumps(emit_inline(), indent=2) + "\n")
        return 0
    if not args.output_dir:
        print("--output-dir required for file mode", file=sys.stderr)
        return 2
    sys.stdout.write(
        json.dumps(emit_file(Path(args.output_dir), args.mismatch, args.drop_citations), indent=2) + "\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
