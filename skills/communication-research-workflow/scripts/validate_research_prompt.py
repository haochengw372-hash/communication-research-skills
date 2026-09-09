#!/usr/bin/env python3
"""Validate a generated codex-research-workflow prompt deterministically."""
from __future__ import annotations
import argparse, re
from pathlib import Path

ROLES={"controller","prompt","executor","auditor"}
OPERATIONS={"diagnose","plan","execute","review","full-pipeline"}
RIGORS={"quick","standard","audit"}
AUTHORITIES={"read-only","edit-existing","create-new"}
TASK_TYPES={"research-question","literature-review","scientometrics-network","data-audit","empirical-analysis","research-code","computational-content-analysis","experiment-survey","research-visualization","writing-revision","manuscript-review","journal-fit","citation-finalization","project-continuation","project-governance"}
def value(text,key):
    m=re.search(rf"(?m)^{re.escape(key)}\s*=\s*(.+?)\s*$",text); return m.group(1).strip() if m else None
def values(text,key):
    return [item.strip() for item in re.findall(rf"(?m)^{re.escape(key)}\s*=\s*(.*?)\s*$", text)]
def labeled_value(text,label):
    m=re.search(rf"(?m)^{re.escape(label)}[ \t]*([^\r\n]*)$", text); return m.group(1).strip() if m else None
def any_labeled_value(text,*labels):
    return next((item for label in labels if (item:=labeled_value(text,label))), None)
def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("prompt",type=Path); a=p.parse_args(argv); text=a.prompt.read_text(encoding="utf-8-sig"); errors=[]
    first=next((x.strip() for x in text.splitlines() if x.strip()),"")
    if first!="Use $communication-research-workflow.": errors.append("first non-empty line must equal: Use $communication-research-workflow.")
    if len(re.findall(r"\$communication-research-workflow", text, re.I)) > 1: errors.append("recursive workflow invocation is forbidden")
    mode=value(text,"prompt_mode") or "standalone"; role=value(text,"target_role"); operation=value(text,"operation"); authority=value(text,"authority"); rigor=value(text,"rigor")
    for key in ("prompt_mode","project_id","task_id","target_role","state_revision","task_type","operation","rigor","authority"):
        if len(values(text,key)) > 1: errors.append(f"duplicate control field: {key}")
    if mode not in {"standalone","project-aware"}: errors.append("prompt_mode must be standalone or project-aware")
    if role not in ROLES: errors.append("target_role must name one of the four roles")
    if operation not in OPERATIONS: errors.append("missing or invalid operation")
    if rigor not in RIGORS: errors.append("missing or invalid rigor")
    if authority not in AUTHORITIES: errors.append("missing or invalid authority")
    if value(text,"task_type") not in TASK_TYPES: errors.append("missing or invalid task_type")
    revision=value(text,"state_revision")
    if revision and not re.fullmatch(r"\d+", revision): errors.append("state_revision must be a non-negative integer")
    if mode=="project-aware":
        for key in ("project_id","task_id","state_revision"):
            if not value(text,key): errors.append(f"missing {key}")
        contract_location=any_labeled_value(text,"Task contract:","任务契约：")
        if not contract_location or re.search(r"待|TBD|TODO|尚未",contract_location,re.I): errors.append("project-aware mode requires a concrete contract location")
        if re.search(r"(?:递归|全部|整个项目).{0,12}(?:扫描|论文|数据)|(?:扫描).{0,12}(?:整个项目|全部论文|全部数据)", text): errors.append("project-aware mode may read only the project control layer and named artifacts")
    if operation in {"review","diagnose"} and authority!="read-only": errors.append("review and diagnose require authority=read-only")
    if operation=="plan" and authority!="read-only": errors.append("plan requires authority=read-only")
    if operation in {"execute","full-pipeline"} and authority not in {"edit-existing","create-new"}: errors.append("execute and full-pipeline require write authority")
    if role=="auditor" and (authority!="read-only" or operation!="review" or rigor!="audit"): errors.append("auditor requires operation=review, rigor=audit, authority=read-only")
    if role=="prompt" and (operation not in {"plan","diagnose"} or authority!="read-only"): errors.append("prompt role requires read-only plan or diagnose operation")
    if not any_labeled_value(text,"Deliverables:","交付物："): errors.append("missing verifiable deliverables")
    if not any_labeled_value(text,"Quality gates:","质量门禁："): errors.append("missing quality gates")
    actionable_lines=[]
    for line in text.splitlines():
        if re.search(r"(?:禁止|不得|不可|不允许).*(?:但|必须|同时|然后|后直接)",line): actionable_lines.append(line)
        elif re.search(r"(?:禁止|不得|不可|不允许|不要)",line): continue
        else: actionable_lines.append(line)
    actionable="\n".join(actionable_lines); normalized=actionable.replace("\\","/")
    broad_read=r"(?:(?:递归|遍历|扫描|枚举|通读|加载|盘点|读取|查阅|浏览|导入|爬取|建立).{0,30}(?:整个项目|项目根目录|项目目录|工作区|仓库|代码库|项目树|源码树).{0,30}(?:每一|每份|所有|全部|全量|代码|论文|脚本|数据|材料|内容|文件|索引)|(?:整个项目|项目根目录|项目目录|工作区|仓库|代码库|项目树|源码树).{0,20}(?:建立|生成|创建).{0,12}(?:文件)?索引)"
    if re.search(broad_read,actionable): errors.append("broad project read is forbidden")
    governance=r"(?:\.codex-research/)?(?:state\.yaml|contracts(?:/[^\s，；。]*)?|decisions\.md|snapshots(?:/[^\s，；。]*)?)"
    write_action=r"(?:修改|更新|改写|覆盖|编辑|写入|创建|负责更新|直接更新|修订|维护|删除|追加|提交至|保存至|写到|改动|重写|变更|移除|增补|同步.{0,8}到|持久化至)"
    if role in {"prompt","executor","auditor"} and (re.search(rf"{write_action}.{{0,40}}{governance}", normalized, re.I) or re.search(rf"{governance}.{{0,24}}{write_action}", normalized, re.I)): errors.append("controller-only governance update requested")
    generic_write=r"(?:修改|改写|覆盖|编辑|写入|创建|运行|执行|删除|追加|修订|维护|保存|提交|更正|替换|落实|调整).{0,24}(?:\.docx|\.csv|\.py|\.xlsx|\.md|\.tex|\.parquet|数据|脚本|稿件|回归|模型|结果|manuscript|article)"
    if role in {"prompt","auditor"} and re.search(generic_write,actionable,re.I): errors.append("role body conflicts with read-only role")
    if operation in {"review","diagnose","plan"} and authority=="read-only" and re.search(generic_write,actionable,re.I): errors.append("role body conflicts with read-only operation")
    if role=="executor" and authority=="create-new" and re.search(r"(?:修改|编辑|覆盖|改写|修订).{0,12}(?:已有|现有)",actionable): errors.append("role body conflicts with create-new authority")
    if (rigor=="audit" or role=="auditor") and re.search(r"(?:待补充|待核验|待确认|待确定|尚未提供|未知|\?{3,}|……|\bTBD\b|\bTODO\b)",text,re.I): errors.append("audit prompt contains unresolved placeholder")
    if role=="executor" and operation in {"execute","full-pipeline"}:
        for english, chinese in (("Required reads:","必须读取："),("Allowed reads:","允许读取："),("Write scope:","写入范围：")):
            if not any_labeled_value(text,english,chinese): errors.append(f"formal executor missing required scope: {english}")
    if role in {"executor","auditor"} and not any_labeled_value(text,"Handoff requirements:","交接要求："): errors.append("missing handoff requirement")
    if errors: print("INVALID"); [print(f"- {x}") for x in errors]; return 1
    print("VALID: codex-research-workflow prompt"); return 0
if __name__=="__main__": raise SystemExit(main())
