#!/usr/bin/env python3
"""Search the installed punkpeye/awesome-mcp-servers catalog."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Iterable


DEFAULT_CATALOG_DIR = Path(
    os.environ.get(
        "AWESOME_MCP_SERVERS_PATH",
        "/Users/kunanonjarat/.codex/sources/awesome-mcp-servers",
    )
)

MARKERS = {
    "official": ["\U0001f396", "\U0001f396\ufe0f"],
    "python": ["\U0001f40d"],
    "typescript": ["\U0001f4c7"],
    "go": ["\U0001f3ce", "\U0001f3ce\ufe0f"],
    "rust": ["\U0001f980"],
    "csharp": ["#\ufe0f\u20e3"],
    "java": ["\u2615"],
    "cpp": ["\U0001f30a"],
    "ruby": ["\U0001f48e"],
    "cloud": ["\u2601", "\u2601\ufe0f"],
    "local": ["\U0001f3e0"],
    "embedded": ["\U0001f4df"],
    "macos": ["\U0001f34e"],
    "windows": ["\U0001fa9f"],
    "linux": ["\U0001f427"],
}

LANGUAGE_KEYS = ("python", "typescript", "go", "rust", "csharp", "java", "cpp", "ruby")
SCOPE_KEYS = ("cloud", "local", "embedded")
OS_KEYS = ("macos", "windows", "linux")

BADGE_RE = re.compile(r"\[!\[[^\]]*\]\([^)]+\)\]\([^)]+\)")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
ANCHOR_RE = re.compile(r"<a\s+name=\"([^\"]+)\"></a>")
HEADING_PREFIX_RE = re.compile(r"^[^A-Za-z0-9]+")


def has_marker(text: str, key: str) -> bool:
    return any(marker in text for marker in MARKERS[key])


def marker_names(text: str, keys: Iterable[str]) -> list[str]:
    return [key for key in keys if has_marker(text, key)]


def clean_heading(line: str) -> str:
    heading = line.removeprefix("###").strip()
    heading = ANCHOR_RE.sub("", heading).strip()
    heading = HEADING_PREFIX_RE.sub("", heading).strip()
    return heading or "Uncategorized"


def clean_description(text: str) -> str:
    text = BADGE_RE.sub("", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip(" -")


def parse_catalog(readme: Path) -> list[dict[str, object]]:
    section = "Uncategorized"
    entries: list[dict[str, object]] = []

    for line_number, line in enumerate(readme.read_text(encoding="utf-8").splitlines(), start=1):
        if line.startswith("### "):
            section = clean_heading(line)
            continue

        if not line.startswith("- ["):
            continue

        link = LINK_RE.search(line)
        if not link:
            continue

        name, url = link.group(1), link.group(2)
        after_link = line[link.end() :]
        parts = re.split(r"\s-\s", after_link, maxsplit=1)
        description = clean_description(parts[1] if len(parts) == 2 else after_link)

        entries.append(
            {
                "name": name,
                "url": url,
                "category": section,
                "description": description,
                "line": line_number,
                "official": has_marker(line, "official"),
                "languages": marker_names(line, LANGUAGE_KEYS),
                "scope": marker_names(line, SCOPE_KEYS),
                "os": marker_names(line, OS_KEYS),
                "raw": line,
            }
        )

    return entries


def match_entry(entry: dict[str, object], args: argparse.Namespace) -> bool:
    haystack = " ".join(
        str(entry[key])
        for key in ("name", "category", "description", "languages", "scope", "os")
    ).lower()

    if args.query and not all(term.lower() in haystack for term in args.query):
        return False
    if args.category and args.category.lower() not in str(entry["category"]).lower():
        return False
    if args.official and not entry["official"]:
        return False
    if args.local and "local" not in entry["scope"]:
        return False
    if args.cloud and "cloud" not in entry["scope"]:
        return False
    if args.language and args.language not in entry["languages"]:
        return False
    return True


def print_text(entries: list[dict[str, object]]) -> None:
    for index, entry in enumerate(entries, start=1):
        markers = []
        if entry["official"]:
            markers.append("official")
        markers.extend(entry["languages"])
        markers.extend(entry["scope"])
        markers.extend(entry["os"])
        print(f"{index}. {entry['name']} [{entry['category']}]")
        print(f"   url: {entry['url']}")
        print(f"   markers: {', '.join(markers) if markers else 'none'}")
        print(f"   line: {entry['line']}")
        if entry["description"]:
            print(f"   desc: {entry['description']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Search the installed awesome-mcp-servers README.")
    parser.add_argument("query", nargs="*", help="Search terms. All terms must match.")
    parser.add_argument("--catalog", default=str(DEFAULT_CATALOG_DIR / "README.md"), help="Path to README.md.")
    parser.add_argument("--category", help="Filter by category substring.")
    parser.add_argument("--official", action="store_true", help="Only include official implementations.")
    parser.add_argument("--local", action="store_true", help="Only include local-scope servers.")
    parser.add_argument("--cloud", action="store_true", help="Only include cloud-scope servers.")
    parser.add_argument("--language", choices=LANGUAGE_KEYS, help="Filter by implementation language marker.")
    parser.add_argument("--limit", type=int, default=10, help="Maximum results to print.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text.")
    parser.add_argument("--list-categories", action="store_true", help="Print available categories and exit.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    readme = Path(args.catalog).expanduser()

    if not readme.exists():
        parser.error(f"catalog not found: {readme}")

    entries = parse_catalog(readme)

    if args.list_categories:
        categories = sorted({str(entry["category"]) for entry in entries})
        for category in categories:
            print(category)
        return 0

    matches = [entry for entry in entries if match_entry(entry, args)]
    matches = matches[: max(args.limit, 0)]

    if args.json:
        print(json.dumps(matches, indent=2, ensure_ascii=False))
    else:
        print_text(matches)
        if not matches:
            print("No matching MCP servers found.", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
