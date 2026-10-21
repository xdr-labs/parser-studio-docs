#!/usr/bin/env python3
"""Check Parser Studio user-manual navigation, MDX links, screenshots and scope.

Runs offline using Python standard libraries only.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted(ROOT.rglob("*.mdx"))
PAGE_NAMES = {str(p.relative_to(ROOT).with_suffix("")) for p in PAGES}
MARKDOWN_LINK = re.compile(r'(?<!!)\[[^\]]+\]\(([^)]+)\)')
MARKDOWN_IMAGE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
MDX_URL = re.compile(r'\b(?:href|src)="([^"]+)"')
IMAGE_TAG = re.compile(r'<img\b[^>]*>', re.IGNORECASE | re.DOTALL)
FENCE = re.compile(r'^\s*(`{3,}|~{3,})', re.MULTILINE)
FRONTMATTER = re.compile(r'^---\n(.*?)\n---\n', re.DOTALL)
FIELDS = ("title", "description", "sidebarTitle")
ERRORS: list[str] = []
REFERENCED_IMAGES: set[str] = set()


def error(where: Path, message: str) -> None:
    ERRORS.append(f"{where.relative_to(ROOT)}: {message}")


def local_url_path(page: Path, raw_url: str) -> Path | None:
    url = raw_url.split("#", 1)[0].split("?", 1)[0]
    if not url or url.startswith(("#", "mailto:", "tel:", "//")):
        return None
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", url):
        return None
    candidate = (ROOT / url.lstrip("/")) if url.startswith("/") else (page.parent / url)
    if not candidate.suffix:
        return candidate.with_suffix(".mdx")
    return candidate


if not PAGES:
    ERRORS.append("No MDX pages found")

for page in PAGES:
    content = page.read_text(encoding="utf-8")
    m = FRONTMATTER.search(content)
    if not m:
        error(page, "missing or unclosed MDX frontmatter")
    else:
        meta = m.group(1)
        for field in FIELDS:
            match = re.search(rf"(?m)^{field}: (.+)$", meta)
            if not match:
                error(page, f"missing {field}")
                continue
            try:
                value = json.loads(match.group(1))
                if not isinstance(value, str) or not value.strip():
                    error(page, f"{field} must be a nonempty string")
            except json.JSONDecodeError:
                error(page, f"{field} is not a JSON-quoted string")
    if len(FENCE.findall(content)) % 2:
        error(page, "unpaired Markdown code fence")

    for image_alt, image_url in MARKDOWN_IMAGE.findall(content):
        if not image_alt.strip():
            error(page, "Markdown image has no alt text")
        image_target = local_url_path(page, image_url)
        if image_target and image_target.suffix.lower() == ".png" and image_target.is_file():
            if image_target.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
                error(page, f"invalid screenshot PNG {image_url}")

    for raw_url in MARKDOWN_LINK.findall(content) + MDX_URL.findall(content) + [url for _, url in MARKDOWN_IMAGE.findall(content)]:
        target = local_url_path(page, raw_url)
        if target is None:
            continue
        if not target.is_file():
            error(page, f"missing local target {raw_url}")
        if target.suffix.lower() in (".png", ".jpeg", ".jpg", ".svg", ".webp"):
            REFERENCED_IMAGES.add(str(target.relative_to(ROOT)))
    for img_tag in IMAGE_TAG.findall(content):
        if not re.search(r'\balt="[^"]+"', img_tag):
            error(page, "image has no nonempty alt text")

    if page.parent.name == "scenarios" and page.name != "index.mdx":
        localized = "ko" in page.parts and page.relative_to(ROOT).parts[0] == "ko"
        sections = (
            ("## 따라 하기", "## 예상 결과", "## 복구 방법")
            if localized else
            ("## Walkthrough", "## Expected review outcome", "## Recovery path")
        )
        for required in sections:
            if required not in content:
                error(page, f"scenario is missing {required}")
    if page.relative_to(ROOT).parts[0] == "ko" and not re.search(r"[가-힣]", content):
        error(page, "Korean localized page has no Hangul instructional text")
    if re.search(r"(?i)\bmintlify\b|data processor deployment|sensor integration", content):
        error(page, "out-of-scope documentation or integration claim")

manifest = ROOT / "docs.json"
if not manifest.exists():
    ERRORS.append("docs.json is missing")
else:
    try:
        config = json.loads(manifest.read_text(encoding="utf-8"))
        nav = config["navigation"]
        localized_nav = nav.get("languages")
        if localized_nav:
            languages = [section.get("language") for section in localized_nav]
            if languages != ["en", "ko"]:
                ERRORS.append(f"unexpected bilingual locale sequence: {languages}")
            menu_paths = [
                path for section in localized_nav
                for group in section["groups"] for path in group["pages"]
            ]
            english = {
                path for group in localized_nav[0]["groups"] for path in group["pages"]
            }
            korean = {
                path for group in localized_nav[1]["groups"] for path in group["pages"]
            }
            if korean != {"ko/" + path for path in english}:
                ERRORS.append("missing or extra localized EN/KO page counterpart")
            if any(path.startswith("ko/") for path in english):
                ERRORS.append("English navigation contains localized paths")
        else:
            groups = nav["groups"]
            menu_paths = [path for group in groups for path in group["pages"]]
        if len(menu_paths) != len(set(menu_paths)):
            ERRORS.append("docs.json navigation contains duplicate pages")
        if set(menu_paths) != PAGE_NAMES:
            ERRORS.append(
                f"navigation mismatch: missing {sorted(PAGE_NAMES - set(menu_paths))}, "
                f"unknown {sorted(set(menu_paths) - PAGE_NAMES)}"
            )
        if not all((ROOT / value.lstrip("/")).read_text(encoding="utf-8").lstrip().startswith("<svg") for value in [
                config.get("logo", {}).get("light", "/missing"),
                config.get("logo", {}).get("dark", "/missing"),
                config.get("favicon", "/missing"),
            ] if (ROOT / value.lstrip("/")).is_file()):
            ERRORS.append("SVG branding has invalid content")
        for name in ("light", "dark"):
            logo = config.get("logo", {}).get(name)
            if not logo or not (ROOT / logo.lstrip("/")).is_file():
                ERRORS.append(f"missing {name} branding logo")
        favicon = config.get("favicon")
        if not favicon or not (ROOT / favicon.lstrip("/")).is_file():
            ERRORS.append("missing favicon")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        ERRORS.append(f"docs.json cannot be validated: {exc}")

for extra in ("style.css",):
    if not (ROOT / extra).is_file():
        ERRORS.append(f"missing XDR Labs style asset {extra}")

if not REFERENCED_IMAGES:
    ERRORS.append("no actual product screenshots referenced")

if ERRORS:
    print("\n".join(f"FAIL {issue}" for issue in ERRORS))
    sys.exit(1)

print(
    "PASS:",
    len(PAGES), "MDX pages;",
    len(REFERENCED_IMAGES), "referenced screenshots/assets;",
    "navigation, internal links, MDX frontmatter, scenarios and scope checked."
)
