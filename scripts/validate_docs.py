#!/usr/bin/env python3
"""Verify product documentation page structure and internal navigation links."""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted(ROOT.rglob("*.mdx"))
LINK = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})", re.M)
ERRORS: list[str] = []

def error(where: Path, what: str) -> None:
    ERRORS.append(f"{where.relative_to(ROOT)}: {what}")

def target_path(origin: Path, href: str) -> Path | None:
    href = href.split("#", 1)[0].split("?", 1)[0]
    if not href or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", href):
        return None
    candidate = ROOT / href.lstrip("/") if href.startswith("/") else origin.parent / href
    if candidate.is_file():
        return candidate
    if candidate.suffix == "":
        return candidate.with_suffix(".mdx")
    return candidate

for page in PAGES:
    content = page.read_text("utf-8")
    if not content.startswith("---\n"):
        error(page, "missing MDX frontmatter")
    else:
        try:
            frontmatter, _ = content[4:].split("\n---\n", 1)
        except ValueError:
            error(page, "unclosed MDX frontmatter")
        else:
            for field in ("title", "description"):
                match = re.search(rf"(?m)^{field}: (.+)$", frontmatter)
                if not match:
                    error(page, f"missing {field}")
                else:
                    try:
                        json.loads(match.group(1))
                    except json.JSONDecodeError:
                        error(page, f"{field} is not a valid quoted string")
    fences = FENCE.findall(content)
    if len(fences) % 2:
        error(page, "odd number of Markdown code fences")
    for href in LINK.findall(content):
        target = target_path(page, href)
        if target is not None and not target.is_file():
            error(page, f"broken link: {href}")
    if page.parent.name == "scenarios" and page.name != "index.mdx":
        if "## Walkthrough" not in content:
            error(page, "scenario is missing walkthrough steps")
        if "Expected review outcome" not in content:
            error(page, "scenario is missing an expected outcome")
        if "Recovery path" not in content and "If it does not work" not in content:
            error(page, "scenario is missing recovery guidance")
    if re.search(r"(?i)mintlify|data processor deployment|sensor integration", content):
        error(page, "contains out-of-scope setup or integration content")

if not PAGES:
    ERRORS.append("No MDX pages found")

if ERRORS:
    print("\n".join("FAIL " + value for value in ERRORS))
    sys.exit(1)
print(f"PASS: {len(PAGES)} MDX pages; frontmatter, internal links, scenario completeness and scope checked.")
