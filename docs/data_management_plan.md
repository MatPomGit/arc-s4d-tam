# Data management plan

Status: canonical data-governance plan for S4D-TAM research artifacts.

## Scope

This plan covers public datasets, converted benchmark inputs, calibration artifacts, model weights, external-baseline outputs, synthetic/SIL/HIL/controlled-flight logs and publication-facing result bundles.

## Data classes

| Class | Examples | Repository policy |
| --- | --- | --- |
| Source datasets | TartanAir, Blackbird, MARSIM, AeroVerse | Do not redistribute unless licensing explicitly permits it. Store source/version identifiers and checksums. |
| Converted inputs | normalized sequences/manifests | Version conversion code and schema; archive immutable manifests and hashes for reportable runs. |
| Model artifacts | full model, H1-H7 ablations, calibration objects | Store immutable identifiers, provenance and SHA-256; large artifacts may live outside Git with a durable reference. |
| Execution outputs | AlgorithmResult, failures, telemetry, timing | Package as immutable evidence bundles; register in `research/evidence_registry.yaml`. |
| Publication artifacts | tables, figures, reports | Generate from registered inputs; do not manually transcribe primary numerical results. |

## Provenance minimum

Every reportable run must identify:

- source commit;
- configuration path and hash;
- dataset manifest and source version;
- model/baseline artifact identity and hash;
- environment/container identity;
- random seed(s);
- hardware class where performance metrics are reported;
- start/end timestamps;
- analysis code commit;
- output artifact checksums.

## Integrity and storage

Use SHA-256 for immutable research artifacts. Raw and converted data must not be overwritten in place once referenced by confirmatory evidence. Generated output under `outputs/` is transient unless promoted into a registered evidence bundle.

Large artifacts should be stored in a durable external archive or release asset with an immutable identifier. The repository records metadata and checksums, not secrets or local infrastructure credentials.

## Train/calibration/test separation

Training, calibration and final test cohorts must remain distinct. Test or locked holdout observations must not drive feature engineering, threshold selection, map construction, hyperparameter tuning or stopping decisions.

## Missing and failed runs

Failures, timeouts, aborts and protocol-defined exclusions are data. Record them with reason codes; do not silently delete or replace them after outcome inspection.

## Retention and release

Retain the exact evidence bundle used for a publication together with source/config/environment metadata for the lifetime of the associated result. Before public release, re-check dataset/model licenses, privacy, security and dual-use constraints.

## Privacy and sensitive information

Do not commit credentials, IP addresses, private infrastructure details or personally identifying data. If controlled physical validation produces sensitive logs, publish only the minimum de-identified research artifact needed for reproducibility.
