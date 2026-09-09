#!/usr/bin/env python3
"""Create a unique, hash-grounded Codex research handoff package."""
from __future__ import annotations
import argparse, hashlib, json, secrets, sys
from datetime import datetime, timezone
from pathlib import Path

def load(p): return json.loads(p.read_text(encoding="utf-8-sig"))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def content_sha(value):
    clean=dict(value); clean.pop("handoff_content_sha256",None)
    return hashlib.sha256(json.dumps(clean,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()
def rel(p,root):
    try: return p.resolve().relative_to(root.resolve()).as_posix()
    except ValueError: return str(p.resolve())
def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("project_root",type=Path); p.add_argument("--task-id",required=True); p.add_argument("--role",choices=("prompt","executor","auditor"),required=True); p.add_argument("--status",choices=("completed","partial","blocked","needs-decision","stale"),required=True); p.add_argument("--contract",type=Path,required=True); p.add_argument("--artifact",type=Path,action="append",default=[]); p.add_argument("--verification-command",default=""); p.add_argument("--verification-result",default=""); p.add_argument("--quality-gate",action="append",default=[]); p.add_argument("--verdict",choices=("pass","pass-with-minor","revise","block")); p.add_argument("--recommended-next-action",default="") ; a=p.parse_args(argv)
    root=a.project_root.resolve(); c=root/".codex-research"; contract_path=a.contract.resolve()
    try: contract_path.relative_to((c/"contracts").resolve())
    except ValueError:
        print("contract must be inside .codex-research/contracts directory", file=sys.stderr); return 2
    state=load(c/"state.yaml"); contract=load(contract_path)
    if a.role=="auditor" and not a.verdict: print("auditor handoff requires --verdict",file=sys.stderr); return 2
    if contract.get("project_id") != state.get("project_id"):
        print("project_id mismatch between contract and state", file=sys.stderr); return 2
    if contract.get("task_id") != a.task_id:
        print("task_id mismatch between arguments and contract", file=sys.stderr); return 2
    if contract.get("target_role") != a.role:
        print("role mismatch between arguments and contract", file=sys.stderr); return 2
    for x in a.artifact:
        rp=rel(x,root)
        if rp.startswith((".codex-research/project.yaml",".codex-research/state.yaml",".codex-research/windows.yaml",".codex-research/contracts/",".codex-research/decisions.md",".codex-research/snapshots/")): print("controller-only governance artifact",file=sys.stderr); return 2
        if a.role=="prompt" and not rp.startswith(".codex-research/handoffs/"): print("prompt role cannot return research artifacts",file=sys.stderr); return 2
        if a.role=="auditor" and not rp.startswith((".codex-research/audits/",".codex-research/handoffs/")): print("auditor role may return only audit artifacts",file=sys.stderr); return 2
        if not x.is_file(): print(f"artifact not found: {x}",file=sys.stderr); return 2
    read=contract.get("state_revision"); current=state.get("revision"); status=a.status; uncertainties=[]
    if read!=current: status="stale"; uncertainties.append(f"状态版本过期：契约读取 {read}，当前 {current}")
    if status=="stale" and a.artifact:
        print("stale handoff cannot include artifacts",file=sys.stderr); return 2
    if status=="completed":
        if a.role=="executor" and not a.artifact:
            print("completed handoff requires at least one executor artifact",file=sys.stderr); return 2
        if a.role=="auditor" and not any(rel(x,root).startswith(".codex-research/audits/") for x in a.artifact):
            print("completed auditor handoff requires an audit report artifact",file=sys.stderr); return 2
        if not a.verification_command.strip() or not a.verification_result.strip() or not a.quality_gate:
            print("completed handoff requires fresh verification command/result and a quality gate",file=sys.stderr); return 2
    stamp=datetime.now(timezone.utc).astimezone().strftime("%Y%m%dT%H%M%S%z"); hid=f"{stamp}_{a.task_id}_{a.role}_{secrets.token_hex(2)}"
    value={"schema_version":"codex-research-handoff/v1","handoff_id":hid,"project_id":state.get("project_id"),"task_id":a.task_id,"sender_role":a.role,"state_revision_read":read,"contract_path":rel(contract_path,root),"contract_sha256":sha(contract_path),"status":status,"fresh_verification":{"command":a.verification_command,"result":a.verification_result},"artifacts":[{"path":rel(x,root),"purpose":"contract deliverable","sha256":sha(x),"verification":{"command":a.verification_command,"result":a.verification_result}} for x in a.artifact],"verified_findings":[],"inferences":[],"uncertainties":uncertainties,"decisions_needed":[],"quality_gates":a.quality_gate,"recommended_next_action":a.recommended_next_action}
    if a.role=="auditor": value.update({"verdict":a.verdict,"findings":[]})
    value["handoff_content_sha256"]=content_sha(value)
    out=c/"handoffs"/f"{hid}.yaml"; out.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n"); print(f"CREATED: {out}"); return 0
if __name__=="__main__": raise SystemExit(main())
