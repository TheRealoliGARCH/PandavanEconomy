# Research protocol

## Objective

Evaluate the five-state absorbing Markov model and any policy or network extensions without changing the definition of the absorbing state.

## Workstream 1: Mathematical baseline

- Preserve the original state order: Peace, Experiment, War, Stagnation, Absorb.
- Preserve the original five-parameter transition matrix.
- Validate stochastic rows, the absorbing row, the fundamental matrix identity, absorption probabilities, and expected absorption times.
- Match numerical examples in the source paper independently.
- Keep any intervention model separate from the original model.

## Workstream 2: Operational state classification

Before collecting outcome data, specify observable rules for each transient state and for terminal absorption. Record ambiguity and classification confidence. Absorb must be defined by an entity-identity rule and remain absorbing in the modeled process. Any recorded return from Absorb requires investigation; it must not be silently recoded.

## Workstream 3: Genuine Nations sampling frame

The researcher's 2026 classification proposes a conservative 15-entity sample and a broader sensitivity sample of about 18–20 entities, based on the specified union of nuclear-armed entities and AAA-rated entities. Treat this as a theory-defined sampling frame, not a universally agreed geopolitical category.

Maintain a versioned roster with:
- stable entity identifier and name;
- nuclear-set membership indicator;
- credit-rating-set membership indicator;
- credit rating agency and reference date;
- inclusion rule and evidence provenance;
- primary versus sensitivity-sample designation.

Freeze a primary cohort for the initial study. Conduct a separate dynamic-membership analysis only after the fixed-cohort baseline is understood. Do not silently change membership with later rating changes.

## Workstream 4: Data dictionary and panel construction

For every series, record source, indicator code, unit, frequency, geographical coverage, period coverage, revision date, missingness, and transformation. Harmonize time frequency before constructing transitions. Annual observations may conceal multiple within-year transitions; state this limitation and examine alternatives when possible.

Keep bilateral network data separate from country-year covariates. A trade link does not automatically imply an alliance, and a two-way connection does not imply symmetric observed flows.

## Workstream 5: Estimation and model comparison

Compare at least:
1. the original constrained five-parameter model;
2. a reference Markov model with fewer structural restrictions;
3. a covariate-augmented model only if sample size and data coverage support it.

Evaluate transition prediction, probability calibration, finite-horizon absorption risk, parameter uncertainty, and leave-one-entity-out sensitivity. Sparse samples and rare absorbing events require cautious inference.

## Workstream 6: Intervention identification

Separate observed associations from causal effects. Do not interpret a state-conditional correlation as a policy effect without an identification strategy. Specify exactly which transition probabilities an intervention is permitted to change, why, and at what cost. Ensure row-stochasticity and retain an absorbing row for Absorb.

## Workstream 7: Network coupling

Construct a versioned bilateral graph with documented edge meaning and weight units. Test whether network variables improve out-of-sample prediction beyond baseline covariates. Improved prediction alone does not prove that increasing connectivity causes peace or lowers absorption risk; reverse causality and confounding must be considered.

## Reporting rules

- Identify synthetic calculations as model-generated.
- Do not report empirical results until the data are assembled and the code is run against them.
- Report sensitivity to sample definition, state classification, period, and single-entity removal.
- Preserve data source versions, code version, parameter configuration, and random seeds.
