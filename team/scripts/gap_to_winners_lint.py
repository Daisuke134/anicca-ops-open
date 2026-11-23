#!/usr/bin/env python3
"""Lint the first markdown table in a file.

Rules (exit 1 if any data row violates them, listing each problem):
  - data row must have exactly 7 cells
  - column 2 (index 1) must contain an http(s) URL
  - column 6 (index 5) must contain an @owner mention

Usage: python3 gap_to_winners_lint.py [FILE]
Default FILE is team/GAP-TO-WINNERS.md.
"""

import re
import sys
from pathlib import Path

DEFAULT_FILE = Path("team/GAP-TO-WINNERS.md")
EXPECTED_COLS = 7
URL_RE = re.compile(r"https?://", re.IGNORECASE)
OWNER_RE = re.compile(r"@[A-Za-z0-9][A-Za-z0-9_-]*")


def split_row(line):
    """Split a markdown table row on pipes into stripped cells."""
    row = line.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [cell.strip() for cell in row.split("|")]


def is_separator_row(line):
    return bool(re.fullmatch(r"[|:\-\s]+", line.strip())) and "-" in line


def first_table_rows(lines):
    """Return (header, separator, data_rows) for the first markdown table."""
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        # Candidate header: next non-empty line must be a separator row.
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines) and is_separator_row(lines[j]):
            data_rows = []
            k = j + 1
            while k < len(lines) and lines[k].strip().startswith("|"):
                data_rows.append((k + 1, lines[k]))  # 1-based line number
                k += 1
            return i + 1, j + 1, data_rows
    return None


def lint_rows(data_rows):
    """Return a list of problem strings for the data rows."""
    problems = []
    for line_no, line in data_rows:
        cells = split_row(line)
        if len(cells) != EXPECTED_COLS:
            problems.append(
                f"line {line_no}: data row has {len(cells)} cells, expected {EXPECTED_COLS}"
            )
            continue
        if not URL_RE.search(cells[1]):
            problems.append(f"line {line_no}: column 2 has no http(s) URL")
        if not OWNER_RE.search(cells[5]):
            problems.append(f"line {line_no}: column 6 has no @owner")
    return problems


def lint_file(path):
    """Lint the first table in `path`; return list of problem strings."""
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    found = first_table_rows(lines)
    if found is None:
        return [f"{path}: no markdown table found"]
    _, _, data_rows = found
    return lint_rows(data_rows)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    path = Path(argv[0]) if argv else DEFAULT_FILE
    problems = lint_file(path)
    if problems:
        for p in problems:
            print(p)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
