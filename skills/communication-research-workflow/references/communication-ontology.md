# Communication research ontology

Read this reference when the request concerns communication, media, platforms, audiences, journalism, or human-machine interaction and you need to place the work on the research reasoning graph before opening task contracts.

## Reasoning graph

Communication research generally progresses in this order. Record where the request starts and what must be locked before the next transition:

```text
Phenomenon -> Literature -> Theory -> Construct -> Mechanism
  -> RQ/H -> Operationalization -> Measurement -> Design/Identification
  -> Evidence -> Theoretical contribution
```

Each transition has a gate. The most consequential boundaries:

- **Phenomenon to Theory**: describe the phenomenon precisely enough that several theories could explain it. If only one theory's keywords match the topic, the phenomenon is under-specified.
- **Theory to Construct**: extract only the constructs the theory's mechanism requires; do not import every adjacent construct from the literature.
- **Construct to Measurement**: lock one definition before selecting a scale; a measure does not define a construct.
- **Evidence to Contribution**: the finding must change an inference the field could not previously make, not merely repeat an established effect in a new context without a boundary revision.

## Typical research objects

Use these objects to disambiguate a request, never as a fixed taxonomy:

- **Journalism and news**: authorship, sourcing, verification, disclosure, institutional trust, editorial accountability, news production and labor.
- **Platform and media systems**: algorithms, recommender systems, moderation, platform dependence, metrics, virality, visibility.
- **Human-machine communication (HMC)**: AI agents, chatbots, disclosure cues, perceived humanness, machine agency, AI-mediated attribution.
- **Publics and opinion**: agenda setting, public discourse, echo chambers, polarization, issue publics, deliberation.
- **Social influence and networks**: diffusion, cascades, network structure, influence measurement.
- **Audience and effects**: attention, persuasion, trust, credibility, emotion, behavior.
- **Technical discourse and meaning**: how technical terms travel, get re-semanticized, and become scripts of anxiety, self-discipline, or aspiration.

## Evidence types that count

Evidence is not limited to survey coefficients. The ontology accepts, when design and claim are aligned:

- audience experiments and survey experiments, including HMC manipulations;
- large-scale content and platform-trace analysis with audited sampling;
- network and diffusion analyses with locked graph boundaries;
- temporal, event-history, sequence, and panel analyses with a locked clock and risk set;
- visual, audio, video, and multimodal analyses with extraction and human-validation evidence;
- spatial communication analyses with geocoding uncertainty and ecological boundaries;
- generative/agent-based simulation treated as an instrument whose calibration is itself measured;
- qualitative and comparative designs with transparent case selection;
- measurement work whose contribution is psychometric or cross-cultural.

## When the graph is misordered

Common failures this reference is designed to catch:

- starting from a dataset or method ("we have platform posts, so topic model") and reverse-engineering the question;
- moving from a label ("AI impact") directly to an experiment without a mechanism;
- claiming a theoretical contribution from a single convenience sample with no boundary argument;
- using frequency or prediction accuracy as if it established meaning, causality, or hegemony.

## Relationship to specialist Skills

This ontology feeds the communication router and skill registry. The seven domain gates (Theory, Construct, Measurement, Design/Identification, Novelty, Contribution, Evidence-to-Claim) are each owned by a specialist Skill; the orchestrator calls them at the transitions above rather than only at the end.
