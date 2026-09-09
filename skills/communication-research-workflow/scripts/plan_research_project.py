#!/usr/bin/env python3
"""Generate a reviewable research-stage and Codex-window plan.

The output is a planning aid. It does not create Codex tasks, mutate project
state, or authorize research work.
"""
from __future__ import annotations

import argparse
import json
import re
from typing import Any


SCHEMA_VERSION = "codex-research-plan/v1"
ARCHETYPES = (
    "cross-sectional-observational",
    "panel-longitudinal",
    "causal-policy-evaluation",
    "survey",
    "experiment",
    "text-computational",
    "network",
    "temporal",
    "multimodal",
    "spatial",
    "simulation",
    "predictive",
    "qualitative",
    "mixed-methods",
)

# Which suite Skills own the analysis stage for each archetype. The planner
# never emits a Skill name outside this suite; general statistical or writing
# tooling is reached through these domain Skills, not by inventing new names.
ANALYSIS_SKILLS: dict[str, list[str]] = {
    "experiment": ["communication-experiment"],
    "survey": ["communication-experiment", "communication-scale"],
    "text-computational": ["communication-content-analysis"],
    "network": ["communication-network-analysis"],
    "temporal": ["communication-temporal-analysis"],
    "multimodal": ["communication-multimodal-analysis"],
    "spatial": ["communication-spatial-analysis"],
    "simulation": ["communication-simulation"],
    "predictive": ["communication-content-analysis", "communication-temporal-analysis"],
    "causal-policy-evaluation": ["communication-causal-inference"],
    "panel-longitudinal": ["communication-temporal-analysis"],
    "cross-sectional-observational": ["communication-method-router"],
    "qualitative": ["communication-content-analysis", "communication-theory"],
    "mixed-methods": ["communication-content-analysis", "communication-experiment"],
}


def package(
    task_id: str,
    title: str,
    stage: str,
    depends_on: list[str],
    goal: str,
    deliverables: list[str],
    skills: list[str],
    *,
    role: str = "executor",
    rigor: str = "standard",
    audit_required: bool = False,
    timing: str = "Open later",
) -> dict[str, Any]:
    return {
        "task_id": task_id,
        "title": title,
        "stage": stage,
        "role": role,
        "depends_on": depends_on,
        "goal": goal,
        "deliverables": deliverables,
        "skill_stack": skills,
        "rigor": rigor,
        "audit_required": audit_required,
        "timing": timing,
        "open_when": "All dependencies are accepted by the controller" if depends_on else "Project boundary is recorded",
        "close_when": "Deliverables, fresh verification, and an immutable handoff are accepted",
        "write_scope": [f"outputs/{task_id}/"] if role == "executor" else [f".codex-research/audits/{task_id}/"],
    }


def universal_packages() -> list[dict[str, Any]]:
    return [
        package(
            "question-theory",
            "Research question, theory, and contribution",
            "framing",
            [],
            "Turn the topic into answerable questions, mechanisms, rival explanations, and contribution claims.",
            ["research-question memo", "mechanism map", "rival explanations", "feasibility risks"],
            ["communication-theory"],
            timing="Open now",
        ),
        package(
            "literature-evidence",
            "Literature search and evidence map",
            "evidence",
            [],
            "Establish the verified evidence base, disagreements, boundary conditions, and unresolved gaps.",
            ["search log", "screening rules", "evidence matrix", "claim-support status"],
            ["communication-literature"],
            timing="Open now",
        ),
        package(
            "constructs-measurement",
            "Constructs and measurement",
            "design",
            ["question-theory", "literature-evidence"],
            "Map every theoretical construct to observations and assess validity, reliability, and proxy limits.",
            ["construct dictionary", "operational definitions", "validity threats"],
            ["communication-construct", "communication-scale"],
        ),
        package(
            "design-sampling-ethics",
            "Design, sampling, and ethics",
            "design",
            ["constructs-measurement"],
            "Specify population, sample, timing, comparison, ethics, privacy, estimand, and analysis boundaries.",
            ["design protocol", "sampling plan", "ethics and data-governance checklist", "definition lock candidate"],
            ["communication-method-router"],
            audit_required=True,
        ),
    ]


def quantitative_tail(
    data_dependency: str,
    model_dependency: str | None,
    analysis_skills: list[str],
) -> list[dict[str, Any]]:
    model_dep = model_dependency or data_dependency
    return [
        package(
            "exploratory-analysis",
            "Exploratory data analysis",
            "analysis",
            [data_dependency],
            "Describe data quality and patterns without converting exploration into confirmatory evidence.",
            ["EDA report", "anomaly log", "descriptive tables"],
            analysis_skills,
            rigor="quick",
        ),
        package(
            "confirmatory-model",
            "Confirmatory estimation",
            "analysis",
            [model_dep],
            "Estimate the locked estimand using the prespecified primary specification and diagnostics.",
            ["model outputs", "effect sizes and uncertainty", "diagnostics", "run log"],
            analysis_skills,
            rigor="audit",
            audit_required=True,
        ),
        package(
            "robustness-sensitivity",
            "Robustness and sensitivity",
            "analysis",
            ["confirmatory-model"],
            "Test plausible alternative specifications and threats without selecting results by significance.",
            ["robustness matrix", "sensitivity results", "scope-of-claim recommendation"],
            analysis_skills + ["communication-reviewer"],
            rigor="audit",
            audit_required=True,
        ),
        package(
            "audit-results",
            "Independent result audit",
            "audit",
            ["confirmatory-model", "robustness-sensitivity"],
            "Independently verify sample, estimand, code, diagnostics, tables, and claim strength.",
            ["Critical/Major/Minor audit report", "verdict", "verified artifact hashes"],
            ["communication-reviewer"],
            role="auditor",
            rigor="audit",
        ),
        package(
            "results-integration",
            "Tables, figures, and result narrative",
            "communication",
            ["audit-results"],
            "Create a consistent data-to-table-to-figure-to-text result chain.",
            ["final tables", "reproducible figures", "result narrative", "lineage check"],
            analysis_skills + ["communication-writing"],
        ),
        package(
            "manuscript-integration",
            "Manuscript integration",
            "writing",
            ["results-integration", "literature-evidence"],
            "Integrate the question, evidence, design, results, limitations, and contribution for the target audience.",
            ["claim map", "manuscript draft", "number and terminology inventory"],
            ["communication-writing"],
            audit_required=True,
        ),
        package(
            "prose-revision",
            "Section-sensitive prose revision",
            "writing",
            ["manuscript-integration"],
            "Reduce formulaic and defensive prose while preserving the accepted claims, evidence, terminology, numbers, and uncertainty.",
            ["revised manuscript", "prose diagnostic", "style change ledger"],
            ["communication-prose-revision"],
        ),
        package(
            "audit-final",
            "Final manuscript and citation audit",
            "audit",
            ["prose-revision"],
            "Verify claim-source support, numerical consistency, reporting requirements, and completion evidence.",
            ["final audit report", "citation-support matrix", "submission readiness verdict"],
            ["communication-reviewer", "communication-literature"],
            role="auditor",
            rigor="audit",
        ),
    ]


def data_audit(depends_on: list[str], analysis_skills: list[str]) -> dict[str, Any]:
    return package(
        "data-audit",
        "Data provenance and quality audit",
        "data",
        depends_on,
        "Verify sources, units, keys, joins, missingness, exclusions, versions, and row transitions.",
        ["data contract", "schema and key audit", "sample-flow table", "variable dictionary"],
        analysis_skills,
        audit_required=True,
    )


def archetype_packages(archetype: str) -> list[dict[str, Any]]:
    design = "design-sampling-ethics"
    analysis_skills = ANALYSIS_SKILLS[archetype]
    if archetype == "qualitative":
        return [
            package("qualitative-data", "Qualitative data generation and management", "data", [design], "Collect or organize qualitative material with consent, provenance, reflexivity, and a documented sampling logic.", ["sampling and fieldwork record", "de-identified corpus", "reflexive memo"], analysis_skills),
            package("qualitative-analysis", "Qualitative coding and interpretation", "analysis", ["qualitative-data"], "Develop and apply an auditable codebook, assess saturation or information power, and examine negative cases.", ["codebook", "coded excerpts with locators", "theme and negative-case matrix"], analysis_skills, rigor="audit", audit_required=True),
            package("audit-qualitative", "Independent qualitative audit", "audit", ["qualitative-analysis"], "Review sampling, reflexivity, coding decisions, negative cases, and evidence-to-interpretation links.", ["audit report", "verdict"], ["communication-reviewer"], role="auditor", rigor="audit"),
            package("manuscript-integration", "Manuscript integration", "writing", ["audit-qualitative", "literature-evidence"], "Write a coherent evidence-grounded manuscript with explicit positionality and transferability limits.", ["claim map", "manuscript draft"], ["communication-writing"], audit_required=True),
            package("prose-revision", "Section-sensitive prose revision", "writing", ["manuscript-integration"], "Reduce formulaic and defensive prose while preserving accepted meaning and evidence.", ["revised manuscript", "prose diagnostic", "style change ledger"], ["communication-prose-revision"]),
            package("audit-final", "Final manuscript and citation audit", "audit", ["prose-revision"], "Verify evidence links, citations, reporting standards, and final scope of claims.", ["final audit report", "verdict"], ["communication-reviewer", "communication-literature"], role="auditor", rigor="audit"),
        ]

    if archetype == "mixed-methods":
        packages = [
            data_audit([design], analysis_skills),
            package("quantitative-analysis", "Quantitative strand", "analysis", ["data-audit"], "Execute the quantitative strand under its locked estimand and diagnostics.", ["quantitative results", "diagnostics"], ["communication-experiment"], rigor="audit", audit_required=True),
            package("qualitative-data", "Qualitative strand data", "data", [design], "Generate or organize qualitative evidence with provenance and reflexive documentation.", ["qualitative corpus", "fieldwork record"], ["communication-content-analysis"]),
            package("qualitative-analysis", "Qualitative strand analysis", "analysis", ["qualitative-data"], "Apply an auditable codebook and examine confirming and disconfirming cases.", ["codebook", "theme matrix"], ["communication-content-analysis", "communication-theory"], rigor="audit", audit_required=True),
            package("mixed-integration", "Mixed-methods integration", "integration", ["quantitative-analysis", "qualitative-analysis"], "Integrate convergent, complementary, and conflicting evidence using the prespecified mixed-methods logic.", ["joint display", "meta-inferences", "discordance log"], ["communication-reviewer", "communication-method-router"], rigor="audit", audit_required=True),
            package("audit-results", "Independent mixed-methods audit", "audit", ["mixed-integration"], "Audit each strand and the legitimacy of cross-strand meta-inferences.", ["audit report", "verdict"], ["communication-reviewer"], role="auditor", rigor="audit"),
            package("manuscript-integration", "Manuscript integration", "writing", ["audit-results", "literature-evidence"], "Write the integrated evidence story without forcing convergence.", ["claim map", "manuscript draft"], ["communication-writing"], audit_required=True),
            package("prose-revision", "Section-sensitive prose revision", "writing", ["manuscript-integration"], "Reduce formulaic and defensive prose while preserving accepted meaning and evidence.", ["revised manuscript", "prose diagnostic", "style change ledger"], ["communication-prose-revision"]),
            package("audit-final", "Final manuscript and citation audit", "audit", ["prose-revision"], "Verify citations, strand consistency, reporting standards, and completion evidence.", ["final audit report", "verdict"], ["communication-reviewer", "communication-literature"], role="auditor", rigor="audit"),
        ]
        return packages

    branch: list[dict[str, Any]] = []
    data_dependencies = [design]
    model_dependency: str | None = None

    if archetype == "causal-policy-evaluation":
        branch.extend([
            package("design-identification", "Identification strategy", "design", [design], "Define treatment timing, counterfactual, estimand, identifying assumptions, diagnostics, and falsification tests.", ["identification memo", "estimand statement", "assumption-to-test map"], ["communication-causal-inference"], rigor="audit", audit_required=True),
            package("audit-identification", "Independent identification audit", "audit", ["design-identification"], "Challenge identification assumptions, timing, spillovers, anticipation, and alternative explanations before estimation.", ["identification audit", "verdict"], ["communication-reviewer"], role="auditor", rigor="audit"),
        ])
        data_dependencies = ["audit-identification"]
        model_dependency = "data-audit"
    elif archetype == "panel-longitudinal":
        branch.append(package("panel-specification", "Panel structure and dependence", "design", [design], "Lock panel unit, time index, attrition, fixed effects, dependence, clustering, and dynamic specification.", ["panel specification", "attrition plan", "standard-error plan"], ["communication-temporal-analysis"], rigor="audit", audit_required=True))
        data_dependencies = ["panel-specification"]
    elif archetype == "survey":
        branch.append(package("instrument-pilot", "Survey instrument and pilot", "design", [design], "Validate question wording, scales, response process, pilot behavior, nonresponse, and weighting plan.", ["instrument", "pilot report", "reliability and validity plan"], ["communication-scale", "communication-method-router"], audit_required=True))
        data_dependencies = ["instrument-pilot"]
    elif archetype == "experiment":
        branch.append(package("randomization-protocol", "Randomization and protocol", "design", [design], "Lock randomization, allocation, manipulation checks, outcomes, exclusions, power, and attrition handling.", ["experimental protocol", "randomization plan", "power analysis", "analysis plan"], ["communication-experiment", "communication-scale"], rigor="audit", audit_required=True))
        data_dependencies = ["randomization-protocol"]
    elif archetype == "text-computational":
        branch.append(package("annotation-validation", "Corpus, labels, and construct validation", "design", [design], "Lock corpus boundaries, annotation protocol, intercoder checks, leakage controls, and construct-validity tests.", ["corpus contract", "annotation guide", "validation plan"], ["communication-content-analysis", "communication-construct", "communication-scale"], rigor="audit", audit_required=True))
        data_dependencies = ["annotation-validation"]
    elif archetype == "network":
        branch.append(package("network-definition", "Network boundary and graph definition", "design", [design], "Lock node and edge meaning, direction, weight, boundary, temporal rule, missingness, and sensitivity choices.", ["graph contract", "boundary audit", "known-example test"], ["communication-network-analysis"], rigor="audit", audit_required=True))
        data_dependencies = ["network-definition"]
    elif archetype == "temporal":
        branch.append(package("temporal-definition", "Temporal process and observation contract", "design", [design], "Lock the clock, interval, risk set, lags, censoring, attrition, temporal aggregation, and dependence.", ["temporal contract", "lag and risk-set rules", "dependence diagnostics plan"], ["communication-temporal-analysis"], rigor="audit", audit_required=True))
        data_dependencies = ["temporal-definition"]
    elif archetype == "multimodal":
        branch.append(package("multimodal-definition", "Multimodal corpus and unitization", "design", [design], "Lock media sampling, frames/scenes/speakers, OCR/ASR or model extraction, cross-modal relations, and human validation.", ["multimodal corpus contract", "unitization protocol", "extraction and validation plan"], ["communication-multimodal-analysis"], rigor="audit", audit_required=True))
        data_dependencies = ["multimodal-definition"]
    elif archetype == "spatial":
        branch.append(package("spatial-definition", "Spatial unit and geographic data contract", "design", [design], "Lock geocoding, spatial unit, CRS, joins, weights, scale, privacy, and ecological claim boundaries.", ["spatial contract", "geocoding and join audit", "scale-sensitivity plan"], ["communication-spatial-analysis"], rigor="audit", audit_required=True))
        data_dependencies = ["spatial-definition"]
    elif archetype == "simulation":
        branch.append(package("simulation-protocol", "Simulation mechanisms and validation", "design", [design], "Lock agents, micro-rules, topology, schedule, parameters, calibration targets, held-out validation, seeds, and rival models.", ["simulation contract", "parameter provenance", "calibration and validation plan"], ["communication-simulation"], rigor="audit", audit_required=True))
        data_dependencies = ["simulation-protocol"]
    elif archetype == "predictive":
        branch.append(package("validation-design", "Prediction target and validation design", "design", [design], "Lock prediction time, target, leakage controls, splits, baselines, metrics, calibration, and external validation.", ["prediction protocol", "split policy", "metric and calibration plan"], ["communication-method-router"], rigor="audit", audit_required=True))
        data_dependencies = ["validation-design"]
    elif archetype == "cross-sectional-observational":
        branch.append(package("confounding-plan", "Confounding and selection plan", "design", [design], "Specify plausible confounders, selection processes, adjustment set, missingness, and causal-language limits.", ["DAG or confounding memo", "adjustment plan", "scope-of-claim rule"], ["communication-method-router"], rigor="audit", audit_required=True))
        data_dependencies = ["confounding-plan"]

    branch.append(data_audit(data_dependencies, analysis_skills))
    branch.extend(quantitative_tail("data-audit", model_dependency, analysis_skills))
    return branch


def build_plan(project_id: str, title: str, archetype: str, include_prompt: bool) -> dict[str, Any]:
    packages = universal_packages() + archetype_packages(archetype)
    windows: list[dict[str, Any]] = [{
        "window_id": "C0",
        "role": "controller",
        "title": "Project controller",
        "lifecycle": "long-lived",
        "timing": "Open now",
        "task_id": None,
        "responsibilities": ["maintain authoritative state", "issue contracts", "merge handoffs", "freeze consequential definitions"],
    }]
    if include_prompt:
        windows.append({
            "window_id": "P0",
            "role": "prompt",
            "title": "Prompt workbench",
            "lifecycle": "optional-long-lived",
            "timing": "Open now",
            "task_id": None,
            "responsibilities": ["compile role prompts from accepted contracts", "never execute the compiled research task"],
        })
    for index, item in enumerate(packages, start=1):
        windows.append({
            "window_id": f"W{index:02d}",
            "role": item["role"],
            "title": item["title"],
            "lifecycle": "stage-bound",
            "timing": item["timing"],
            "task_id": item["task_id"],
            "responsibilities": [item["goal"]],
        })
    return {
        "schema_version": SCHEMA_VERSION,
        "project_id": project_id,
        "title": title or project_id,
        "archetype": archetype,
        "status": "proposed-not-authoritative",
        "controller_rule": "Only the controller may accept this plan into project state",
        "windows": windows,
        "work_packages": packages,
        "decision_points": [
            "primary research question or theoretical contribution changes",
            "construct, source-of-truth, sample, key, or time window changes",
            "estimand or identification strategy changes",
            "external write or final submission is proposed",
        ],
    }


def mermaid_id(task_id: str) -> str:
    return "N_" + re.sub(r"[^A-Za-z0-9_]", "_", task_id)


def render_markdown(plan: dict[str, Any]) -> str:
    lines = [
        f"# Research window plan: {plan['title']}",
        "",
        f"- Project ID: `{plan['project_id']}`",
        f"- Archetype: `{plan['archetype']}`",
        f"- Status: `{plan['status']}`",
        "",
        "## Windows",
        "",
        "| Window | Role | Timing | Lifecycle | Work package |",
        "|---|---|---|---|---|",
    ]
    for window in plan["windows"]:
        lines.append(f"| {window['window_id']} | {window['role']} | {window['timing']} | {window['lifecycle']} | {window['task_id'] or 'governance'} |")
    lines.extend(["", "## Dependency graph", "", "```mermaid", "flowchart TD"])
    for item in plan["work_packages"]:
        lines.append(f"    {mermaid_id(item['task_id'])}[\"{item['title']}\"]")
    for item in plan["work_packages"]:
        for dependency in item["depends_on"]:
            lines.append(f"    {mermaid_id(dependency)} --> {mermaid_id(item['task_id'])}")
    lines.extend(["```", "", "## Work packages", ""])
    for item in plan["work_packages"]:
        lines.extend([
            f"### {item['task_id']}: {item['title']}",
            "",
            f"- Role: `{item['role']}`; rigor: `{item['rigor']}`; timing: **{item['timing']}**",
            f"- Depends on: {', '.join(f'`{x}`' for x in item['depends_on']) or 'none'}",
            f"- Goal: {item['goal']}",
            f"- Deliverables: {'; '.join(item['deliverables'])}",
            f"- Open when: {item['open_when']}",
            f"- Close when: {item['close_when']}",
            "",
        ])
    lines.extend(["## Controller decision points", ""])
    lines.extend(f"- {item}" for item in plan["decision_points"])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--title", default="")
    parser.add_argument("--archetype", choices=ARCHETYPES, required=True)
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--include-prompt-workbench", action="store_true")
    args = parser.parse_args(argv)
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,62}", args.project_id):
        parser.error("project-id must use lowercase letters, digits, and hyphens")
    plan = build_plan(args.project_id, args.title, args.archetype, args.include_prompt_workbench)
    if args.format == "json":
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(plan), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
