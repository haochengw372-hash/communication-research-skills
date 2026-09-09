# Research design, evidence, and scientometrics workflows

## Contents

1. Research question and hypothesis
2. Literature review and evidence matrix
3. Scientometrics and cross-database citation networks
4. Project continuation

## 1. Research question and hypothesis

**Use for:** topic development, research gaps, conceptual models, hypotheses, and feasibility.

**Minimum inputs:** phenomenon, unit of analysis, outcome, mechanism, context/time window, intended contribution, accessible data.

**Route:** `communication-theory` for mechanism and rival explanations,
`communication-literature` for the verified gap, and `communication-reviewer` for the
question/contribution gate. Add `communication-writing` only when an accepted framing
must be turned into manuscript prose.

**Process:**

1. Distinguish a socially important topic from an answerable research question.
2. Map the current literature, contradiction or blind spot; label a “gap” unverified until searched.
3. Specify unit, exposure/treatment, outcome, mechanism, comparison, scope conditions, and temporal order.
4. Generate competing explanations and falsifiers, not only confirmatory hypotheses.
5. Map every construct to observable data and likely coverage limitations.
6. Evaluate novelty, theoretical contribution, data access, identification, computation, ethics, and venue fit.

**Gate:** pass only when research gap, contribution, and feasibility are all explicit. A novel wording without new evidence or leverage is not a contribution.

## 2. Literature review and evidence matrix

**Route:** `research-lookup`, `literature-review`, `openalex-database`, `paper-lookup`, `zotero:Zotero`; use `citation-management` for bibliography audits.

**Process:**

1. Define review question, databases, fields, languages, years, document types, inclusion/exclusion rules, and search date.
2. Log exact queries and result counts. Preserve database-specific syntax.
3. Keep `candidate`, `screened-in`, `verified`, and `excluded` statuses separate.
4. Resolve DOI/title/author/year and stable source IDs; deduplicate before synthesis.
5. Verify evidence in the primary paper or authoritative record, not a search snippet.
6. Build an evidence matrix with study, setting, sample, constructs, methods, findings, limitations, relevance, verification status, and source locator.
7. Synthesize agreements, contradictions, boundary conditions, and missing evidence. Do not vote-count significance.

**Zotero/OpenAlex rule:** a topically relevant Zotero item may enter a candidate collection, but does not become verified evidence until identity and claim support are checked. Do not write to Zotero unless external write authority is explicit.

**Gate:** deliver search log, screening rules, evidence matrix, unresolved records, and coverage limits. Conclusions use verified rows only.

## 3. Scientometrics and cross-database citation networks

**Route:** `communication-network-analysis` for graph contracts and claims; use the
available scholarly metadata, citation-management, and coding tools for extraction and
execution.

**Entity and data contract:**

- record source-specific IDs; OpenAlex, Overton, ROR, DOI, ISSN, and local IDs are different namespaces;
- normalize names only for candidate discovery, never as the sole merge key;
- store entity type, parent/child hierarchy, country, domain, aliases, provenance, and match confidence (`exact`, `probable`, `ambiguous`, `no-match`);
- specify time window, date field, analysis unit, node types, edge direction, edge meaning, multiedge treatment, self-loop rule, and second-order citation policy;
- record pagination, API version/date, rate or access limits, missingness, duplicates, and coverage.

**Process:**

1. Resolve entities against authoritative platform records and, where useful, ROR or official institutional pages.
2. Freeze an ID crosswalk with provenance and confidence before building the graph.
3. Extract raw records read-only; retain request/query logs and retrieval timestamps.
4. Validate row counts, unique IDs, duplicates, broken references, coverage and date ranges.
5. Construct nodes and edges deterministically; test direction and weighting on a small known example.
6. Report network metrics with graph definition, component handling, normalization, and sensitivity choices.

**Gate:** do not report node counts, centrality, diffusion, or coverage as final while entity mappings or time boundaries remain ambiguous.

## 4. Project continuation

**Route:** use current Codex thread/history tools when available; use `session-logs` only after adapting its location/schema to the current Codex environment. Then route to the task-specific workflow.

**Process:**

1. Identify the unique project before acting. Use stated paths, saved state, recent artifacts, VCS status, scripts, inputs, outputs, and timestamps.
2. Treat historical text as context, not current truth. Re-open authoritative project files and latest results.
3. Restore task type, operation, authority, source-of-truth, sample/estimand, completed artifacts, last verification, unresolved issues, and next action.
4. If multiple plausible projects remain, present a short evidence-based candidate list and pause. Never pick the most recent directory by guess.
5. Continue from the smallest unverified step; do not rerun or rewrite completed work without reason.

**Gate:** no mutation until project root, authoritative inputs, and current stage are uniquely identified.
