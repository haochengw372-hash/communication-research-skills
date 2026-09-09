#!/usr/bin/env python3
"""Enumerate journal articles in a date window from OpenAlex, cross-checked with Crossref.

Produces enriched.jsonl, metadata.csv, and counts.json without downloading full text.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path


OPENALEX = "https://api.openalex.org/works"
CROSSREF_JOURNAL = "https://api.crossref.org/journals/{issn}/works"
USER_AGENT = "scholarly-access/0.2 (research corpus enumerator)"


def get_json(url: str, timeout: int = 30) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def bare_doi(value: str) -> str:
    if not value:
        return ""
    text = value.strip()
    text = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", text, flags=re.I)
    text = re.sub(r"^doi:\s*", "", text, flags=re.I)
    return text.lower()


def abstract_from_inverted_index(index: dict | None) -> str:
    if not index:
        return ""
    positions: dict[int, str] = {}
    for word, positions_list in index.items():
        for position in positions_list:
            positions[position] = word
    return " ".join(positions[i] for i in sorted(positions))


def enrich(work: dict, slug: str) -> dict:
    best_oa = work.get("best_oa_location") or {}
    locations = work.get("locations") or []
    oa_urls = []
    oa_licenses = []
    for loc in locations:
        if loc.get("pdf_url"):
            oa_urls.append(loc["pdf_url"])
            if loc.get("license"):
                oa_licenses.append(loc["license"])
    if best_oa.get("pdf_url") and best_oa["pdf_url"] not in oa_urls:
        oa_urls.insert(0, best_oa["pdf_url"])

    concepts = [c.get("display_name") for c in (work.get("concepts") or [])[:3]]
    authors = [
        (item.get("author") or {}).get("display_name", "")
        for item in (work.get("authorships") or [])
        if item.get("author")
    ]
    first_author = authors[0] if authors else ""
    doi = bare_doi(work.get("doi") or "")
    open_access_obj = work.get("open_access") or {}
    is_oa = bool(open_access_obj.get("is_oa"))
    publication_date = work.get("publication_date") or ""
    return {
        "doi": doi,
        "title": (work.get("title") or "").strip(),
        "journal_slug": slug,
        "publication_date": publication_date,
        "year": publication_date[:4] if publication_date else "",
        "type": work.get("type") or "",
        "open_access": is_oa,
        "oa_url": best_oa.get("pdf_url") or "",
        "oa_license": best_oa.get("license") or "",
        "oa_urls": oa_urls[:5],
        "oa_licenses": oa_licenses[:5],
        "abstract": abstract_from_inverted_index(work.get("abstract_inverted_index")),
        "concepts": concepts,
        "cited_by_count": work.get("cited_by_count") or 0,
        "authors": authors,
        "first_author": first_author,
    }


def openalex_works(issn: str, date_from: str, date_to: str, email: str | None) -> list[dict]:
    items: list[dict] = []
    cursor = "*"
    while True:
        params = {
            "filter": f"primary_location.source.issn:{issn},from_publication_date:{date_from},to_publication_date:{date_to}",
            "per-page": "200",
            "cursor": cursor,
        }
        if email:
            params["mailto"] = email
        url = OPENALEX + "?" + urllib.parse.urlencode(params)
        data = get_json(url)
        items.extend(data.get("results", []))
        cursor = data.get("meta", {}).get("next_cursor")
        if not cursor:
            break
        time.sleep(0.15)
    return items


def crossref_total(issn: str, date_from: str, date_to: str) -> int | None:
    url = (
        CROSSREF_JOURNAL.format(issn=issn)
        + "?rows=0&filter="
        + urllib.parse.quote(f"from-pub-date:{date_from},until-pub-date:{date_to}")
    )
    data = get_json(url, timeout=30)
    total = data.get("message", {}).get("total-results")
    return int(total) if total is not None else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--journals", type=Path, required=True, help="JSON mapping slug -> ISSN list")
    parser.add_argument("--from", dest="date_from", required=True)
    parser.add_argument("--to", dest="date_to", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--email", default=None, help="optional OpenAlex polite-pool email")
    args = parser.parse_args()

    journals = json.loads(args.journals.read_text(encoding="utf-8"))
    args.out.mkdir(parents=True, exist_ok=True)

    enriched_path = args.out / "enriched.jsonl"
    csv_path = args.out / "metadata.csv"
    counts: dict[str, dict] = {}
    seen_dois: set[str] = set()
    seen_titles: set[str] = set()

    with enriched_path.open("w", encoding="utf-8") as fh:
        for slug, issns in journals.items():
            items: dict[str, dict] = {}
            for issn in issns:
                for work in openalex_works(issn, args.date_from, args.date_to, args.email):
                    row = enrich(work, slug)
                    if row["doi"]:
                        if row["doi"] in seen_dois:
                            continue
                        seen_dois.add(row["doi"])
                        items[row["doi"]] = row
                        if row["title"]:
                            seen_titles.add(re.sub(r"\W+", " ", row["title"].lower()).strip())
                    elif row["title"]:
                        key = "t:" + re.sub(r"\W+", " ", row["title"].lower()).strip()
                        if key in seen_titles:
                            continue
                        seen_titles.add(key)
                        items[key] = row

            crossref = {}
            for issn in issns:
                try:
                    crossref[issn] = crossref_total(issn, args.date_from, args.date_to)
                except Exception as exc:
                    crossref[issn] = f"error: {type(exc).__name__}"

            for row in items.values():
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            counts[slug] = {"openalex_dedup": len(items), "crossref": crossref}

    fieldnames = [
        "doi", "title", "journal_slug", "year", "publication_date", "type",
        "open_access", "oa_url", "oa_license", "abstract_available",
        "concepts", "cited_by_count",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        with enriched_path.open(encoding="utf-8") as read:
            for line in read:
                row = json.loads(line)
                writer.writerow({
                    "doi": row["doi"],
                    "title": row["title"],
                    "journal_slug": row["journal_slug"],
                    "year": row["year"],
                    "publication_date": row["publication_date"],
                    "type": row["type"],
                    "open_access": row["open_access"],
                    "oa_url": row["oa_url"],
                    "oa_license": row["oa_license"],
                    "abstract_available": "1" if row["abstract"] else "0",
                    "concepts": "; ".join(row["concepts"]),
                    "cited_by_count": row["cited_by_count"],
                })

    (args.out / "counts.json").write_text(
        json.dumps(counts, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"enriched: {enriched_path}")
    print(f"csv: {csv_path}")
    print(f"counts: {args.out / 'counts.json'}")
    print(json.dumps({k: v["openalex_dedup"] for k, v in counts.items()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
