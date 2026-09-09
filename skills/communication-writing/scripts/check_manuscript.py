#!/usr/bin/env python3
"""Run bounded consistency checks on a Markdown manuscript and writing packet."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CLAIM_MARKER = re.compile(r"<!--\s*claim:([A-Za-z0-9_-]+)\s*-->")
NUMBER_MARKER = re.compile(r"<!--\s*number:([A-Za-z0-9_-]+)\s*-->")
PLACEHOLDER = re.compile(
    r"\[(?:CITATION NEEDED|RESULT NEEDED|VERIFY|AUTHOR INPUT NEEDED)\]", re.I
)
SECTION_ALIASES = {
    "introduction": "introduction",
    "background": "introduction",
    "method": "methods",
    "methods": "methods",
    "methodology": "methods",
    "data and methods": "methods",
    "results": "results",
    "findings": "results",
    "analysis": "results",
    "discussion": "discussion",
    "discussion and conclusion": "discussion",
    "conclusion": "conclusion",
    "conclusions": "conclusion",
    "references": "references",
    "bibliography": "references",
}


def load_packet(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("writing packet root must be an object")
    return value


def normalize_section(value: str) -> str:
    value = re.sub(r"^\d+(?:\.\d+)*[.)]?\s+", "", value.strip())
    value = re.sub(r"\s+", " ", value).casefold()
    return SECTION_ALIASES.get(value, value)


def headings(text: str) -> set[str]:
    return {
        normalize_section(match.group(1))
        for match in re.finditer(r"(?m)^#{1,6}\s+(.+?)\s*$", text)
    }


def audit(text: str, packet: dict) -> list[str]:
    errors: list[str] = []
    required_top = {"schema_version", "document_id", "stage", "source_of_truth"}
    for key in sorted(required_top - set(packet)):
        errors.append(f"packet: missing {key}")
    if packet.get("schema_version") != "communication-writing-packet/v1":
        errors.append("packet: unsupported schema_version")
    if packet.get("stage") not in {"outline", "draft", "revision", "final"}:
        errors.append("packet: invalid stage")
    if not packet.get("source_of_truth"):
        errors.append("packet: source_of_truth must not be empty")

    present_headings = headings(text)
    for section in packet.get("required_sections", []):
        if normalize_section(str(section)) not in present_headings:
            errors.append(f"section: missing {section}")

    claim_rows = {str(row.get("id")): row for row in packet.get("claims", [])}
    present_claims = set(CLAIM_MARKER.findall(text))
    for claim_id in sorted(present_claims - set(claim_rows)):
        errors.append(f"claim:{claim_id}: missing from packet")
    for claim_id, row in sorted(claim_rows.items()):
        if row.get("required") and claim_id not in present_claims:
            errors.append(f"claim:{claim_id}: required marker missing")
        if claim_id in present_claims:
            if row.get("status") != "verified":
                errors.append(f"claim:{claim_id}: status is not verified")
            if not row.get("evidence"):
                errors.append(f"claim:{claim_id}: evidence is empty")
            if not row.get("boundary"):
                errors.append(f"claim:{claim_id}: boundary is empty")

    number_rows = {str(row.get("id")): row for row in packet.get("numbers", [])}
    present_numbers = list(NUMBER_MARKER.finditer(text))
    present_number_ids = {match.group(1) for match in present_numbers}
    for number_id in sorted(present_number_ids - set(number_rows)):
        errors.append(f"number:{number_id}: missing from packet")
    for number_id, row in sorted(number_rows.items()):
        if row.get("required") and number_id not in present_number_ids:
            errors.append(f"number:{number_id}: required marker missing")
        if number_id in present_number_ids:
            if not row.get("source"):
                errors.append(f"number:{number_id}: source is empty")
            value = str(row.get("value", ""))
            match = next(m for m in present_numbers if m.group(1) == number_id)
            window = text[max(0, match.start() - 180):match.end() + 180]
            if not value or value not in window:
                errors.append(f"number:{number_id}: locked value not near marker")

    folded = text.casefold()
    for row in packet.get("terms", []):
        canonical = str(row.get("canonical", "")).strip()
        if not canonical:
            errors.append("term: canonical value is empty")
            continue
        for forbidden in row.get("forbidden", []):
            if str(forbidden).casefold() in folded:
                errors.append(f"term:{canonical}: forbidden alias present")

    for index, _ in enumerate(PLACEHOLDER.finditer(text), start=1):
        errors.append(f"placeholder:{index}: unresolved")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    try:
        packet = load_packet(args.packet)
        errors = audit(args.manuscript.read_text(encoding="utf-8"), packet)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2
    if errors:
        print("MANUSCRIPT CHECK FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("MANUSCRIPT CHECK PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
