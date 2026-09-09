# Integrity and delivery gates

## Contents

1. Gate ledger
2. Epistemic labels
3. Truthfulness rules
4. Verification matrix
5. Red flags and rationalizations

## 1. Gate ledger

Maintain the following mentally or in authorized long-task state:

| Gate | Pass evidence | Failure response |
|---|---|---|
| Authority | requested operation, allowed materials, exact write target | narrow scope; pause only for material ambiguity |
| Materials | authoritative paths/IDs/versions, keys, fields, sample/exclusions | diagnose mismatch; do not silently substitute |
| Epistemic | claim labels and evidence locator | weaken, label, verify, or remove claim |
| Empirical truthfulness | reproducible lineage from data to result/figure/text | reject manipulation; rerun dependent outputs |
| Citation support | identity check plus claim-level support check | mark candidate/unverified or revise claim |
| Completion | fresh command/check output covering deliverables | state actual incomplete status and next step |

These gates are cumulative. Passing a later gate does not repair an earlier failure.

## 2. Epistemic labels

- `evidence`: directly supported by an inspected authoritative source or fresh result.
- `inference`: reasoned interpretation from stated evidence; alternatives remain.
- `hypothesis`: testable proposed relationship or mechanism.
- `recommendation`: preferred action based on evidence, constraints, and judgment.
- `unverified`: plausible but not yet checked, inaccessible, ambiguous, or time-sensitive.

Use labels explicitly when a reader could mistake one category for another. Do not decorate every ordinary sentence.

## 3. Truthfulness rules

- Never alter data, labels, exclusions, model, threshold, axis, result table, or figure to obtain a desired direction, significance, balance, or visual impression.
- Analytic changes require scientific justification, provenance, rerunning all dependent outputs, and disclosure.
- Preserve adverse diagnostics. Explain them, revise the design transparently, or limit the claim.
- A deadline does not relax evidence or authorization gates.
- A real citation can still be a false citation if it does not support the claim.
- Search snippets, generated summaries, and prior chat statements are discovery aids, not final evidence.

## 4. Verification matrix

| Deliverable | Fresh evidence required |
|---|---|
| Data table | schema, row/ID counts, missingness, invariants, source version |
| Statistical result | exact command/run, sample/estimand, diagnostics, output values |
| Figure | regenerated file, plotted-data identity, visual inspection |
| Code | relevant tests, full test suite as proportionate, clean exit/output |
| Manuscript | diff/scope audit, number/citation checks, render when applicable |
| Literature matrix | deduplication, identity and claim-support status, search log |
| Journal recommendation | current official indexing/scope/requirements with access date |
| Continuation state | current project path, latest artifacts and validation re-opened |

Before saying “完成/通过/已修复/一致”, identify the proving check, run it now, read the full result, and ensure it covers the claim.

## 5. Red flags and rationalizations

Stop and correct course when thinking:

- “用户大概也允许我顺手改.”
- “这个目录最像上次项目，先用它.”
- “只是画图，改几个点不影响表格.”
- “换了样本/estimand，但结论方向一样.”
- “论文是真的，所以可以支持这句话.”
- “旧分区应该还没变.”
- “测试刚才跑过，不必再跑.”
- “先说完成，细节以后补.”

| Rationalization | Correction |
|---|---|
| Urgency implies permission | Deadlines never expand authority. |
| Cosmetic figure edits are harmless | Figures are research results and must share the analysis lineage. |
| Same sign means same estimand | Estimand defines the scientific quantity; pause on change. |
| Topical relevance equals support | Verify the exact claim, population, method, and causal strength. |
| Recent memory equals current state | Re-open authoritative artifacts and rerun the proving check. |
