# Computational social science (CSS) theory anchors

Companion to [theory-anchors.md](theory-anchors.md). Use these when the
phenomenon is a general social-science process (contagion, segregation,
collective action, attention, cultural evolution) rather than a
communication-specific mechanism. Each row states the mechanism, boundary
conditions, typical suitable evidence, and common misuse. This is a routing
aid, not a substitute for the original literature.

| Theory / mechanism | Mechanism | Boundary conditions | Suitable evidence | Common misuse |
|---|---|---|---|---|
| Threshold contagion (Granovetter) | A node adopts once the share of already-adopted neighbors exceeds a personal threshold | Discrete adoption; observable peer behavior; non-trivial social network | Temporal network plus adoption events; threshold estimation | Inferring contagion from similarity without separating homophily |
| Homophily / network closure (McPherson) | Similarity drives tie formation, concentrating attributes in connected groups | Needs longitudinal tie data to separate selection from influence | SIENA / ERGM / panel networks | Attributing similarity to social influence while selection is uncontrolled |
| Structural holes / brokerage (Burt) | Bridging otherwise disconnected groups yields informational and control advantage | Applies to information and brokerage benefits, less to dense-trust settings | Network position cross-referenced with outcomes | Equating any high centrality with brokerage advantage |
| Schelling segregation / tipping | Mild individual in-group preference aggregates into strong macro segregation | Threshold and bounded-rationality models; requires macro-micro link | ABM plus empirically estimated thresholds | Claiming individual prejudice from aggregate segregation alone |
| Social identity / intergroup | Salient group membership shifts evaluation of in-group vs out-group | Requires a salient, diagnostic group boundary | Experiments manipulating identity salience | Labeling any group difference as identity-driven |
| Polarization / echo chambers | Selective exposure and social feedback reinforce within-group opinion | Needs longitudinal and ideally cross-platform exposure data | Exposure-by-attitude panels; natural experiments | Claiming echo chambers from one cross-sectional platform snapshot |
| Collective action / public goods (Olson) | Free-rider logic predicts under-provision of public goods absent selective incentives | Assumes self-interested rationality; weak when strong norms or identity present | Game experiments; natural experiments; protest data | Ignoring selective incentives, norms, or identity |
| Cultural evolution / memetics | Variation-selection-retention of cultural items through transmission | Requires transmission dynamics, not mere popularity | Temporal diffusion data with content features | Calling any viral item a "meme" without a transmission model |
| Attention economy | Scarce attention is allocated across competing stimuli under platform incentives | Requires an attention measure, not only engagement counts | Clickstream, dwell time, eye tracking, field data | Equating likes/shares/engagement with attention |
| Computational grounded theory / abductive discovery | Iterative qualitative-quantitative pattern discovery from large corpora | Theory-building, not confirmatory; needs human-in-the-loop validity | Mixed-methods triangulation; member checks | Presenting post-hoc patterns as preregistered hypotheses |
| Complex contagion | Adoption requires reinforcement from multiple independent contacts | Most plausible for costly, contested, or identity-relevant behavior | Temporal networks with independent-path exposure; experiments varying reinforcement | Counting repeated exposures without checking source independence |
| Preferential attachment / cumulative advantage | Prior visibility or connectivity attracts further attention or ties | Growth process and opportunity set must be observed over time | Longitudinal network growth and exposure data | Explaining any skewed distribution as preferential attachment |
| Information cascades | Actors follow observed prior choices when private information is weak or hidden | Sequential decisions and observability of earlier choices are required | Ordered choice records, cascade experiments, event histories | Calling rapid diffusion a cascade without decision dependence |
| Bounded-confidence opinion dynamics | Actors update toward sufficiently similar opinions and ignore distant ones | Opinion distance, interaction opportunity, and update rules must be specified | Calibrated agent-based models and longitudinal opinion networks | Treating simulated polarization as proof of the human mechanism |
| Peer effects / social influence | Alters' prior behavior changes an actor's later behavior | Homophily, shared context, and simultaneity must be addressed | Randomized encouragement, longitudinal networks, valid instruments | Regressing ego on contemporaneous alter behavior and calling it influence |
| Path dependence / institutional feedback | Early choices create increasing returns and constrain later alternatives | Requires temporally ordered choices and a self-reinforcing mechanism | Historical process evidence, comparative sequences, policy/institutional panels | Using history as an explanation without a feedback mechanism |
| Network externalities | The value or cost of participation changes with the number or composition of other users | Requires an interaction-dependent payoff, not popularity alone | Adoption panels, platform experiments, structural demand or diffusion models | Treating user growth as evidence that network effects caused growth |

## Using this table

1. Match by mechanism, never by keyword.
2. Copy the boundary conditions into the theory memo.
3. If a communication-specific row in [theory-anchors.md](theory-anchors.md)
   fits better, use it; the two tables are complementary, not competing.
4. If no row fits, search the original literature for the mechanism instead
   of forcing a label.
