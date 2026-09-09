# Contract and boundary examples

## Example 1: PSM/ATT audit

```yaml
task_type: empirical-analysis
goal: 核对匹配后的 ATT、平衡性与论文表述是否一致
operation: review
rigor: audit
authority: read-only
source_of_truth: {"dataset": "matched_weights.parquet", "estimand": "ATT", "sample": "treated units on common support and matched controls"}
materials:
  - analysis script
  - matched weights
  - balance table
  - Love plot
  - results section
deliverables:
  - issue-ranked audit in the response
quality_gates:
  - authority
  - sample-and-estimand
  - figure-table-text identity
constraints:
  - do not edit files
stop_conditions:
  - estimand or sample definition differs across artifacts
uncertainties:
  - standard-error method not yet verified
```

Correct behavior: inspect only; never cap SMD values or modify scripts. If estimand/sample drift is found, pause before any execution.

## Example 2: Zotero/OpenAlex evidence matrix

Use `literature-review`, `openalex-database`, and `zotero:Zotero`. Keep candidate and verified records separate. External Zotero writes require explicit authority. A paper enters synthesis only after identity and claim support are verified.

## Example 3: Conflicting authority

Request: “只评价修改要求，不读本地数据，也不要实施；顺手把稿件改好。”

Resolve as `operation=review`, `authority=read-only`. Evaluate only the text supplied or authorized. The phrase “顺手” does not authorize editing.

## Example 4: Cross-database entity mapping

Overton and OpenAlex IDs are source-specific. Build a crosswalk using official identity evidence, ROR/domain/hierarchy where applicable, plus confidence. Do not build final network metrics until time window, nodes, edges, and ambiguous entities are resolved.

## Example 5: Continue a project

When “继续上次 PSM 项目” could refer to several directories, inspect history/state and candidate artifacts read-only. Require a unique match before writing. Restore the last sample, estimand, paths, outputs, and verification rather than assuming the newest directory.

## Example 6: Negative triggers

- “概括这篇 PDF” → use the PDF Skill directly.
- “解释这个普通 Python traceback” → use Code/debugging directly.
- “设计本科课程” → teaching workflow, not this research Skill.
- “整理学院行政表格” → document/spreadsheet workflow, not this research Skill.
