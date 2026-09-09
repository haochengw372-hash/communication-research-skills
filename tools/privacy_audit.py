#!/usr/bin/env python3
"""Detect generic personal, credential, and local-path exposure in a public release."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".txt", ".cff"}
PATTERNS = {
    "absolute local path": r"(?i)(?:\b[A-Z]:[\\/][^\r\n`<>|]+|/(?:home|Users)/[^/\s]+)",
    "email address": r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
    "credential assignment": r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[\"']?[^\s\"']+",
    "private key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
}
ALLOWLIST = {
    ("README.md", "credential assignment"),
    ("README.zh-CN.md", "credential assignment"),
    ("skills/communication-research-workflow/references/profile-and-preferences.md", "credential assignment"),
    ("skills/communication-research-workflow/references/skill-registry.md", "credential assignment"),
}


def generic_matches(text: str):
    for label, pattern in PATTERNS.items():
        for match in re.finditer(pattern, text):
            yield label, match


def main() -> int:
    findings = []
    reviewed = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts or ".omx" in path.parts or "__pycache__" in path.parts:
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"LICENSE", "VERSION", ".gitignore"}:
            continue
        reviewed += 1
        relative = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for label, match in generic_matches(text):
            if (relative, label) in ALLOWLIST:
                continue
            line = text.count("\n", 0, match.start()) + 1
            findings.append(f"{relative}:{line}: {label}")
    print(f"files reviewed: {reviewed}")
    if findings:
        print("PRIVACY AUDIT FAILED")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("PRIVACY AUDIT PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
