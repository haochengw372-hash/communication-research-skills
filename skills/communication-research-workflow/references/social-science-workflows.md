# Social-science empirical workflow router

## Contents

1. Applicability
2. Universal lifecycle
3. Study archetype router
4. Shared social-science gates
5. Scope limits

## 1. Applicability

Use this router for empirical social-science projects, including quantitative, computational, qualitative, and mixed-methods work. Treat it as a governance layer, not a substitute for domain theory, ethics review, qualitative expertise, statistical expertise, or specialist Skills.

The workflow is strongest for data-intensive and multi-stage research. Small one-step tasks may use a narrower Skill without project governance.

## 2. Universal lifecycle

1. Establish project identity, authority, ethics, and decision ownership.
2. Refine the research question, theory, mechanism, rival explanations, contribution, and feasibility.
3. Build a verified literature evidence matrix.
4. Define constructs, measurements, units, timing, population, sample, comparison, and scope conditions.
5. Lock the design, data-governance rules, estimand or interpretive aim, and analysis plan.
6. Audit data provenance, sampling, keys, missingness, exclusions, and transformations.
7. Separate exploratory work from confirmatory or final interpretive work.
8. Execute the appropriate analysis with diagnostics, uncertainty, negative cases, and robustness.
9. Independently audit consequential results and evidence-to-claim links.
10. Generate tables, figures, and prose from the same accepted evidence.
11. Audit citations, reporting requirements, and the final submission version.

## 3. Study archetype router

| Archetype | Required design additions | Typical audit focus |
|---|---|---|
| Cross-sectional observational | confounding, selection, temporality, missingness, proxy validity | causal-language limits and adjustment rationale |
| Panel or longitudinal | unit/time structure, attrition, dependence, fixed/random effects, dynamics | clustering, lag choices, time-varying confounding |
| Causal policy evaluation | treatment timing, counterfactual, estimand, spillovers, anticipation, parallel trends or design-specific assumptions | independent identification audit before estimation |
| Survey | sampling frame, instrument, pilot, reliability, construct validity, nonresponse, weights | scale quality, measurement invariance, common-method risk |
| Experiment | randomization, allocation, manipulation, power, attrition, exclusions, outcome registration | protocol deviations, imbalance, multiplicity |
| Text or computational | corpus boundary, annotation, intercoder agreement, leakage, construct validation, drift | labels-to-construct validity and reproducibility |
| Network | network boundary, node/edge meaning, direction, weight, temporality, missing ties | sensitivity to graph construction choices |
| Temporal process | clock, interval, risk set, lag, censoring, attrition, aggregation | dependence, temporal-resolution and timing claims |
| Multimodal | media sampling, frame/scene/speaker units, extraction error, cross-modal relations | human validation, modality loss, model and subgroup bias |
| Spatial | geocoding, spatial unit, CRS, joins, weights, privacy, MAUP | ecological claims, uncertainty, scale and neighborhood sensitivity |
| Simulation | agents, micro-rules, topology, schedule, parameters, calibration and validation split | code verification, equifinality, seeds, held-out human evidence |
| Predictive | prediction time, target, splits, leakage, baseline, calibration, external validation | out-of-sample validity and intended use |
| Qualitative | sampling logic, consent, positionality, reflexivity, codebook, negative cases, saturation or information power | evidence locators, coding decisions, transferability |
| Mixed methods | design type, strand priority/timing, integration point, discordant evidence | legitimacy of meta-inferences and non-forced convergence |

Select the archetype from the research question and evidence needed, not from the software or method the researcher hopes to use. A project may have a primary archetype and secondary branch; record both and define where they integrate.

## 4. Shared social-science gates

### Question and contribution

- Distinguish social importance from an answerable question.
- Verify the claimed gap; do not equate new wording or a new dataset with theoretical contribution.
- State mechanisms, competing explanations, falsifiers, scope conditions, and feasible evidence.

### Constructs and measurement

- Separate a construct from its proxy.
- Record reliability, validity, coding, timing, unit, and plausible measurement error.
- Do not let available variables silently redefine the research question.

### Sampling and ethics

- Record target population, sampling frame, inclusion/exclusion, representativeness, attrition, and weights.
- Apply applicable ethics, consent, privacy, data-use, and vulnerable-population rules before collection or linkage.
- Never place personally identifying data, credentials, or protected raw data in project-control files.

### Inference

- Define the estimand for quantitative confirmatory work or the interpretive aim for qualitative work.
- Match causal language to design and assumptions.
- Report uncertainty, practical importance, diagnostics, sensitivity, negative cases, and limitations.
- Preserve adverse results; do not select models, samples, or outcomes by desired significance.

### Communication

- Link every major claim to verified literature, accepted analysis output, or clearly labeled interpretation.
- Keep exploratory findings labeled as exploratory.
- Use reporting guidance appropriate to the design and venue; verify current requirements rather than assuming one universal checklist.

## 5. Scope limits

Do not claim universal coverage. Obtain additional specialist review for high-risk clinical studies, regulated human-subject research, advanced ethnography, sensitive fieldwork, historical-archival interpretation, formal theory, legal analysis, or domain-specific measurement when the available Skills and materials are insufficient.

The controller should mark such gaps as `needs-specialist` rather than forcing the project through an unsuitable quantitative template.
