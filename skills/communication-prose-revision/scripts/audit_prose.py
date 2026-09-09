#!/usr/bin/env python3
"""Flag formulaic and defensive academic prose without predicting authorship."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


PATTERNS = {
    "FORMULAIC_OPENING": re.compile(
        r"\b(?:in recent years|in today'?s .{0,25}landscape|with the rapid "
        r"development of|随着.{0,12}(?:发展|进步))\b",
        re.I,
    ),
    "EMPTY_METADISCOURSE": re.compile(
        r"(?:\b(?:it is (?:important|worthwhile|necessary) to (?:note|mention)|"
        r"it should be noted|needless to say)\b|值得注意的是|有必要指出)",
        re.I,
    ),
    "VAGUE_CONTRIBUTION": re.compile(
        r"(?:\b(?:shed(?:s|ding)? light on|provide(?:s|d)? valuable insights?|"
        r"bridge(?:s|d)? the gap|pav(?:e|es|ed|ing) the way)\b|"
        r"具有(?:重要|重大)(?:理论|实践|现实)?意义|提供了?有益启示)",
        re.I,
    ),
    "ANONYMOUS_AUTHORITY": re.compile(
        r"(?:\bit is (?:widely )?(?:believed|considered|argued|recognized)\b|"
        r"普遍认为|有研究认为)",
        re.I,
    ),
    "STACKED_HEDGE": re.compile(
        r"\b(?:may|might|could|perhaps|possibly|potentially|seem(?:s|ed)?|"
        r"appear(?:s|ed)?|suggest(?:s|ed)?)\b(?:\W+\w+){0,5}\W+\b"
        r"(?:may|might|could|perhaps|possibly|potentially|seem(?:s|ed)?|"
        r"appear(?:s|ed)?|suggest(?:s|ed)?)\b",
        re.I,
    ),
    "GENERIC_CAUTION": re.compile(
        r"(?:\b(?:should be interpreted with caution|results? must be treated with caution)\b|"
        r"谨慎解释|谨慎对待)",
        re.I,
    ),
    "MECHANICAL_TRANSITION": re.compile(
        r"^\s*(?:moreover|furthermore|additionally|in addition|此外|另外|进一步而言)[,，]",
        re.I,
    ),
}


def audit(text: str) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for number, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith(("#", "```", "|")):
            continue
        for code, pattern in PATTERNS.items():
            if pattern.search(line):
                findings.append({"line": number, "code": code})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        text = args.manuscript.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: {exc}")
        return 2
    findings = audit(text)
    counts = Counter(str(item["code"]) for item in findings)
    if args.as_json:
        print(json.dumps({"findings": findings, "counts": dict(counts)}, indent=2))
    else:
        print("PROSE DIAGNOSTIC — review candidates, not authorship predictions")
        for item in findings:
            print(f"L{item['line']} {item['code']}")
        print("counts:", " ".join(f"{key}={value}" for key, value in sorted(counts.items())) or "none")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
