# Experiment naming and identifiers

Use stable, outcome-independent identifiers for all reportable executions.

## Study IDs

Recommended study IDs:

- `EXT`: external complete-system comparison;
- `ABL`: internal H1-H7 ablation family;
- `SIL`: software-in-the-loop validation;
- `HIL`: hardware-in-the-loop validation;
- `FLT`: controlled real-flight validation;
- `REPRO`: independent reproduction.

These labels classify evidence and do not imply readiness.

## Session ID

Use:

`S4D__<study>__<dataset-or-cohort>__<phase>__<YYYYMMDD>__runNNN`

Example:

`S4D__ABL__tartanair-frozen01__confirmatory__20261001__run001`

Allowed phases include `development`, `pilot`, `confirmatory`, `sil`, `hil`, `controlled-flight` and `reproduction`.

## Trial ID

Append:

`__trialNNNN`

## Evidence ID

Use:

`EV__<session-id>__<short-commit>`

Register reportable evidence IDs in `research/evidence_registry.yaml`.

## Do not encode

Do not encode measured outcomes, hypothesis support, private machine names, IP addresses, credentials or hardware serial numbers in IDs. Put those details, where appropriate, in structured metadata.
