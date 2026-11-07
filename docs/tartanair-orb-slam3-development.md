# TartanAir + ORB-SLAM3 development vertical slice

This manual runbook defines the first end-to-end development comparison. The canonical checkpointed path is `docs/tartanair-orb-slam3-automation.md`; prefer that path for end-to-end execution. TartanAir V1 is simulated AirSim data, not physical-flight evidence.

It is deliberately restricted to one dataset and one independent external baseline:

- dataset: TartanAir V1-compatible converted cohort;
- candidate: `s4d_tam_reference`;
- baseline: ORB-SLAM3;
- phase: `development`;
- experiment: `configs/experiments/tartanair_orb_slam3_development.yaml`.

Results from this run are engineering/development evidence only. They must not be reported as confirmatory hypothesis tests.

## 1. Repository health

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest
s4dtam-bench validate-comparison configs/experiments/tartanair_orb_slam3_development.yaml
```

## 2. Convert and preflight the selected TartanAir cohort

Set the exact upstream location and a sampling frequency verified for that release:

```bash
export TARTANAIR_SOURCE=/absolute/path/to/tartanair-v1
export TARTANAIR_FPS=<VERIFIED_FPS>

s4dtam-bench convert-tartanair \
  "$TARTANAIR_SOURCE" \
  data/raw/tartanair-converted \
  --fps "$TARTANAIR_FPS" \
  --link-mode symlink

s4dtam-bench preflight-tartanair data/raw/tartanair-converted
```

Do not guess `TARTANAIR_FPS`; the V1 `pose_left.txt` source does not carry timestamps and the declared sampling rate enters the trajectory time base.

## 3. Freeze the cohort

```bash
mkdir -p artifacts/manifests/tartanair
s4dtam-bench freeze-tartanair \
  data/raw/tartanair-converted \
  artifacts/manifests/tartanair/frozen \
  --raw-root "$TARTANAIR_SOURCE"

cat artifacts/manifests/tartanair/frozen/sequence-list.txt
cat artifacts/manifests/tartanair/frozen/freeze.json
```

The ORB-SLAM3 run and S4D-TAM evaluation must use exactly this frozen sequence list.

## 4. Prepare deterministic ORB-SLAM3 inputs

Generate the exact `mono_tum` input lists and per-sequence camera settings from the converted TartanAir descriptors:

```bash
s4dtam-bench prepare-orb-slam3-tartanair \
  data/raw/tartanair-converted \
  artifacts/baseline-inputs/orb_slam3/tartanair
```

For every converted sequence this produces:

```text
artifacts/baseline-inputs/orb_slam3/tartanair/<sequence-id>/
  rgb.txt
  settings.yaml
  input-manifest.json
```

`rgb.txt` uses the official ORB-SLAM3 `mono_tum` timestamp/path convention. `settings.yaml` is generated from the camera calibration and `declared_fps` stored in that sequence's `sequence.json`, rather than copying calibration from a TUM or EuRoC example. `input-manifest.json` records SHA-256 hashes for the source descriptor, RGB list and generated settings.

Inspect the prepared inputs before execution:

```bash
find artifacts/baseline-inputs/orb_slam3/tartanair -type f -print | sort
```

## 5. Reproduce the pinned ORB-SLAM3 implementation

The baseline specification is `configs/algorithms/orb_slam3.yaml`. The repository pins the upstream revision and its source-build identity; the `container` field is retained for schema compatibility and is not a Docker digest. Follow `docs/tartanair-orb-slam3-automation.md` to build the pinned runner and check its actual binary and vocabulary hashes.

```bash
python - <<'PY'
from s4dtam_benchmark.config import load_yaml
cfg = load_yaml("configs/algorithms/orb_slam3.yaml")
print("upstream:", cfg["upstream"])
print("revision:", cfg["revision"])
print("container:", cfg["container"])
PY
```

The official upstream monocular entry point is typically invoked as follows, but the repository's verified frame-wise runner is the required implementation for this benchmark:

```text
mono_tum path_to_vocabulary path_to_settings path_to_sequence
```

The prepared sequence directory provides the last two experiment-specific inputs (`settings.yaml` and `rgb.txt` under `path_to_sequence`). The pinned external implementation must still be executed for every sequence on the frozen list, and its raw trajectory/timing output must be converted into the normalized S4D-TAM result artifact. Input preparation alone is not baseline reproduction evidence.

Expected normalized outputs:

```text
outputs/baselines/orb_slam3/tartanair/<sequence-id>.npz
```

Each output must satisfy the repository `s4dtam-algorithm-result-npz/v1` contract and include trajectory timing plus recorded resource information required by the baseline-evidence validator.

## 6. Freeze baseline evidence

Create run metadata containing the actual hardware and exact executed command, then validate the complete frozen cohort:

```bash
s4dtam-bench validate-baseline-evidence \
  orb_slam3 \
  tartanair \
  artifacts/manifests/tartanair/frozen/sequence-list.txt \
  outputs/baselines/orb_slam3 \
  configs/algorithms/orb_slam3.yaml \
  artifacts/baselines/orb-slam3-tartanair-run.json \
  artifacts/baselines/evidence
```

This gate must fail if any frozen sequence is missing, an unexpected output appears, the implementation is not pinned, or run metadata are incomplete.

## 7. Execute the common comparison

Only after baseline evidence validates:

```bash
s4dtam-bench validate-comparison \
  configs/experiments/tartanair_orb_slam3_development.yaml

s4dtam-bench run \
  configs/experiments/tartanair_orb_slam3_development.yaml
```

Expected publication-pipeline output root:

```text
outputs/tartanair_orb_slam3_development/
```

Both systems are evaluated through the same evaluator and reporting path.

## 8. Development acceptance criteria

The vertical slice is complete only when all of the following are true:

1. the TartanAir cohort passes conversion and strict preflight;
2. its sequence list and files are frozen with SHA-256 evidence;
3. deterministic ORB-SLAM3 `rgb.txt`, settings and input manifests are generated for every frozen sequence;
4. the pinned ORB-SLAM3 implementation has produced one valid normalized artifact for every frozen sequence;
5. `validate-baseline-evidence` passes;
6. `validate-comparison` passes for the dedicated development configuration;
7. the common evaluator completes without silent metric imputation;
8. generated tables/plots can be traced to immutable input and baseline evidence.

Completion of this run does not unlock confirmatory H1-H7 testing. The full confirmatory external matrix, learned-model freeze, preregistered ablations and field/field-analog validation remain separate publication gates.
