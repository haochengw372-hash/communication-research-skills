#!/usr/bin/env python3
"""Static security audit for the installable skill package."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "skills"
TEXT_EXTENSIONS = {".md", ".py", ".yaml", ".yml", ".json", ".txt"}
PATTERNS = {
    "credential access": r"(?i)(\.ssh|\.aws|auth\.json|browser cookies|credential files)",
    "dynamic execution": r"(?i)\b(eval|exec)\s*\(",
    "obfuscation": r"(?i)(base64\.b64decode|frombase64string)",
    "network execution": r"(?i)\b(curl|wget)\b.*https?://",
    "privilege escalation": r"(?i)\b(sudo|runas)\b",
}
ALLOWLIST = {
    ("communication-research-workflow/references/skill-registry.md", "credential access"),
}


def main() -> int:
    findings: list[str] = []
    reviewed = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        reviewed += 1
        relative = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8-sig")
        for label, pattern in PATTERNS.items():
            if (relative, label) in ALLOWLIST:
                continue
            for match in re.finditer(pattern, text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append(f"{relative}:{line}: {label}: {match.group(0)}")
    print(f"files reviewed: {reviewed}")
    if findings:
        print("SECURITY AUDIT FAILED")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("SECURITY AUDIT PASSED: no credential, obfuscation, dynamic execution, network-execution, or privilege-escalation patterns")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
