from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from s4dtam_benchmark.datasets import TartanAirDataset
from s4dtam_benchmark.tartanair_ingestion import convert_tartanair_v1, freeze_tartanair_cohort


def _write_raw_sequence(root: Path, poses: list[list[float]], frame_indices: list[int]) -> Path:
    sequence = root / "AbandonedFactory" / "Easy" / "P000"
    image_dir = sequence / "image_left"
    image_dir.mkdir(parents=True)
    for index in frame_indices:
        (image_dir / f"{index:06d}_left.png").write_bytes(f"frame-{index}".encode())
    np.savetxt(sequence / "pose_left.txt", np.asarray(poses, dtype=float), fmt="%.9f")
    return sequence


def test_convert_and_freeze_tartanair_v1(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    converted = tmp_path / "converted"
    evidence = tmp_path / "evidence"
    poses = [
        [1.0, 2.0, -3.0, 0.0, 0.0, 0.0, 1.0],
        [2.0, 3.0, -4.0, 0.0, 0.0, 0.0, 1.0],
        [3.0, 4.0, -5.0, 0.0, 0.0, 0.0, 1.0],
    ]
    _write_raw_sequence(raw, poses, [0, 1, 2])

    summary = convert_tartanair_v1(raw, converted, fps=10.0, link_mode="copy")
    assert summary.sequences == 1
    assert summary.frames == 3

    descriptor_path = converted / "AbandonedFactory__Easy__P000" / "sequence.json"
    descriptor = json.loads(descriptor_path.read_text(encoding="utf-8"))
    assert descriptor["schema"] == "s4dtam-tartanair-sequence/v1"
    assert descriptor["provenance"]["declared_fps"] == 10.0
    assert [frame["timestamp"] for frame in descriptor["frames"]] == [0.0, 0.1, 0.2]
    assert descriptor["calibration"]["image_size"] == [640, 480]

    loaded = list(TartanAirDataset(converted).sequences())
    assert len(loaded) == 1
    np.testing.assert_allclose(loaded[0].gt_positions[0], [2.0, 1.0, 3.0])
    np.testing.assert_allclose(
        np.abs(loaded[0].gt_quaternions[0]),
        [np.sqrt(0.5), np.sqrt(0.5), 0.0, 0.0],
        atol=1e-7,
    )

    freeze = freeze_tartanair_cohort(converted, evidence)
    assert freeze.sequences == 1
    assert freeze.frames == 3
    assert freeze.files == 4
    assert len(freeze.manifest_sha256) == 64
    assert len(freeze.sequence_list_sha256) == 64
    assert (evidence / "sequence-list.txt").read_text() == "AbandonedFactory__Easy__P000\n"
    manifest = (evidence / "files.sha256").read_text()
    assert "AbandonedFactory__Easy__P000/sequence.json" in manifest
    assert "AbandonedFactory__Easy__P000/frames/000000_left.png" in manifest
    assert hashlib.sha256(manifest.encode()).hexdigest() == freeze.manifest_sha256


def test_converter_rejects_pose_image_count_mismatch(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    poses = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]
    _write_raw_sequence(raw, poses, [0, 1])

    with pytest.raises(ValueError, match="pose/image count mismatch"):
        convert_tartanair_v1(raw, tmp_path / "converted", fps=10.0, link_mode="copy")


def test_converter_rejects_missing_frame_index(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    poses = [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    ]
    _write_raw_sequence(raw, poses, [0, 2])

    with pytest.raises(ValueError, match="frame indices are missing or out of order"):
        convert_tartanair_v1(raw, tmp_path / "converted", fps=10.0, link_mode="copy")


def test_converter_rejects_invalid_sampling_rate(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    poses = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]
    _write_raw_sequence(raw, poses, [0])

    with pytest.raises(ValueError, match="fps must be finite and positive"):
        convert_tartanair_v1(raw, tmp_path / "converted", fps=0.0, link_mode="copy")


def test_tartanair_identity_axis_preserves_identity_orientation(tmp_path: Path) -> None:
    sequence = tmp_path / "sequence"
    sequence.mkdir()
    (sequence / "frame.png").write_bytes(b"frame")
    descriptor = {
        "id": "identity",
        "timestamp_unit": "s",
        "position_unit": "m",
        "frames": [{"index": 0, "timestamp": 0.0, "file": "frame.png"}],
        "positions": [[1.0, 2.0, 3.0]],
        "quaternions_xyzw": [[0.0, 0.0, 0.0, 1.0]],
        "calibration": {
            "camera_matrix": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
            "image_size": [1, 1],
            "camera_frame": "camera",
            "body_frame": "body",
        },
    }
    (sequence / "sequence.json").write_text(json.dumps(descriptor), encoding="utf-8")
    loaded = list(TartanAirDataset(tmp_path, axis_convention="identity").sequences())[0]
    np.testing.assert_allclose(loaded.gt_positions[0], [1.0, 2.0, 3.0])
    np.testing.assert_allclose(loaded.gt_quaternions[0], [0.0, 0.0, 0.0, 1.0])

def test_freeze_with_original_source_records_pose_and_rgb_hashes(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    poses = [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    ]
    trajectory = _write_raw_sequence(raw, poses, [0, 1])
    converted = tmp_path / "converted"
    convert_tartanair_v1(raw, converted, fps=10.0, link_mode="copy")
    evidence = tmp_path / "evidence"
    freeze_tartanair_cohort(converted, evidence, raw_root=raw)

    metadata = json.loads((evidence / "freeze.json").read_text(encoding="utf-8"))
    manifest = (evidence / "raw-files.sha256").read_text(encoding="utf-8")
    assert metadata["raw_source_validation"] == "byte_matched"
    assert metadata["raw_source_manifest"] == "raw-files.sha256"
    assert hashlib.sha256(manifest.encode()).hexdigest() == metadata[
        "raw_source_manifest_sha256"
    ]
    assert "AbandonedFactory/Easy/P000/pose_left.txt" in manifest
    assert "AbandonedFactory/Easy/P000/image_left/000000_left.png" in manifest
    assert hashlib.sha256((trajectory / "pose_left.txt").read_bytes()).hexdigest() in manifest


def test_freeze_without_raw_source_does_not_claim_upstream_validation(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    _write_raw_sequence(raw, [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]], [0])
    converted = tmp_path / "converted"
    evidence = tmp_path / "evidence"
    convert_tartanair_v1(raw, converted, fps=10.0, link_mode="copy")
    freeze_tartanair_cohort(converted, evidence)

    metadata = json.loads((evidence / "freeze.json").read_text(encoding="utf-8"))
    assert metadata["raw_source_validation"] == "not_performed"
    assert "raw_source_manifest_sha256" not in metadata
    assert not (evidence / "raw-files.sha256").exists()


@pytest.mark.parametrize("mutated", ["rgb", "pose"])
def test_freeze_rejects_upstream_drift_after_copy_conversion(
    tmp_path: Path, mutated: str
) -> None:
    raw = tmp_path / "raw"
    trajectory = _write_raw_sequence(
        raw, [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]], [0]
    )
    converted = tmp_path / "converted"
    convert_tartanair_v1(raw, converted, fps=10.0, link_mode="copy")
    if mutated == "rgb":
        (trajectory / "image_left" / "000000_left.png").write_bytes(b"changed")
    else:
        np.savetxt(
            trajectory / "pose_left.txt",
            [[42.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]],
        )

    evidence = tmp_path / "evidence"
    with pytest.raises(ValueError, match="(RGB bytes differ|poses changed)"):
        freeze_tartanair_cohort(converted, evidence, raw_root=raw)
    assert not (evidence / "freeze.json").exists()
