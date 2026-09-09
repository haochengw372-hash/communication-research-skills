#!/usr/bin/env python3
"""Institution-gated full-text fetch for screened non-open items.

Requires the user's authenticated institutional network (campus IP or VPN).
This script never stores credentials, never bypasses paywalls or DRM, and
downloads one article at a time with a polite delay. It is the institutional
counterpart of fetch_oa_pdfs.py.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.request
from pathlib import Path


USER_AGENT = "scholarly-access/0.2 (institutional single-item retrieval)"


def safe_name(doi: str) -> str:
    return doi.strip().replace("/", "_").replace("\\", "_")[:160]


def publisher_pdf_url(row: dict) -> str | None:
    """Map a DOI to the publisher's direct PDF endpoint by journal slug."""
    doi = row.get("doi")
    slug = (row.get("journal_slug") or "").lower()
    if not doi:
        return None
    if slug in {"cmm", "dj"}:
        return f"https://www.tandfonline.com/doi/pdf/{doi}?needAccess=true"
    if slug == "nms":
        return f"https://journals.sagepub.com/doi/pdf/{doi}?download=true"
    # Oxford (JoC, JCMC) needs the article landing page to resolve the PDF id.
    return None


def download(url: str, dest: Path) -> tuple[bool, str]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/pdf,*/*"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read(1_048_576 * 60)
            if not data.startswith(b"%PDF"):
                return False, "not-a-pdf"
            if len(data) < 4000:
                return False, "pdf-too-small"
            dest.write_bytes(data)
            return True, "ok"
    except Exception as exc:
        return False, type(exc).__name__


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="screened or pending jsonl")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--delay", type=float, default=2.0)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--only-status", choices=["institution", "auth-required"], default="institution")
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    status_path = args.out / "downloads.jsonl"
    done = {
        line.split("\t", 1)[0]
        for line in (status_path.read_text(encoding="utf-8").splitlines() if status_path.exists() else [])
    }
    rows = [
        json.loads(line)
        for line in args.input.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    downloaded = skipped = failed = 0
    with status_path.open("a", encoding="utf-8") as log:
        for row in rows:
            doi = row.get("doi")
            key = safe_name(doi) if doi else ""
            if not doi or key in done:
                skipped += 1
                continue
            if args.limit and downloaded >= args.limit:
                break
            url = publisher_pdf_url(row)
            if url is None:
                # Oxford-style landing page is out of scope for the direct fetch;
                # record as requiring a session-backed browser step.
                log.write(f"{key}\t{doi}\tlanding-page-required\tneeds-browser\n")
                log.flush()
                done.add(key)
                failed += 1
                continue
            dest = args.out / f"{key}.pdf"
            ok, reason = download(url, dest)
            if not ok and dest.exists():
                dest.unlink()
            log.write(f"{key}\t{doi}\t{url}\t{reason}\n")
            log.flush()
            done.add(key)
            if ok:
                downloaded += 1
            else:
                failed += 1
            time.sleep(args.delay)
    print(f"downloaded={downloaded} skipped_existing={skipped} failed={failed}")
    print(f"status: {status_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
