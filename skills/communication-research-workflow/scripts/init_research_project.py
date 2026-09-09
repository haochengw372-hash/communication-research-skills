#!/usr/bin/env python3
"""Initialize the non-invasive Codex research project control layer."""
from __future__ import annotations
import argparse, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

VERSION = "codex-research-project/v1"

def dump(value): return json.dumps(value, ensure_ascii=False, indent=2) + "\n"
def valid_id(value): return bool(re.fullmatch(r"[a-z0-9][a-z0-9-]{1,62}", value))

def documents(project_id, title):
    now = datetime.now(timezone.utc).isoformat()
    project = {"schema_version": VERSION, "project_id": project_id, "title": title or project_id, "created_at": now, "control_root": ".codex-research", "governance": "controller-single-writer", "research_materials": "remain-in-place"}
    state = {"schema_version": "codex-research-state/v1", "project_id": project_id, "revision": 0, "updated_at": now, "updated_by": "controller", "current_stage": "project-initiation", "work_packages": {}, "ready_tasks": [], "blocked_tasks": {}, "source_of_truth": {"inputs": [], "keys": [], "sample": "", "estimand": "", "time_window": ""}, "verified_artifacts": [], "key_decisions": [], "open_issues": [], "pending_handoffs": [], "next_actions": [], "latest_verification": {}}
    windows = {"schema_version": "codex-research-windows/v1", "project_id": project_id, "roles": {"controller": {"instances": 1, "writes": ["state.yaml", "contracts/", "decisions.md", "snapshots/"]}, "prompt": {"instances": None, "writes": ["handoffs/"]}, "executor": {"instances": None, "writes": ["contract-authorized artifacts", "handoffs/"]}, "auditor": {"instances": None, "writes": ["audits/", "handoffs/"]}}}
    return project, state, windows

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("project_root", type=Path); p.add_argument("--project-id", required=True); p.add_argument("--title", default=""); p.add_argument("--dry-run", action="store_true"); a=p.parse_args(argv)
    if not valid_id(a.project_id): print("INVALID project-id: use lowercase letters, digits, and hyphens", file=sys.stderr); return 2
    root=a.project_root.resolve(); control=root/".codex-research"; project,state,windows=documents(a.project_id,a.title)
    files={control/"project.yaml":dump(project), control/"state.yaml":dump(state), control/"windows.yaml":dump(windows), control/"decisions.md":"# Decision log\n\nOnly the controller records accepted project decisions here.\n"}
    fragment=(Path(__file__).resolve().parents[1]/"assets"/"project-control"/"AGENTS.fragment.md").read_text(encoding="utf-8")
    agents=root/"AGENTS.md"
    if agents.exists(): files[control/"AGENTS.codex-research.fragment.md"]=fragment
    else: files[agents]=fragment
    dirs=[control/n for n in ("contracts","handoffs","audits","snapshots")]
    actions=[f"CREATE {x}" for x in dirs if not x.exists()]+[f"CREATE {x}" for x in files if not x.exists()]
    if a.dry_run: print("DRY RUN\n"+"\n".join(actions or ["NO CHANGES"])); return 0
    root.mkdir(parents=True, exist_ok=True)
    for d in dirs: d.mkdir(parents=True, exist_ok=True)
    for path,text in files.items():
        if not path.exists(): path.write_text(text, encoding="utf-8", newline="\n")
    print("INITIALIZED\n"+"\n".join(actions or ["NO CHANGES"])); return 0
if __name__=="__main__": raise SystemExit(main())
