# Communication research router

Read this reference first when a communication research request arrives. Its job is to classify the request before any contract or method choice, then map it to a registered planner archetype and the smallest specialist Skill stack.

## Step 1: name the phenomenon and the goal

Extract the object (journalism, platform, HMC, public opinion, audience, discourse) and the research goal:

| Goal | What is being claimed | What is not yet claimed |
|---|---|---|
| Description | What exists, how it is distributed | Why it exists |
| Measurement | A construct is validly measured | The measured level has causes |
| Explanation | A mechanism links constructs | The mechanism is identified causally |
| Prediction | Outcomes can be anticipated in new data | The predictors cause the outcome |
| Causal identification | A specific intervention changes the outcome | The effect generalizes beyond the design |
| Simulation explanation | Micro rules can reproduce macro patterns | The rules are the true ones |

## Step 2: choose the route

Do not let the available data choose the route. Representative examples:

| Request shape | Planner archetype | Specialist Skills |
|---|---|---|
| AI-byline / disclosure / trust survey experiment | `experiment` | communication-experiment, communication-construct, communication-scale, communication-reviewer |
| Audience survey or panel with scales | `survey` | communication-scale, communication-construct |
| Technical-term circulation across platforms | `text-computational` | communication-content-analysis, communication-method-router |
| Platform posts, news corpus, LLM-assisted coding | `text-computational` | communication-content-analysis |
| Diffusion, cascades, network opinion | `network` | communication-network-analysis, communication-temporal-analysis |
| Platform or policy intervention | `causal-policy-evaluation` | communication-causal-inference |
| Longitudinal communication process | `temporal` | communication-temporal-analysis |
| Image, video, audio, or cross-modal meaning | `multimodal` | communication-multimodal-analysis |
| Geographic communication pattern or diffusion | `spatial` | communication-spatial-analysis |
| Generative/agent-based simulation of publics | `simulation` | communication-simulation |
| Interviews/case selection | `qualitative` | communication-theory, communication-reviewer |
| Multi-strand project | `mixed-methods` | communication-method-router, communication-reviewer |

## Step 3: attach gates

The gates fire at fixed transitions, not at the end:

- Theory Gate before RQ/H finalization.
- Construct Gate before operationalization.
- Measurement Gate before fielding or coding.
- Design/Identification Gate before data collection.
- Novelty Gate before writing the contribution.
- Contribution Gate before drafting discussion.
- Evidence-to-Claim Gate before every empirical claim is written.

Assign audit rigor (`audit`) when the task claims causality, compares groups across languages/cultures, uses simulation as evidence, or prepares a submission.

## Step 4: decide what is not routed

- If full text/PDFs are needed, add `scholarly-access` to the stack. It never downloads without the user's authorization and never uses plaintext credentials.
- If the request is not research (single PDF summary, generic coding, formatting), return the mismatch and do not open a contract.
- If the communication object is ambiguous between journalism, platform, and HMC, pause on that ambiguity instead of guessing the venue and the evidence type.
- If the available methods cannot support the goal (e.g., cross-sectional data claimed as causal, one corpus claimed as general public meaning), mark `needs-specialist` and return the capability gap.

## Route output

Finish with one short paragraph and a compact table:

1. phenomenon and goal class;
2. archetype and specialist stack;
3. the single most consequential gate for this project;
4. open decisions that block contract finalization, if any.
