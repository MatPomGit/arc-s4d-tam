# Research-quality TODO

This file tracks cross-cutting research-engineering work. Scientific hypotheses and frozen protocol decisions remain authoritative in the dedicated protocol documents.

## Evidence readiness

- [ ] Freeze source dataset versions, sequence lists and SHA-256 manifests.
- [ ] Record sensor-compatibility decisions for every external comparison cell.
- [ ] Execute and archive reproducible external-baseline evidence rather than treating pins as evidence.
- [ ] Freeze the final trained full-model artifact and H1-H7 artifacts.
- [ ] Complete the confirmatory-freeze package without placeholders.
- [ ] Execute confirmatory offline analyses from frozen inputs.
- [ ] Package all primary results with provenance, failures, exclusions and checksums.

## Reproducibility

- [ ] Verify clean-environment reproduction for at least one public dataset and one external baseline.
- [ ] Archive exact environment/container digests for publication-facing runs.
- [ ] Confirm deterministic seed handling where deterministic behavior is claimed.
- [ ] Record deviations from frozen protocols under `research/deviations/`.
- [ ] Register reportable evidence bundles in `research/evidence_registry.yaml`.
- [ ] Link manuscript claims to evidence in `research/claim_ledger.yaml`.

## Scientific reporting

- [ ] Complete literature search logs for each major claim family.
- [ ] Verify bibliographic metadata against primary/publisher sources before submission.
- [ ] Preserve null and negative findings in `research/negative_results.md`.
- [ ] Complete CRediT roles before submission.
- [ ] Run the publication/release checklist for every manuscript or reproducibility release.

## Validation progression

- [ ] SIL validation after confirmatory offline readiness.
- [ ] HIL validation after SIL readiness.
- [ ] Controlled real-flight validation only after independent operational safety gates are satisfied.
- [ ] Independent reproduction package tested by a clean-room user/environment.
