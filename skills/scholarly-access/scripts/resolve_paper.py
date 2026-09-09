#!/usr/bin/env python3
"""Resolve scholarly full text through the five-layer policy.

This is a dry-run-first scaffold. It performs read-only metadata lookups
(OpenAlex) and classifies each item against the resolver policy. It never
downloads files, never authenticates, and never writes library state.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


OPENALEX_API = "https://api.openalex.org/works/"
USER_AGENT = "scholarly-access-resolver/0.1 (research skill)"
LAYER_LIMIT = 5


@dataclass
class Resolution:
    identifier: str
    doi: str = ""
    title: str = ""
    status: str = "unavailable"
    reason: str = ""
    source: str = ""
    auth_required: bool = False
    candidates: list[str] = field(default_factory=list)


def normalize_doi(value: str) -> str:
    """Return a lower-case bare DOI without URL or scheme prefixes."""
    text = value.strip()
    patterns = (
        r"^https?://(?:dx\.)?doi\.org/",
        r"^doi:\s*",
        r"^https?://doi\.org/",
    )
    for pattern in patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    return text.lower()


def fetch_json(url: str, timeout: int = 15) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def openalex_url(doi: str) -> str:
    encoded = urllib.parse.quote(f"doi:{doi}")
    return OPENALEX_API + encoded


def read_institution_config(path: Path) -> dict[str, Any]:
    """Read the constrained YAML subset used by this repository's adapters."""
    config: dict[str, Any] = {"name": "", "homepage": "", "sso_type": "", "resources": [], "auth_flow": "", "notes": ""}
    current_key: str | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line or line.startswith("#"):
            continue
        if re.match(r"^[A-Za-z_]+:\s*$", line):
            current_key = line[:-1].strip()
            continue
        list_match = re.match(r"^\s*-\s+(.+)$", line)
        if list_match and current_key == "resources":
            config["resources"].append(list_match.group(1).strip())
            continue
        kv = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if kv:
            key, value = kv.groups()
            if key == "resources":
                continue
            config[key] = value.strip().strip("'\"")
            current_key = key
    return config


def classify_from_openalex(
    item_id: str,
    metadata: dict[str, Any],
    *,
    institution: dict[str, Any] | None = None,
    layers: set[int] | None = None,
    offline: bool = False,
) -> Resolution:
    """Pure classifier; tests can call this without any network."""
    layers = layers or set(range(1, LAYER_LIMIT + 1))
    doi = normalize_doi(str(metadata.get("doi") or item_id))
    title = str(metadata.get("title") or "")
    row = Resolution(identifier=item_id, doi=doi, title=title)

    if offline:
        row.reason = "offline: no metadata lookup was performed"
        return row

    locations = metadata.get("locations") or []
    best_oa = metadata.get("best_oa_location") or {}
    pdf_locations: list[dict[str, Any]] = []
    for loc in locations:
        if loc.get("pdf_url"):
            pdf_locations.append(loc)

    if 1 in layers:
        candidate = best_oa if best_oa.get("pdf_url") else next(
            (loc for loc in pdf_locations if loc.get("is_oa")), None
        )
        if candidate and candidate.get("pdf_url"):
            row.status = "oa"
            row.reason = "open-access full text located"
            row.source = candidate["pdf_url"]
            row.candidates = [loc["pdf_url"] for loc in pdf_locations[:5]]
            return row

    if 4 in layers and pdf_locations:
        source = pdf_locations[0]
        row.status = "repository"
        row.reason = "repository or author version located"
        row.source = source["pdf_url"]
        row.candidates = [loc["pdf_url"] for loc in pdf_locations[:5]]
        return row

    if institution and institution.get("resources"):
        delivery_hints = ("delivery", "文献传递", "百链")
        if 5 in layers and any(
            any(hint in str(resource).lower() for hint in delivery_hints)
            for resource in institution["resources"]
        ):
            row.status = "delivery"
            row.reason = "library delivery is the remaining configured route"
            row.auth_required = True
            return row
        if 2 in layers or 3 in layers:
            row.status = "institution"
            row.reason = "institution may hold this item; user authentication is required"
            row.source = str(institution.get("homepage") or "")
            row.auth_required = True
            return row

    row.reason = "no legal full-text route found under current layers and institution"
    return row


def resolve_one(
    item_id: str,
    *,
    fetcher: Callable[[str], dict[str, Any]],
    institution: dict[str, Any] | None,
    layers: set[int],
) -> Resolution:
    try:
        normalized = normalize_doi(item_id)
        metadata = fetcher(openalex_url(normalized)) if normalized else {}
    except Exception as exc:  # network or parse failure is a soft failure here
        metadata = {}
    return classify_from_openalex(
        item_id,
        metadata,
        institution=institution,
        layers=layers,
        offline=not metadata,
    )


def parse_layers(values: list[str]) -> set[int]:
    parsed: set[int] = set()
    for raw in values:
        for part in raw.split(","):
            part = part.strip()
            if not part:
                continue
            if "-" in part:
                start, end = (int(x) for x in part.split("-", 1))
                parsed.update(range(start, end + 1))
            else:
                parsed.add(int(part))
    return parsed & set(range(1, LAYER_LIMIT + 1))


def render_table(rows: list[Resolution]) -> str:
    lines = [
        "DRY RUN: no downloads, no authentication, no library writes.",
        "",
        f"{'identifier':<34} {'status':<13} {'auth':<5} source",
        "-" * 100,
    ]
    for row in rows:
        auth = "yes" if row.auth_required else "-"
        source = row.source or row.reason
        lines.append(f"{row.identifier[:33]:<34} {row.status:<13} {auth:<5} {source}")
    lines.append("")
    lines.append("Summary: " + ", ".join(f"{s}={n}" for s, n in summarize(rows).items()))
    return "\n".join(lines)


def summarize(rows: list[Resolution]) -> dict[str, int]:
    counts = {
        status: 0
        for status in (
            "oa",
            "institution",
            "repository",
            "delivery",
            "unavailable",
            "auth-required",
            "institution-limited",
        )
    }
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1
    return counts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doi", nargs="+", default=[], help="one or more DOIs")
    parser.add_argument("--title", nargs="+", default=[], help="one or more titles used when DOI is missing")
    parser.add_argument(
        "--layers",
        default="1-5",
        help="comma/range list of enabled layers, e.g. 1 or 1,4 or 1-5",
    )
    parser.add_argument("--institution", type=Path, help="path to an institution YAML adapter")
    parser.add_argument("--offline", action="store_true", help="skip all network lookups")
    parser.add_argument(
        "--dry-run",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="default on: metadata only, no downloads or library writes",
    )
    parser.add_argument("--format", choices=("table", "json"), default="table")
    args = parser.parse_args(argv)

    if not args.doi and not args.title:
        parser.error("provide at least one --doi or --title")

    layers = parse_layers([args.layers])
    if not layers:
        parser.error("--layers must include at least one of 1-5")

    institution = read_institution_config(args.institution) if args.institution else None
    identifiers: list[str] = list(args.doi) + list(args.title)
    fetcher: Callable[[str], dict[str, Any]]
    if args.offline:
        fetcher = lambda _url: {}
    else:
        fetcher = fetch_json

    rows = [
        resolve_one(identifier, fetcher=fetcher, institution=institution, layers=layers)
        for identifier in identifiers
    ]

    if args.format == "json":
        payload = {
            "dry_run": args.dry_run,
            "offline": args.offline,
            "layers": sorted(layers),
            "items": [
                {
                    "identifier": row.identifier,
                    "doi": row.doi,
                    "title": row.title,
                    "status": row.status,
                    "reason": row.reason,
                    "source": row.source,
                    "auth_required": row.auth_required,
                    "candidates": row.candidates,
                }
                for row in rows
            ],
            "summary": summarize(rows),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_table(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
