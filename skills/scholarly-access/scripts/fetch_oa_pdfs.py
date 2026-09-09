#!/usr/bin/env python3
"""Download and validate open-access PDFs from an enriched metadata file.

Polite by default: one request at a time, small delay, skip existing files.
Records the license and a per-item status without ever using credentials.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.request
from pathlib import Path


USER_AGENT = "scholarly-access/0.2 (research corpus fetcher)"


def safe_name(doi: str) -> str:
    text = doi.strip().replace("/", "_").replace("\\", "_")
    for ch in ' :?*"<>|':
        text = text.replace(ch, "_")
    return text[:160]


def download(url: str, dest: Path) -> tuple[bool, str]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/pdf,*/*"},
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = resp.read(1_048_576 * 40)  # cap at 40 MiB in memory
            if not data.startswith(b"%PDF"):
                return False, "not-a-pdf"
            if len(data) < 4000:
                return False, "pdf-too-small"
            dest.write_bytes(data)
            return True, "ok"
    except Exception as exc:
        return False, f"{type(exc).__name__}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="enriched or screened jsonl")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--delay", type=float, default=1.0)
    parser.add_argument("--limit", type=int, default=0, help="max downloads; 0 = no limit")
    parser.add_argument("--overwrite", action="store_true", help="retry previously recorded items")
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    status_path = args.out / "downloads.jsonl"
    done = set() if args.overwrite else {
        line.split("\t", 1)[0]
        for line in (status_path.read_text(encoding="utf-8").splitlines() if status_path.exists() else [])
    }

    rows = [json.loads(line) for line in args.input.read_text(encoding="utf-8").splitlines() if line.strip()]
    downloaded = 0
    skipped = 0
    failed = 0

    mode = "w" if args.overwrite else "a"
    with status_path.open(mode, encoding="utf-8") as log:
        for row in rows:
            doi = row.get("doi")
            candidates = []
            for candidate in [row.get("oa_url")] + (row.get("oa_urls") or []):
                if candidate and candidate not in candidates:
                    candidates.append(candidate)
            if not doi or not candidates:
                continue
            key = safe_name(doi)
            if key in done:
                skipped += 1
                continue
            if args.limit and downloaded >= args.limit:
                break

            dest = args.out / f"{key}.pdf"
            ok, reason = False, "no-candidate-succeeded"
            for url in candidates:
                ok, reason = download(url, dest)
                if ok:
                    break
                if dest.exists():
                    dest.unlink()
            log.write(f"{key}\t{doi}\t{candidates[0]}\t{reason}\n")
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
