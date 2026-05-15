#!/usr/bin/env python3
"""Scan public copy for source-specific exact names.

Terms are provided at runtime so public repo copy can keep neutral operator-pattern
language without storing session-specific source names in the repository.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

PUBLIC_COPY_GLOBS = [
    "README.md",
    "AGENTBRAIN.md",
    "PRINCIPLES.md",
    "ANTI_RATIONALIZATION.md",
    "CONTRIBUTING.md",
    "commands/*.md",
    "docs/*.md",
    "skills/*/SKILL.md",
    "templates/*.md",
    "evals/**/*.md",
    "adapters/*/README.md",
]
ALLOWED_README_SECTIONS = {"comparisons", "comparison", "benchmarks", "benchmark"}


def iter_public_files(root: Path) -> list[Path]:
    files: set[Path] = set()
    for pattern in PUBLIC_COPY_GLOBS:
        files.update(path for path in root.glob(pattern) if path.is_file())
    return sorted(files)


def readme_section_for_line(lines: list[str], line_number: int) -> str:
    current = ""
    for index, line in enumerate(lines, start=1):
        if index > line_number:
            break
        if line.startswith("## "):
            current = line.removeprefix("## ").strip().lower()
    return current


def is_allowed_occurrence(path: Path, root: Path, lines: list[str], line_number: int) -> bool:
    if path.relative_to(root).as_posix() != "README.md":
        return False
    return readme_section_for_line(lines, line_number) in ALLOWED_README_SECTIONS


def find_violations(root: Path, terms: list[str]) -> list[str]:
    unique_terms = sorted({term for term in terms if term})
    normalized_terms = [(term, term.casefold()) for term in unique_terms]
    violations: list[str] = []
    for path in iter_public_files(root):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(lines, start=1):
            normalized_line = line.casefold()
            for term, normalized_term in normalized_terms:
                if normalized_term not in normalized_line:
                    continue
                if is_allowed_occurrence(path, root, lines, line_number):
                    continue
                violations.append(f"{path.relative_to(root)}:{line_number}: contains banned exact name: {term}")
    return violations


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scrub public copy for source-specific exact names.")
    parser.add_argument("terms", nargs="*", help="Exact source names or branding strings to ban.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(os.environ.get("AGENTBRAIN_SCRUB_ROOT", Path(__file__).resolve().parents[1])).resolve()
    violations = find_violations(root, args.terms)
    if violations:
        print("Banned exact names found in public copy:")
        for violation in violations:
            print(f"- {violation}")
        return 1
    print("No banned exact names found in public copy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
