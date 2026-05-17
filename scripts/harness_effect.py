#!/usr/bin/env python3
"""Measure tool-output presentation parity for a harness tool.

Agent Brain's `docs/harness-effect.md` says harness changes should be measured,
not asserted. This script runs the same tool twice over the same input set,
once per declared presentation mode (for example `inline` versus `file`), and
reports whether retrieved evidence and citations stayed identical across modes.

The script is intentionally model-agnostic. It does not call an LLM. It calls
a user-supplied tool (any CLI that returns JSON on stdout) once per mode, then
diffs the structured outputs. The output is a JSON harness-effect report that
the rest of the harness can attach to a plan or review artifact.

A fixture file selects the tool, the modes, the request payload, and which
fields define "retrieved evidence" and "citations" for the parity check.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

UTC = dt.timezone.utc

SUPPORTED_MODES = {"inline", "file"}


def now_iso() -> str:
    return dt.datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_fixture(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    require_fields(data, ["id", "tool", "modes"], where=f"fixture {path}")
    require_fields(data["tool"], ["command_template"], where=f"fixture {path} tool")
    if not isinstance(data["modes"], list) or len(data["modes"]) < 2:
        raise ValueError(f"fixture {path} modes must list at least two modes for a parity comparison")
    names: list[str] = []
    for mode in data["modes"]:
        require_fields(mode, ["name", "params"], where=f"fixture {path} mode")
        if mode["name"] not in SUPPORTED_MODES:
            raise ValueError(
                f"fixture {path} mode name must be one of {sorted(SUPPORTED_MODES)}, got {mode['name']!r}"
            )
        names.append(mode["name"])
    if len(set(names)) != len(names):
        raise ValueError(f"fixture {path} modes must be unique, got {names}")
    return data


def require_fields(payload: Any, fields: list[str], *, where: str) -> None:
    if not isinstance(payload, dict):
        raise ValueError(f"{where} must be a JSON object")
    missing = [f for f in fields if f not in payload]
    if missing:
        raise ValueError(f"{where} missing fields: {missing}")


def render_template(template: str, params: dict[str, str], *, max_passes: int = 5) -> str:
    """Render `{placeholder}` references using params, repeating until stable.

    Param values may themselves contain `{placeholder}` references (for
    example a `file_dir_arg` value of `" --output-dir {output_dir}"`). Each
    pass substitutes one layer; the loop stops when the string stops
    changing. Unknown placeholders raise immediately.
    """

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in params:
            raise KeyError(f"template references unknown placeholder: {{{key}}}")
        return str(params[key])

    pattern = re.compile(r"\{([a-zA-Z0-9_]+)\}")
    current = template
    for _ in range(max_passes):
        rendered = pattern.sub(replace, current)
        if rendered == current:
            return rendered
        current = rendered
    raise RuntimeError(
        f"template substitution did not stabilize after {max_passes} passes; current value: {current!r}"
    )


def run_tool(command: str, *, cwd: Path | None = None, timeout: int = 60) -> dict[str, Any]:
    completed = subprocess.run(
        shlex.split(command),
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"tool returned exit {completed.returncode}\ncommand: {command}\nstderr: {completed.stderr.strip()}"
        )
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"tool stdout is not valid JSON\ncommand: {command}\nstdout head: {completed.stdout[:200]!r}"
        ) from exc


def split_path(path: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    escaped = False
    for char in path:
        if escaped:
            buf.append(char)
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == ".":
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(char)
    parts.append("".join(buf))
    return parts


def collect_path(payload: Any, path: str) -> list[Any]:
    values: list[Any] = [payload]
    for part in split_path(path):
        next_values: list[Any] = []
        collect_list = part.endswith("[]")
        key = part[:-2] if collect_list else part
        for value in values:
            if isinstance(value, dict) and key in value:
                child = value[key]
                if collect_list and isinstance(child, list):
                    next_values.extend(child)
                else:
                    next_values.append(child)
            elif isinstance(value, list) and collect_list:
                for entry in value:
                    if isinstance(entry, dict) and key in entry:
                        child = entry[key]
                        if isinstance(child, list):
                            next_values.extend(child)
                        else:
                            next_values.append(child)
        values = next_values
    return values


def load_file_artifact(payload: Any, artifact_path_field: str) -> list[dict[str, Any]]:
    """Resolve a JSONL artifact produced by file-mode tools.

    Returns one dict per non-header line. The header line is allowed but
    skipped so callers can compare item-level fields across modes.
    """
    candidates = collect_path(payload, artifact_path_field)
    candidates = [c for c in candidates if isinstance(c, str) and c]
    if not candidates:
        raise RuntimeError(
            f"file mode response does not expose artifact path at {artifact_path_field!r}"
        )
    artifact = Path(candidates[0])
    if not artifact.exists():
        raise RuntimeError(f"file mode artifact missing on disk: {artifact}")
    lines = artifact.read_text(encoding="utf-8").splitlines()
    items: list[dict[str, Any]] = []
    for line in lines:
        if not line.strip():
            continue
        parsed = json.loads(line)
        if isinstance(parsed, dict) and "meta" in parsed and len(parsed) == 1:
            continue
        items.append(parsed)
    return items


def normalize_evidence(values: list[Any]) -> list[Any]:
    """Sort hashable values when possible, otherwise return them in input order."""
    try:
        return sorted(values)
    except TypeError:
        return values


def evidence_for_mode(
    mode_name: str,
    payload: dict[str, Any],
    *,
    inline_evidence_fields: list[str],
    inline_citation_fields: list[str],
    file_artifact_field: str,
    file_item_evidence_fields: list[str],
    file_item_citation_fields: list[str],
) -> dict[str, Any]:
    if mode_name == "inline":
        retrieved: list[Any] = []
        for field in inline_evidence_fields:
            retrieved.extend(collect_path(payload, field))
        citations: list[Any] = []
        for field in inline_citation_fields:
            citations.extend(collect_path(payload, field))
        return {
            "retrieved_ids": normalize_evidence(retrieved),
            "citations": normalize_evidence(citations),
            "item_count": len(retrieved),
        }
    items = load_file_artifact(payload, file_artifact_field)
    retrieved = []
    citations = []
    for item in items:
        for field in file_item_evidence_fields:
            retrieved.extend(collect_path(item, field))
        for field in file_item_citation_fields:
            citations.extend(collect_path(item, field))
    return {
        "retrieved_ids": normalize_evidence(retrieved),
        "citations": normalize_evidence(citations),
        "item_count": len(items),
    }


def measure_bytes(payload: dict[str, Any]) -> int:
    return len(json.dumps(payload, ensure_ascii=False).encode("utf-8"))


def compute_parity(mode_results: dict[str, dict[str, Any]]) -> dict[str, Any]:
    pairs = list(mode_results.items())
    base_name, base = pairs[0]
    parity: dict[str, Any] = {"reference_mode": base_name, "ids_equal": True, "citations_equal": True, "differences": []}
    for name, other in pairs[1:]:
        ids_equal = base["retrieved_ids"] == other["retrieved_ids"]
        citations_equal = base["citations"] == other["citations"]
        parity["differences"].append(
            {
                "compared_mode": name,
                "ids_equal": ids_equal,
                "citations_equal": citations_equal,
                "missing_in_other_ids": [v for v in base["retrieved_ids"] if v not in other["retrieved_ids"]],
                "extra_in_other_ids": [v for v in other["retrieved_ids"] if v not in base["retrieved_ids"]],
                "missing_in_other_citations": [
                    v for v in base["citations"] if v not in other["citations"]
                ],
                "extra_in_other_citations": [
                    v for v in other["citations"] if v not in base["citations"]
                ],
            }
        )
        parity["ids_equal"] = parity["ids_equal"] and ids_equal
        parity["citations_equal"] = parity["citations_equal"] and citations_equal
    return parity


def run_fixture(
    fixture: dict[str, Any],
    *,
    cwd: Path | None,
    output_dir: Path | None,
    timeout: int,
) -> dict[str, Any]:
    base_params = dict(fixture["tool"].get("base_params", {}) or {})
    template = fixture["tool"]["command_template"]
    parity_fields = fixture.get("parity", {})
    inline_evidence_fields = list(parity_fields.get("inline_retrieved_fields", []))
    file_artifact_field = parity_fields.get("file_artifact_field", "artifact.path")
    file_item_evidence_fields = list(parity_fields.get("file_item_evidence_fields", []))
    inline_citation_fields = list(parity_fields.get("inline_citation_fields", []))
    file_item_citation_fields = list(parity_fields.get("file_item_citation_fields", []))
    if not inline_evidence_fields or not file_item_evidence_fields:
        raise ValueError(
            "fixture parity must declare inline_retrieved_fields and file_item_evidence_fields"
        )
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
    mode_runs: list[dict[str, Any]] = []
    mode_results: dict[str, dict[str, Any]] = {}
    for mode in fixture["modes"]:
        params = {**base_params, **(mode.get("params") or {})}
        if mode["name"] == "file" and output_dir is not None:
            params.setdefault("output_dir", str(output_dir))
        command = render_template(template, params)
        payload = run_tool(command, cwd=cwd, timeout=timeout)
        evidence = evidence_for_mode(
            mode["name"],
            payload,
            inline_evidence_fields=inline_evidence_fields,
            inline_citation_fields=inline_citation_fields,
            file_artifact_field=file_artifact_field,
            file_item_evidence_fields=file_item_evidence_fields,
            file_item_citation_fields=file_item_citation_fields,
        )
        envelope_bytes = measure_bytes(payload)
        mode_runs.append(
            {
                "mode": mode["name"],
                "command": command,
                "envelope_bytes": envelope_bytes,
                "envelope_sha256": hashlib.sha256(
                    json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
                ).hexdigest(),
                "item_count": evidence["item_count"],
            }
        )
        mode_results[mode["name"]] = evidence
    parity = compute_parity(mode_results)
    inline_bytes = next((run["envelope_bytes"] for run in mode_runs if run["mode"] == "inline"), None)
    file_bytes = next((run["envelope_bytes"] for run in mode_runs if run["mode"] == "file"), None)
    bytes_diff = (
        {"inline_envelope_bytes": inline_bytes, "file_envelope_bytes": file_bytes, "file_minus_inline_bytes": file_bytes - inline_bytes}
        if inline_bytes is not None and file_bytes is not None
        else None
    )
    verdict = "pass" if parity["ids_equal"] and parity["citations_equal"] else "fail"
    return {
        "report_version": "1.0",
        "generated_at": now_iso(),
        "fixture_id": fixture["id"],
        "modes": mode_runs,
        "parity": parity,
        "byte_budget": bytes_diff,
        "verdict": verdict,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", help="path to a harness-effect fixture JSON file")
    parser.add_argument("--cwd", help="working directory for the tool invocation")
    parser.add_argument("--output-dir", help="directory passed to file-mode tool invocations as {output_dir}")
    parser.add_argument("--timeout", type=int, default=60, help="per-mode tool timeout in seconds")
    parser.add_argument("--out", help="write the JSON report to this path instead of stdout")
    parser.add_argument("--fail-on-mismatch", action="store_true", help="exit non-zero when parity verdict is fail")
    args = parser.parse_args(argv)
    fixture_path = Path(args.fixture)
    fixture = load_fixture(fixture_path)
    report = run_fixture(
        fixture,
        cwd=Path(args.cwd) if args.cwd else None,
        output_dir=Path(args.output_dir) if args.output_dir else None,
        timeout=args.timeout,
    )
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    else:
        sys.stdout.write(text + "\n")
    if args.fail_on_mismatch and report["verdict"] != "pass":
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
