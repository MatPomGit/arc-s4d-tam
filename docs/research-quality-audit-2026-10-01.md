# Research-quality audit — 2026-10-01

Reference repository: `MatPomGit/arc-hri-safety`.

## Existing strengths

Before this audit S4D-TAM already contained executable benchmark contracts, dataset/baseline configurations, extensive tests, CI and CodeQL, container specifications, a preregistration, readiness gates, reproducibility documentation, SIL/HIL/physical-validation protocols, artifact schemas, a canonical manuscript and an independent-reproduction package.

## Gaps identified

The principal gaps were governance rather than algorithmic implementation:

- no machine-readable global project state;
- no explicit cross-project TODO tied to evidence readiness;
- no claim-to-evidence ledger or evidence registry;
- no protocol-deviation and decision-record structure;
- no dedicated data-management plan;
- no standalone statistical-reporting policy;
- no literature-search log/policy;
- no explicit authorship/CRediT policy;
- no common experiment/session/evidence ID convention;
- no central scientific and reproducibility risk register;
- no dedicated responsible-use release governance;
- no CI check for research-governance artifacts.

## Remediation

The repository now includes the above records, documentation and a static governance audit. These controls improve traceability and reproducibility; they do not themselves create scientific evidence or guarantee research validity.

## Non-modification rule

The frozen H1-H7 preregistration and scientific decision criteria were not changed by this governance audit.
