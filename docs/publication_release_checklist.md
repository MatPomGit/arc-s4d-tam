# Publication and research-release checklist

Use this checklist before manuscript submission, dataset/model release or a public reproducibility package.

## Scientific scope

- [ ] Primary question and estimand match the frozen protocol.
- [ ] Confirmatory and exploratory analyses are separated.
- [ ] Null/negative results relevant to the question were not silently omitted.
- [ ] Claims match the actual evidence class and implementation maturity.
- [ ] Limitations and residual uncertainty are explicit.

## Evidence and provenance

- [ ] Dataset versions, cohort lists and checksums are frozen.
- [ ] Model/baseline artifacts are immutable and identified by checksum.
- [ ] Every reportable evidence bundle is in `research/evidence_registry.yaml`.
- [ ] Source commit, configuration, environment, hardware class and seeds are recorded.
- [ ] Failures/exclusions follow the frozen rule and are auditable.
- [ ] Primary tables/figures are generated from registered inputs.

## Statistical analysis

- [ ] Inferential unit is correct.
- [ ] Estimands, effect sizes and uncertainty intervals are explicit.
- [ ] Multiplicity handling follows the preregistration.
- [ ] Sensitivity and exploratory analyses are labeled.
- [ ] Analysis code regenerates publication artifacts without manual numerical transcription.

## Manuscript quality

- [ ] Title, abstract, conclusions and figures agree with the evidence.
- [ ] Terminology is consistent with `docs/terminology_glossary.md`.
- [ ] Every publication-facing citation was verified.
- [ ] No placeholder claims or unsupported precision remain.
- [ ] Equations, units, tables and captions are internally consistent.

## Authorship and declarations

- [ ] Author names/affiliations are final.
- [ ] CRediT roles reflect actual contributions.
- [ ] Funding, conflicts, acknowledgments and data/code availability statements are accurate.
- [ ] AI-assistance disclosure follows current venue policy.

## Safety, security and dual use

- [ ] No credentials/private infrastructure are present.
- [ ] Flight-readiness language does not imply certification that has not been established.
- [ ] Dual-use review was completed for released code/models/data.
- [ ] Physical-validation descriptions retain independent safety controller, geofence/abort and qualified-operator requirements.

## Release provenance

- [ ] Exact release commit/tag is recorded.
- [ ] `CHANGELOG.md` and `CITATION.cff` are current.
- [ ] Public artifacts have checksums and licenses.
- [ ] Reproduction instructions were tested from a clean environment or their untested scope is stated.
