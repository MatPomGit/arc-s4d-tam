#!/usr/bin/env python3
"""Reproduce and evaluate the pinned ORB-SLAM3 baseline on frozen TartanAir V1 data.

This intentionally does NOT claim a complete comparison with S4D-TAM.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from s4dtam_benchmark.algorithms.external import parse_external_artifact
from s4dtam_benchmark.baseline_evidence import validate_and_freeze_baseline_evidence
from s4dtam_benchmark.config import load_yaml
from s4dtam_benchmark.datasets import TartanAirDataset
from s4dtam_benchmark.evaluation import evaluate_result
from s4dtam_benchmark.tartanair_orb_pipeline import _verify_frozen_files


REPO_ROOT = Path(__file__).resolve().parents[2]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _validated_input(directory: Path, sequence_id: str) -> None:
    manifest_path = directory / "input-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("sequence_id") != sequence_id:
        raise ValueError(f"ORB input sequence mismatch: {sequence_id}")
    for key, hash_key in (
        ("rgb_list", "rgb_list_sha256"),
        ("settings", "settings_sha256"),
        ("source_sequence_descriptor", "source_sequence_descriptor_sha256"),
    ):
        candidate = (directory / manifest[key]).resolve()
        if not candidate.is_file() or _sha256(candidate) != manifest[hash_key]:
            raise ValueError(f"ORB input checksum mismatch: {key} ({sequence_id})")
    settings = (directory / "settings.yaml").read_text(encoding="utf-8")
    if "Camera.RGB: 0" not in settings.splitlines():
        raise ValueError(f"ORB-SLAM3 requires OpenCV BGR settings: {sequence_id}")


def run_baseline(work: Path, expected_freeze_sha256: str, output_dir: Path) -> dict[str, Any]:
    work = work.resolve()
    output_dir = output_dir.resolve()
    converted = work / "converted"
    raw = work / "raw"
    frozen = work / "freeze"
    prepared = work / "orb-inputs-bgr"
    build = work / "orb-build"
    prefix = work / "local"

    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"Refusing to overwrite existing experiment output: {output_dir}")

    freeze = json.loads((frozen / "freeze.json").read_text(encoding="utf-8"))
    if freeze.get("file_manifest_sha256") != expected_freeze_sha256:
        raise ValueError("Requested frozen cohort SHA-256 does not match freeze.json")
    _verify_frozen_files(converted, frozen, raw)

    sequence_ids = [
        line.strip() for line in (frozen / "sequence-list.txt")
        .read_text(encoding="utf-8").splitlines() if line.strip()
    ]
    if not sequence_ids or len(sequence_ids) != len(set(sequence_ids)):
        raise ValueError("Invalid or duplicate frozen sequence IDs")
    dataset = {item.sequence_id: item for item in TartanAirDataset(converted).sequences()}
    if set(dataset) != set(sequence_ids):
        raise ValueError("Converted cohort does not exactly match frozen sequence list")

    pangolin_manifest = prefix / "pangolin-build-manifest.json"
    orb_manifest = build / "build-manifest.json"
    if not pangolin_manifest.is_file() or not orb_manifest.is_file():
        raise FileNotFoundError("Verified Pangolin and ORB-SLAM3 build manifests are required")

    algorithm_config = REPO_ROOT / "configs/algorithms/orb_slam3.yaml"
    pin = load_yaml(algorithm_config)
    if json.loads(orb_manifest.read_text(encoding="utf-8")).get("revision") != pin["revision"]:
        raise ValueError("ORB-SLAM3 build revision differs from pinned algorithm config")

    # Check all inputs before starting any baseline execution.
    for sequence_id in sequence_ids:
        _validated_input(prepared / sequence_id, sequence_id)

    result_root = output_dir / "results"
    commands: list[str] = []
    metrics: dict[str, dict[str, float | None]] = {}
    unavailable: dict[str, list[str]] = {}
    tracking_counts: dict[str, dict[str, int]] = {}

    for sequence_id in sequence_ids:
        target = result_root / "tartanair" / f"{sequence_id}.npz"
        cmd = [
            sys.executable,
            str(REPO_ROOT / "tools/orb_slam3/run_sequence.py"),
            "--runner", str(build / "bin/s4dtam_orb_slam3_runner"),
            "--vocabulary", str(build / "ORBvoc.txt"),
            "--build-manifest", str(orb_manifest),
            "--settings", str(prepared / sequence_id / "settings.yaml"),
            "--sequence", str(prepared / sequence_id),
            "--output", str(target),
        ]
        print(">>>", shlex.join(cmd), flush=True)
        subprocess.run(cmd, check=True, cwd=REPO_ROOT)
        commands.append(shlex.join(cmd))

        result = parse_external_artifact(target, "orb_slam3")
        observed_metrics, absent = evaluate_result(dataset[sequence_id], result)
        metrics[sequence_id] = {
            key: float(value) if math.isfinite(float(value)) else None
            for key, value in observed_metrics.items()
        }
        unavailable[sequence_id] = absent
        valid = result.metadata.get("tracking_valid")
        tracking_counts[sequence_id] = {
            "frames": len(result.timestamps),
            "tracking_valid": sum(valid) if valid is not None else len(result.timestamps),
        }

    output_dir.mkdir(parents=True, exist_ok=True)
    metadata = {
        "baseline": "orb_slam3",
        "dataset": "tartanair",
        "revision": pin["revision"],
        "container": pin["container"],
        "input_manifest_sha256": expected_freeze_sha256,
        "hardware": {
            "platform": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor() or "unknown",
            "cpu_count": os.cpu_count(),
        },
        "command": " && ".join(commands),
        "sequence_commands": commands,
        "executed_utc": datetime.now(timezone.utc).isoformat(),
        "study_phase": "development",
        "fps_source_verified": False,
        "pangolin_build_manifest_sha256": _sha256(pangolin_manifest),
        "orb_slam3_build_manifest_sha256": _sha256(orb_manifest),
    }
    metadata_path = output_dir / "run-metadata.json"
    metadata_path.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    evidence = validate_and_freeze_baseline_evidence(
        baseline="orb_slam3",
        dataset="tartanair",
        sequence_list=frozen / "sequence-list.txt",
        result_root=result_root,
        config_path=algorithm_config,
        run_metadata_path=metadata_path,
        output_dir=output_dir / "evidence",
    )

    summary: dict[str, Any] = {
        "schema": "s4dtam-orb-slam3-development-baseline/v1",
        "study_phase": "development",
        "comparison_completed": False,
        "fps_source_verified": False,
        "frozen_manifest_sha256": expected_freeze_sha256,
        "baseline_evidence_sha256": evidence.evidence_sha256,
        "sequences": sequence_ids,
        "tracking_counts": tracking_counts,
        "metrics": metrics,
        "unavailable_metrics": unavailable,
        "repo_commit": subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT, text=True, capture_output=True, check=True
        ).stdout.strip(),
    }
    (output_dir / "baseline-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--expected-freeze-sha256", required=True)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    output = args.output or args.work / "orb-baseline-development"
    report = run_baseline(args.work, args.expected_freeze_sha256, output)
    for sequence_id, values in report["tracking_counts"].items():
        print(f"ORB-SLAM3 {sequence_id}: valid={values['tracking_valid']}/{values['frames']}")
    print("Baseline reproduction evidence:", output / "evidence")
    print("Standalone ORB baseline finished; two-algorithm comparison NOT complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
