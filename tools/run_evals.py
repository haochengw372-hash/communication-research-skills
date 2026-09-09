#!/usr/bin/env python3
"""Run deterministic repository checks and emit a compact JSON report."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(name: str, command: list[str]) -> dict[str, object]:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return {
        "name": name,
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def main() -> int:
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "checks": [
            run(
                "unittest",
                [sys.executable, "-m", "unittest", "discover", "-s", "evals", "-p", "test_*.py", "-v"],
            ),
            run(
                "scholarly-access-unittest",
                [sys.executable, str(ROOT / "skills" / "scholarly-access" / "scripts" / "test_resolve_paper.py")],
            ),
            run("security_audit", [sys.executable, "tools/security_audit.py"]),
            run("privacy_audit", [sys.executable, "tools/privacy_audit.py"]),
        ],
    }
    failed = [item for item in report["checks"] if item["returncode"] != 0]
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"checks: {len(report['checks'])}; failed: {len(failed)}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
