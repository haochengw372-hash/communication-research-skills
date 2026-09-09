#!/usr/bin/env python3
"""Export screened literature records into Obsidian Markdown notes plus an index."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


JOURNAL_NAMES = {
    "nms": "New Media & Society",
    "dj": "Digital Journalism",
    "jcmc": "Journal of Computer-Mediated Communication",
    "cmm": "Communication Methods and Measures",
    "joc": "Journal of Communication",
}


def yaml_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def slug(text: str, max_words: int = 7) -> str:
    words = re.sub(r"[^\w]+", " ", text).split()
    return "-".join(word.capitalize() for word in words[:max_words])


def filename(row: dict) -> str:
    author = re.sub(r"[^\w]+", "", (row.get("first_author") or "")).strip()
    year = row.get("year") or ""
    title_slug = slug(row.get("title") or "Untitled")
    return f"{author}_{year}_{title_slug}".strip("_")[:180]


def note_text(row: dict) -> str:
    title = row.get("title") or "Untitled"
    journal = JOURNAL_NAMES.get(row.get("journal_slug"), row.get("journal_slug", ""))
    tags = row.get("method_tags") or []
    lines = ["---"]
    lines.append(f"doi: {yaml_string(row.get('doi', ''))}")
    lines.append(f"title: {yaml_string(title)}")
    lines.append(f"journal: {yaml_string(journal)}")
    lines.append(f"year: {row.get('year', '')}")
    lines.append(f"status: {yaml_string(row.get('status', 'included'))}")
    lines.append(f"open_access: {'true' if row.get('open_access') else 'false'}")
    lines.append("method_tags:")
    if tags:
        for tag in tags:
            lines.append(f"  - {yaml_string(str(tag))}")
    else:
        lines.append("  - \"unassigned\"")
    lines.append("---")
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"- DOI: {row.get('doi', '')}")
    lines.append(f"- Journal: {journal}")
    lines.append(f"- Year: {row.get('year', '')}")
    lines.append(f"- First author: {row.get('first_author', '')}")
    lines.append(f"- Open access: {row.get('open_access', '')}")
    if row.get("oa_license"):
        lines.append(f"- License: {row['oa_license']}")
    lines.append("")
    lines.append("## Abstract")
    lines.append("")
    lines.append(row.get("abstract") or "_(abstract not available)_")
    lines.append("")
    lines.append("## Method tags")
    lines.append("")
    lines.append(", ".join(tags) if tags else "_none_")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- [ ] key claim / method")
    lines.append("- [ ] relevance to my work")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="screened jsonl")
    parser.add_argument("--obsidian", type=Path, required=True)
    args = parser.parse_args()

    args.obsidian.mkdir(parents=True, exist_ok=True)
    rows = [json.loads(line) for line in args.input.read_text(encoding="utf-8").splitlines() if line.strip()]
    written = 0
    skipped = 0
    index_rows = []

    for row in rows:
        name = filename(row)
        path = args.obsidian / f"{name}.md"
        if path.exists():
            skipped += 1
            index_rows.append((name, row))
            continue
        path.write_text(note_text(row), encoding="utf-8")
        written += 1
        index_rows.append((name, row))

    by_journal: dict[str, list[tuple[str, dict]]] = {}
    for name, row in index_rows:
        by_journal.setdefault(row.get("journal_slug", "other"), []).append((name, row))

    index = ["# 计算传播文献索引", ""]
    for journal, entries in sorted(by_journal.items()):
        display = JOURNAL_NAMES.get(journal, journal)
        index.append(f"## {display}")
        index.append("")
        entries.sort(key=lambda pair: (pair[1].get("year") or "", pair[0].lower()))
        for name, row in entries:
            tags = "; ".join(row.get("method_tags") or [])
            index.append(f"- [[{name}]] — {row.get('title', '')} ({tags})")
        index.append("")

    (args.obsidian / "_INDEX.md").write_text("\n".join(index), encoding="utf-8")
    print(f"written={written} skipped_existing={skipped}")
    print(f"index: {args.obsidian / '_INDEX.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
