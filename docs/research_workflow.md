# Research workflow

This workflow separates software readiness from scientific evidence.

## Canonical progression

1. **Specify**: define the question, estimand, metrics, comparison cell and evidence class.
2. **Register**: freeze the relevant protocol/configuration and record the commit/hash.
3. **Prepare inputs**: verify dataset version, checksums, sensor compatibility, calibration and environment.
4. **Execute**: run from version-controlled configuration without manual outcome-dependent edits.
5. **Package evidence**: record outputs, failures, exclusions, environment and checksums.
6. **Analyze**: run the predefined statistical procedure at the correct inferential unit.
7. **Register evidence**: add the immutable bundle to `research/evidence_registry.yaml`.
8. **Map claims**: connect manuscript claims to evidence in `research/claim_ledger.yaml`.
9. **Write**: distinguish established literature, S4D-TAM hypotheses, simulation results and real validation.
10. **Release**: run the publication/research-release checklist and archive the exact release state.

## State control

Read `PROJECT_STATE.yaml` before treating the project as ready for a new evidence class. A green CI run means software checks passed; it does not promote offline work to SIL, HIL, real-flight or independent-reproduction evidence.

## Deviations

Any post-freeze departure from a protocol belongs in `research/deviations/`. State whether it occurred before or after outcome inspection and whether confirmatory interpretation remains valid.

## Decisions

Use `docs/adr/` or `research/decisions/` for consequential choices. Do not change a frozen hypothesis or endpoint merely because an observed result is unfavorable.

## Negative results

Preserve scientifically valid null/negative findings in `research/negative_results.md`. Publication-facing summaries must not selectively omit valid evidence solely because it does not support the proposed mechanism.
