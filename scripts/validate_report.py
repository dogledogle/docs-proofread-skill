#!/usr/bin/env python3
"""Validate the shape of a docs-proofreader-skill Markdown report."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ISSUE_RE = re.compile(r"^###\s+(\d+)\.\s+`([^`]+)`\s*$", re.MULTILINE)
FILE_SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
REQUIRED_FIELDS = [
    "- 问题描述：",
    "- 修改建议：",
    "- English commit description:",
]


def section_text(content: str, start: int) -> str:
    next_issue = re.search(r"^###\s+\d+\.\s+`", content[start + 1 :], re.MULTILINE)
    next_file = re.search(r"^##\s+", content[start + 1 :], re.MULTILINE)
    candidates = [m.start() + start + 1 for m in (next_issue, next_file) if m]
    end = min(candidates) if candidates else len(content)
    return content[start:end]


def validate(content: str) -> list[str]:
    errors: list[str] = []
    if not re.search(r"^#\s+\S", content, re.MULTILINE):
        errors.append("Missing H1 title.")
    if "审校范围：" not in content:
        errors.append("Missing scope line: 审校范围：")
    if not FILE_SECTION_RE.search(content):
        errors.append("Missing file/page sections starting with ##.")

    matches = list(ISSUE_RE.finditer(content))
    if not matches:
        errors.append("Missing issue headings like: ### 1. `path:line`")
        return errors

    expected = 1
    for match in matches:
        number = int(match.group(1))
        location = match.group(2)
        if number != expected:
            errors.append(f"Issue numbering should be {expected}, found {number}.")
            expected = number
        expected += 1
        if ":" not in location and "#" not in location and not re.search(r"\bhttps?://", location):
            errors.append(f"Issue {number} location should include a line, range, anchor, or URL: {location}")
        body = section_text(content, match.end())
        for field in REQUIRED_FIELDS:
            if field not in body:
                errors.append(f"Issue {number} missing required field: {field}")
        if "- English commit description:" in body and not re.search(
            r"- English commit description:\s*`docs(?:\([^)]+\))?:\s+[^`]+`", body
        ):
            errors.append(f"Issue {number} English commit description should be a backticked docs(...) commit.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="Markdown report to validate.")
    args = parser.parse_args()

    content = args.report.read_text(encoding="utf-8-sig")
    errors = validate(content)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Report format looks valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
