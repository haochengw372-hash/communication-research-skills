#!/usr/bin/env python3
"""Validate a codex-research-workflow task contract in JSON or simple YAML."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:  # The documented flat subset remains dependency-free.
    yaml = None


REQUIRED = (
    "task_type", "goal", "operation", "rigor", "authority", "source_of_truth",
    "materials", "deliverables", "quality_gates", "constraints",
    "stop_conditions", "uncertainties",
)
TASK_TYPES = {
    "research-question", "literature-review", "scientometrics-network",
    "data-audit", "empirical-analysis", "research-code",
    "computational-content-analysis", "network-analysis", "causal-inference",
    "temporal-analysis", "multimodal-analysis", "spatial-analysis",
    "simulation-study", "experiment-survey",
    "qualitative-analysis", "mixed-methods",
    "research-visualization", "writing-revision", "manuscript-review",
    "journal-fit", "citation-finalization", "project-continuation", "project-governance",
}
OPERATIONS = {"diagnose", "plan", "execute", "review", "full-pipeline"}
RIGOR_LEVELS = {"quick", "standard", "audit"}
AUTHORITIES = {"read-only", "edit-existing", "create-new"}
LIST_FIELDS = {
    "materials", "deliverables", "quality_gates", "constraints",
    "stop_conditions", "uncertainties", "input_artifacts",
}
PROJECT_FIELDS = {
    "schema_version", "project_id", "task_id", "target_role", "state_revision",
    "contract_version", "input_artifacts", "return_handoff",
}
PROJECT_REQUIRED = PROJECT_FIELDS - {"schema_version"}
ROLES = {"controller", "prompt", "executor", "auditor"}


def scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value[0:1] in {'"', "'"} and value[-1:] == value[0]:
        return value[1:-1]
    if value.startswith(("[", "{")):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none", "~"}:
        return None
    try:
        return int(value)
    except ValueError:
        pass
    return value


def parse_simple_yaml(text: str) -> dict[str, Any]:
    """Parse the flat mapping/list subset used by the documented contract."""
    result: dict[str, Any] = {}
    current: str | None = None
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        stripped = line.strip()
        if stripped.startswith("- "):
            if current is None or not isinstance(result.get(current), list):
                raise ValueError(f"line {number}: list item has no list field")
            result[current].append(scalar(stripped[2:]))
            continue
        if line[:1].isspace():
            raise ValueError(
                f"line {number}: nested YAML mappings are not supported; "
                "use a scalar, JSON object, or JSON input"
            )
        if ":" not in line:
            raise ValueError(f"line {number}: expected 'key: value'")
        key, value = line.split(":", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"line {number}: empty key")
        current = key
        result[key] = scalar(value) if value.strip() else ([] if key in LIST_FIELDS else "")
    return result


def load_contract(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8-sig")
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        if yaml is not None:
            try:
                value = yaml.safe_load(text)
            except yaml.YAMLError as exc:
                raise ValueError(f"invalid YAML: {exc}") from exc
        else:
            value = parse_simple_yaml(text)
    if not isinstance(value, dict):
        raise ValueError("contract root must be an object/mapping")
    return value


def validate(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in LIST_FIELDS:
        if field in contract and contract[field] is None:
            contract[field] = []
    for field in REQUIRED:
        if field not in contract:
            errors.append(f"missing required field: {field}")
    if contract.get("task_type") not in TASK_TYPES:
        errors.append("task_type must be one of: " + ", ".join(sorted(TASK_TYPES)))
    if contract.get("operation") not in OPERATIONS:
        errors.append("operation must be one of: " + ", ".join(sorted(OPERATIONS)))
    if contract.get("rigor") not in RIGOR_LEVELS:
        errors.append("rigor must be one of: " + ", ".join(sorted(RIGOR_LEVELS)))
    if contract.get("authority") not in AUTHORITIES:
        errors.append("authority must be one of: " + ", ".join(sorted(AUTHORITIES)))
    if contract.get("operation") in {"review", "diagnose"} and contract.get("authority") != "read-only":
        errors.append("review and diagnose operations require authority=read-only")
    if contract.get("operation") in {"execute", "full-pipeline"} and contract.get("authority") == "read-only":
        errors.append("execute and full-pipeline operations require write authority")
    if contract.get("schema_version") == "codex-research-contract/v1":
        for field in sorted(PROJECT_REQUIRED):
            if field not in contract:
                errors.append(f"missing required project field: {field}")
        if contract.get("target_role") not in ROLES:
            errors.append("target_role must be one of: " + ", ".join(sorted(ROLES)))
        role = contract.get("target_role")
        if role == "prompt" and not (contract.get("operation") in {"plan", "diagnose"} and contract.get("authority") == "read-only"):
            errors.append("role matrix: prompt requires plan/diagnose with read-only authority")
        if role == "auditor" and not (contract.get("operation") == "review" and contract.get("rigor") == "audit" and contract.get("authority") == "read-only"):
            errors.append("role matrix: auditor requires review/audit/read-only")
        if not isinstance(contract.get("state_revision"), int) or isinstance(contract.get("state_revision"), bool):
            errors.append("state_revision must be an integer")
        elif contract.get("state_revision") < 0:
            errors.append("state_revision must be non-negative")
        if not isinstance(contract.get("contract_version"), int) or isinstance(contract.get("contract_version"), bool):
            errors.append("contract_version must be an integer")
        elif contract.get("contract_version") < 1:
            errors.append("contract_version must be positive")
        if not isinstance(contract.get("return_handoff"), bool):
            errors.append("return_handoff must be boolean")
        governed = ".codex-research/project.yaml .codex-research/state.yaml .codex-research/windows.yaml .codex-research/contracts .codex-research/decisions.md .codex-research/snapshots"
        delivery_text = " ".join(str(item) for item in contract.get("deliverables", []))
        if contract.get("target_role") != "controller" and any(token in delivery_text for token in governed.split()):
            errors.append("controller-only governance files cannot be deliverables for this role")
    for field in LIST_FIELDS:
        if field in contract and not isinstance(contract[field], list):
            errors.append(f"{field} must be a list")
    for field in ("goal", "source_of_truth"):
        if field in contract and contract[field] in (None, "", [], {}):
            errors.append(f"{field} must not be empty; use 'to-be-verified' if unresolved")
    allowed = set(REQUIRED) | (PROJECT_FIELDS if contract.get("schema_version") == "codex-research-contract/v1" else set())
    unknown = sorted(set(contract) - allowed)
    if unknown:
        errors.append("unknown fields: " + ", ".join(unknown))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", type=Path, help="JSON or simple YAML contract")
    args = parser.parse_args(argv)
    try:
        contract = load_contract(args.contract)
        errors = validate(contract)
    except (OSError, ValueError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 2
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALID: codex-research-workflow task contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
