#!/usr/bin/env python3
"""Validate a Codex research project control layer without modifying it."""
from __future__ import annotations
import argparse, json, posixpath
from pathlib import Path

ACTIVE_STATUSES = {"ready", "in-progress", "blocked", "needs-decision", "needs-audit", "revision", "stale"}
ALLOWED_STATUSES = ACTIVE_STATUSES | {"planned", "draft", "completed", "cancelled"}

def load(path): return json.loads(path.read_text(encoding="utf-8-sig"))
def within(scope,prefix): return scope==prefix or scope.startswith(prefix+"/")
def cycles(graph):
    visiting=set(); done=set()
    def visit(node):
        if node in visiting: return True
        if node in done: return False
        visiting.add(node)
        for dep in graph.get(node, []):
            if dep in graph and visit(dep): return True
        visiting.remove(node); done.add(node); return False
    return any(visit(n) for n in graph)
def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("project_root",type=Path); a=p.parse_args(argv); c=a.project_root.resolve()/".codex-research"; errors=[]
    required=[c/n for n in ("project.yaml","state.yaml","windows.yaml","decisions.md","contracts","handoffs","audits","snapshots")]
    for x in required:
        if not x.exists(): errors.append(f"missing: {x}")
    if not errors:
        try: project,state,windows=load(c/"project.yaml"),load(c/"state.yaml"),load(c/"windows.yaml")
        except (OSError,json.JSONDecodeError) as e: errors.append(f"invalid JSON-compatible YAML: {e}")
        else:
            if project.get("project_id")!=state.get("project_id") or project.get("project_id")!=windows.get("project_id"): errors.append("project_id mismatch")
            if not isinstance(state.get("revision"),int): errors.append("revision must be integer")
            elif state.get("revision") < 0: errors.append("revision must be non-negative")
            if state.get("updated_by") != "controller": errors.append("updated_by must be controller")
            roles=windows.get("roles",{})
            if set(roles)!={"controller","prompt","executor","auditor"}: errors.append("windows must define four roles")
            if roles.get("controller",{}).get("instances")!=1: errors.append("controller instances must equal 1")
            expected_writes={"controller":{"state.yaml","contracts/","decisions.md","snapshots/"},"prompt":{"handoffs/"},"executor":{"contract-authorized artifacts","handoffs/"},"auditor":{"audits/","handoffs/"}}
            for role, expected in expected_writes.items():
                if set(roles.get(role,{}).get("writes",[])) != expected: errors.append(f"role permission mismatch: {role}")
            packages=state.get("work_packages",{})
            graph={k:v.get("depends_on",[]) for k,v in packages.items() if isinstance(v,dict)}
            for task_id, package in packages.items():
                if not isinstance(package, dict):
                    errors.append(f"invalid work package: {task_id}")
                    continue
                if package.get("status") not in ALLOWED_STATUSES:
                    errors.append(f"invalid status for {task_id}: {package.get('status')}")
                role=package.get("assigned_role")
                if role not in {"controller","prompt","executor","auditor"}:
                    errors.append(f"invalid assigned role for {task_id}: {role}")
                if package.get("status") in ACTIVE_STATUSES and role != "controller" and not package.get("write_scope"):
                    errors.append(f"active package requires non-empty write_scope: {task_id}")
                normalized_scopes=[posixpath.normpath(str(x).replace("\\","/").strip("/")).casefold() for x in package.get("write_scope",[]) if str(x).strip()]
                governance_prefixes=(".codex-research/project.yaml",".codex-research/state.yaml",".codex-research/windows.yaml",".codex-research/contracts",".codex-research/decisions.md",".codex-research/snapshots")
                if role in {"prompt","executor","auditor"} and any(x.startswith(governance_prefixes) for x in normalized_scopes): errors.append(f"write scope violates role {role}: {task_id}")
                if role=="prompt" and any(not within(x,".codex-research/handoffs") for x in normalized_scopes): errors.append(f"write scope violates role prompt: {task_id}")
                if role=="auditor" and any(not (within(x,".codex-research/audits") or within(x,".codex-research/handoffs")) for x in normalized_scopes): errors.append(f"write scope violates role auditor: {task_id}")
                for dependency in package.get("depends_on", []):
                    if dependency not in packages:
                        errors.append(f"unknown dependency for {task_id}: {dependency}")
                    elif package.get("status") in {"ready","in-progress","needs-audit","completed"} and packages.get(dependency,{}).get("status") != "completed":
                        errors.append(f"dependency not completed for {task_id}: {dependency}")
                if package.get("status") == "completed":
                    verification=package.get("latest_verification")
                    if not isinstance(verification,dict) or not verification.get("command") or not verification.get("result"):
                        errors.append(f"completed package requires latest verification: {task_id}")
                    if package.get("audit_required") and package.get("audit_verdict") not in {"pass","pass-with-minor"}:
                        errors.append(f"completed audited package requires passing audit verdict: {task_id}")
            active_scopes=[]
            for task_id, package in packages.items():
                if not isinstance(package, dict) or package.get("status") not in ACTIVE_STATUSES:
                    continue
                for scope in package.get("write_scope", []):
                    normalized=posixpath.normpath(str(scope).replace("\\", "/").strip("/")).casefold()
                    if normalized:
                        active_scopes.append((task_id, normalized))
            for index, (left_id, left_scope) in enumerate(active_scopes):
                for right_id, right_scope in active_scopes[index + 1:]:
                    if left_id == right_id:
                        continue
                    if left_scope == right_scope or left_scope.startswith(right_scope + "/") or right_scope.startswith(left_scope + "/"):
                        errors.append(f"overlapping write scope: {left_id}={left_scope}, {right_id}={right_scope}")
            if cycles(graph): errors.append("dependency cycle detected")
    if errors:
        print("INVALID"); [print(f"- {e}") for e in errors]; return 1
    print("VALID: Codex research project control layer"); return 0
if __name__=="__main__": raise SystemExit(main())
