#!/usr/bin/env python3
"""Validate handoff structure, revision, contract, and artifact hashes."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
def load(p): return json.loads(p.read_text(encoding="utf-8-sig"))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def content_sha(value):
    clean=dict(value); clean.pop("handoff_content_sha256",None)
    return hashlib.sha256(json.dumps(clean,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()
def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("project_root",type=Path); p.add_argument("handoff",type=Path); a=p.parse_args(argv); root=a.project_root.resolve(); errors=[]
    try: h=load(a.handoff); state=load(root/".codex-research"/"state.yaml")
    except (OSError,json.JSONDecodeError) as e: print(f"INVALID: {e}"); return 2
    req=("schema_version","handoff_id","project_id","task_id","sender_role","state_revision_read","contract_path","contract_sha256","status","artifacts")
    for k in req:
        if k not in h: errors.append(f"missing field: {k}")
    if h.get("schema_version")!="codex-research-handoff/v1": errors.append("invalid schema_version")
    if h.get("status") not in {"completed","partial","blocked","needs-decision","stale"}: errors.append("invalid status")
    if h.get("handoff_content_sha256") != content_sha(h): errors.append("handoff content hash mismatch")
    if a.handoff.stem != h.get("handoff_id"): errors.append("handoff_id must match filename")
    cp=root/h.get("contract_path",""); contract=None
    if not cp.is_file(): errors.append("contract not found")
    elif sha(cp)!=h.get("contract_sha256"): errors.append("contract hash mismatch")
    else:
        try: contract=load(cp)
        except (OSError,json.JSONDecodeError) as e: errors.append(f"invalid contract: {e}")
    if h.get("project_id") != state.get("project_id"): errors.append("project_id mismatch")
    if contract is not None:
        if h.get("project_id") != contract.get("project_id"): errors.append("contract project_id mismatch")
        if h.get("task_id") != contract.get("task_id"): errors.append("task_id mismatch")
        if h.get("sender_role") != contract.get("target_role"): errors.append("sender role mismatch")
        if h.get("state_revision_read") != contract.get("state_revision"): errors.append("state revision mismatch with contract")
    for item in h.get("artifacts",[]):
        ap=root/item.get("path","")
        if not ap.is_file(): errors.append(f"artifact not found: {item.get('path')}")
        elif sha(ap)!=item.get("sha256"): errors.append(f"artifact hash mismatch: {item.get('path')}")
        verification=item.get("verification",{})
        if not verification.get("command") or not verification.get("result"): errors.append(f"artifact verification missing: {item.get('path')}")
    paths=[str(x.get("path","")).replace("\\","/") for x in h.get("artifacts",[])]
    if h.get("sender_role")!="controller" and any(x.startswith((".codex-research/project.yaml",".codex-research/state.yaml",".codex-research/windows.yaml",".codex-research/contracts/",".codex-research/decisions.md",".codex-research/snapshots/")) for x in paths): errors.append("controller-only artifact")
    if h.get("sender_role")=="prompt" and any(not x.startswith(".codex-research/handoffs/") for x in paths): errors.append("prompt role artifact scope violation")
    if h.get("sender_role")=="auditor" and any(not x.startswith((".codex-research/audits/",".codex-research/handoffs/")) for x in paths): errors.append("auditor artifact scope violation")
    if h.get("status")=="stale" and paths: errors.append("stale handoff cannot include artifacts")
    if h.get("state_revision_read")!=state.get("revision") and h.get("status")!="stale": errors.append("stale state revision must use status=stale")
    if h.get("sender_role")=="auditor" and h.get("verdict") not in {"pass","pass-with-minor","revise","block"}: errors.append("auditor verdict missing")
    if h.get("status")=="completed":
        if h.get("sender_role")=="executor" and not h.get("artifacts"): errors.append("completed executor handoff requires artifacts")
        if h.get("sender_role")=="auditor" and not any(x.startswith(".codex-research/audits/") for x in paths): errors.append("completed auditor handoff requires audit report")
        if not h.get("quality_gates"): errors.append("completed handoff requires quality gates")
        fresh=h.get("fresh_verification",{})
        if not fresh.get("command") or not fresh.get("result"): errors.append("completed handoff requires fresh verification")
    if errors: print("INVALID"); [print(f"- {e}") for e in errors]; return 1
    print("VALID: Codex research handoff"); return 0
if __name__=="__main__": raise SystemExit(main())
