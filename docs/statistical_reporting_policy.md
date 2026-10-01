# Statistical reporting policy

Status: reporting and inference policy subordinate to the frozen preregistration where the two overlap.

## Inferential unit

Use mission/sequence-level inference for primary navigation comparisons. Repeated frames, timestamps or tokens are not independent replicates. Repeated seeds within a scenario must be represented in a way that preserves the paired/hierarchical design.

## Primary reporting

For each primary outcome report:

- estimand and direction;
- sample size at the inferential unit;
- point estimate;
- uncertainty interval;
- effect size in interpretable units;
- exact analysis procedure;
- multiplicity handling when applicable;
- number and reasons for failures/exclusions;
- evidence class and frozen protocol reference.

Do not report p-values without corresponding effect estimates and uncertainty.

## H1-H7 family

The preregistered H1-H7 decisions, primary endpoints, multiplicity handling and H7 non-inferiority criterion are authoritative in `docs/preregistration.md`. They must not be changed after outcome inspection.

## Paired comparisons

Preserve paired sequence/scenario/seed structure whenever the protocol defines it. If a pair is broken, report the reason and use only a prespecified missing-data rule or label the alternative analysis exploratory.

## Bootstrap and resampling

Resample at the inferential unit, not at the frame level. Preserve pairing when estimating paired effects.

## Missing data and failures

Unavailable ground truth means the metric is unavailable, not zero. Algorithm failure, timeout, collision or abort remains in protocol-defined denominators unless an exclusion rule explicitly applies.

## Multiplicity

Primary confirmatory families use the correction specified by the preregistration. Secondary/sensitivity analyses must state whether they are multiplicity-adjusted and must not silently replace the primary decision rule.

## Exploratory analyses

Post hoc subgrouping, alternative endpoints, threshold tuning or model-selection analyses are exploratory unless independently preregistered before accessing the relevant outcome data.

## Numerical precision

Report only precision supported by measurement and computation. Units must be explicit. Avoid treating tiny numerical differences as scientifically meaningful without uncertainty and practical-effect context.
