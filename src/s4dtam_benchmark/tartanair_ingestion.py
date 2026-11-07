"""Reproducible ingestion and freeze utilities for TartanAir V1-style trajectories."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from s4dtam_benchmark.datasets import TartanAirDataset

_IMAGE_RE = re.compile(r"^(\d+)_left\.png$")

# TartanAir V1 pinhole calibration published by the dataset authors.
_TARTANAIR_V1_CALIBRATION = {
    "camera_matrix": [[320.0, 0.0, 320.0], [0.0, 320.0, 240.0], [0.0, 0.0, 1.0]],
    "image_size": [640, 480],
    "camera_frame": "camera_left",
    "body_frame": "body",
    "distortion_coefficients": [0.0, 0.0, 0.0, 0.0],
    "source": "TartanAir V1 published pinhole calibration",
}


@dataclass(frozen=True)
class TartanAirConversionSummary:
    sequences: int
    frames: int
    output_root: Path


@dataclass(frozen=True)
class TartanAirFreezeSummary:
    sequences: int
    frames: int
    files: int
    output_dir: Path
    manifest_sha256: str
    sequence_list_sha256: str


def discover_tartanair_v1_trajectories(raw_root: str | Path) -> list[Path]:
    """Find trajectory directories containing the canonical V1 pose and left RGB streams."""
    root = Path(raw_root)
    if not root.is_dir():
        raise FileNotFoundError(f"TartanAir raw root does not exist: {root}")
    trajectories = [
        pose.parent
        for pose in sorted(root.rglob("pose_left.txt"))
        if (pose.parent / "image_left").is_dir()
    ]
    if not trajectories:
        raise FileNotFoundError(
            f"No TartanAir V1 trajectories with pose_left.txt and image_left found below {root}"
        )
    return trajectories


def convert_tartanair_v1(
    raw_root: str | Path,
    output_root: str | Path,
    *,
    fps: float,
    link_mode: str = "symlink",
    overwrite: bool = False,
) -> TartanAirConversionSummary:
    """Convert V1-style trajectories into the strict one-level ``sequence.json`` contract.

    Raw TartanAir V1 trajectories do not carry per-frame timestamps in the canonical pose file.
    Timestamps are therefore generated deterministically from the frame index and an explicitly
    supplied sampling rate. The rate is persisted in every descriptor so the timing assumption is
    never hidden inside the converter.
    """
    if not np.isfinite(fps) or fps <= 0:
        raise ValueError("TartanAir fps must be finite and positive")
    if link_mode not in {"symlink", "hardlink", "copy"}:
        raise ValueError("link_mode must be one of: symlink, hardlink, copy")

    raw = Path(raw_root)
    output = Path(output_root)
    output.mkdir(parents=True, exist_ok=True)

    total_frames = 0
    trajectories = discover_tartanair_v1_trajectories(raw)
    for trajectory in trajectories:
        relative = trajectory.relative_to(raw)
        sequence_id = "__".join(relative.parts)
        destination = output / sequence_id
        if destination.exists():
            if not overwrite:
                raise FileExistsError(
                    f"Converted TartanAir sequence already exists: {destination}; use --overwrite"
                )
            shutil.rmtree(destination)
        frames_dir = destination / "frames"
        frames_dir.mkdir(parents=True)

        images = sorted((trajectory / "image_left").glob("*_left.png"))
        if not images:
            raise ValueError(f"No left RGB PNG frames found in {trajectory / 'image_left'}")
        indices = []
        for image in images:
            match = _IMAGE_RE.match(image.name)
            if match is None:
                raise ValueError(f"Unexpected TartanAir left-image filename: {image.name}")
            indices.append(int(match.group(1)))
        if indices != list(range(len(images))):
            raise ValueError(f"TartanAir frame indices are missing or out of order in {trajectory}")

        poses = np.loadtxt(trajectory / "pose_left.txt", dtype=float)
        if poses.ndim == 1:
            poses = poses.reshape(1, -1)
        if poses.shape != (len(images), 7):
            raise ValueError(
                "TartanAir pose/image count mismatch or invalid pose format in "
                f"{trajectory}: poses={poses.shape}, images={len(images)}"
            )
        if np.any(~np.isfinite(poses)):
            raise ValueError(f"TartanAir pose file contains non-finite values: {trajectory}")
        quaternion_norms = np.linalg.norm(poses[:, 3:7], axis=1)
        if np.any(np.abs(quaternion_norms - 1.0) > 1e-3):
            raise ValueError(f"TartanAir pose file contains non-unit quaternions: {trajectory}")

        frame_entries = []
        for index, source in enumerate(images):
            target = frames_dir / source.name
            _materialize_frame(source, target, link_mode)
            frame_entries.append(
                {
                    "index": index,
                    "timestamp": index / fps,
                    "file": f"frames/{source.name}",
                }
            )

        descriptor = {
            "schema": "s4dtam-tartanair-sequence/v1",
            "id": sequence_id,
            "frame_count": len(images),
            "timestamp_unit": "s",
            "position_unit": "m",
            "frames": frame_entries,
            "positions": poses[:, :3].tolist(),
            "quaternions_xyzw": poses[:, 3:7].tolist(),
            "calibration": dict(_TARTANAIR_V1_CALIBRATION),
            "provenance": {
                "source_layout": "tartanair_v1",
                "source_relative_trajectory": relative.as_posix(),
                "pose_file": "pose_left.txt",
                "image_stream": "image_left",
                "timestamp_source": "frame_index_divided_by_declared_fps",
                "declared_fps": float(fps),
                "materialization": link_mode,
                "source_coordinate_frame": "NED",
                "adapter_coordinate_transform": "tartanair_ned_to_enu",
            },
        }
        (destination / "sequence.json").write_text(
            json.dumps(descriptor, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        total_frames += len(images)

    # Validate the complete generated cohort with the same adapter used by the benchmark.
    list(TartanAirDataset(output).sequences())
    return TartanAirConversionSummary(
        sequences=len(trajectories), frames=total_frames, output_root=output
    )


def freeze_tartanair_cohort(
    converted_root: str | Path,
    output_dir: str | Path,
    *,
    raw_root: str | Path | None = None,
) -> TartanAirFreezeSummary:
    """Freeze converted inputs and optionally attest matching upstream V1 bytes.

    Without raw_root, only the converted artifacts are hashed. That limited
    result must not be presented as verified upstream dataset provenance.
    """
    root = Path(converted_root)
    destination = Path(output_dir)
    sequences = list(TartanAirDataset(root).sequences())
    descriptors = sorted(root.glob("*/sequence.json"))
    if len(descriptors) != len(sequences):
        raise ValueError("TartanAir descriptor discovery does not match validated sequence count")

    sequence_ids = [sequence.sequence_id for sequence in sequences]
    sequence_list_text = "".join(f"{sequence_id}\n" for sequence_id in sequence_ids)
    sequence_list_hash = _sha256_bytes(sequence_list_text.encode("utf-8"))

    files: dict[str, Path] = {}
    frame_count = 0
    for descriptor in descriptors:
        spec = json.loads(descriptor.read_text(encoding="utf-8"))
        rel_descriptor = descriptor.relative_to(root).as_posix()
        files[rel_descriptor] = descriptor
        for frame in spec["frames"]:
            path = descriptor.parent / str(frame["file"])
            if not path.is_file():
                raise ValueError(f"Missing TartanAir frame while freezing cohort: {path}")
            rel = path.relative_to(root).as_posix()
            files[rel] = path
            frame_count += 1

    manifest_text = "".join(
        f"{_sha256_file(path)}  {relative}\n" for relative, path in sorted(files.items())
    )
    manifest_hash = _sha256_bytes(manifest_text.encode("utf-8"))
    raw_manifest_text = (
        _audit_tartanair_v1_sources(Path(raw_root), root, descriptors)
        if raw_root is not None
        else None
    )

    # No output is written until the converted and optional upstream audits pass.
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "sequence-list.txt").write_text(sequence_list_text, encoding="utf-8")
    (destination / "files.sha256").write_text(manifest_text, encoding="utf-8")
    freeze = {
        "schema": "s4dtam-tartanair-freeze/v1",
        "dataset": "tartanair",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "converted_root": str(root),
        "sequence_count": len(sequences),
        "frame_count": frame_count,
        "file_count": len(files),
        "sequence_list": "sequence-list.txt",
        "sequence_list_sha256": sequence_list_hash,
        "file_manifest": "files.sha256",
        "file_manifest_sha256": manifest_hash,
        "raw_source_validation": "byte_matched" if raw_manifest_text is not None else "not_performed",
    }
    if raw_manifest_text is not None:
        (destination / "raw-files.sha256").write_text(raw_manifest_text, encoding="utf-8")
        freeze["raw_source_manifest"] = "raw-files.sha256"
        freeze["raw_source_manifest_sha256"] = _sha256_bytes(
            raw_manifest_text.encode("utf-8")
        )
    (destination / "freeze.json").write_text(
        json.dumps(freeze, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return TartanAirFreezeSummary(
        sequences=len(sequences),
        frames=frame_count,
        files=len(files),
        output_dir=destination,
        manifest_sha256=manifest_hash,
        sequence_list_sha256=sequence_list_hash,
    )


def _audit_tartanair_v1_sources(
    raw_root: Path, converted_root: Path, descriptors: list[Path]
) -> str:
    """Verify each converted pose and RGB frame against its exact upstream file."""
    raw_root = raw_root.resolve()
    if not raw_root.is_dir():
        raise FileNotFoundError(f"Original TartanAir source root does not exist: {raw_root}")
    source_files: dict[str, Path] = {}
    for descriptor in descriptors:
        spec = json.loads(descriptor.read_text(encoding="utf-8"))
        provenance = spec.get("provenance", {})
        if provenance.get("source_layout") != "tartanair_v1":
            raise ValueError(f"Not an attested TartanAir V1 conversion: {descriptor}")
        relative = provenance.get("source_relative_trajectory")
        if not isinstance(relative, str) or not relative:
            raise ValueError(f"Missing upstream trajectory path: {descriptor}")
        relative_path = Path(relative)
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise ValueError(f"Unsafe upstream trajectory path: {relative}")
        trajectory = (raw_root / relative_path).resolve()
        if not trajectory.is_relative_to(raw_root):
            raise ValueError(f"Upstream trajectory escapes source root: {relative}")

        pose_file = trajectory / "pose_left.txt"
        if not pose_file.is_file() or not pose_file.resolve().is_relative_to(raw_root):
            raise FileNotFoundError(f"Original TartanAir pose file missing: {pose_file}")
        poses = np.loadtxt(pose_file, dtype=float)
        if poses.ndim == 1:
            poses = poses.reshape(1, -1)
        expected_poses = np.column_stack(
            [np.asarray(spec["positions"]), np.asarray(spec["quaternions_xyzw"])]
        )
        if not np.array_equal(poses, expected_poses):
            raise ValueError(f"Original TartanAir poses changed after conversion: {relative}")
        source_files[pose_file.relative_to(raw_root).as_posix()] = pose_file

        for frame in spec["frames"]:
            frame_path = Path(str(frame["file"]))
            if len(frame_path.parts) != 2 or frame_path.parts[0] != "frames":
                raise ValueError(f"Unexpected converted frame path: {frame_path}")
            source = trajectory / "image_left" / frame_path.name
            if not source.is_file() or not source.resolve().is_relative_to(raw_root):
                raise FileNotFoundError(f"Original TartanAir RGB file missing: {source}")
            converted = descriptor.parent / frame_path
            if _sha256_file(source) != _sha256_file(converted):
                raise ValueError(f"Original TartanAir RGB bytes differ: {source}")
            source_files[source.relative_to(raw_root).as_posix()] = source

    return "".join(
        f"{_sha256_file(path)}  {relative}\n"
        for relative, path in sorted(source_files.items())
    )

def _materialize_frame(source: Path, target: Path, mode: str) -> None:
    if mode == "copy":
        shutil.copy2(source, target)
    elif mode == "hardlink":
        os.link(source, target)
    else:
        relative = os.path.relpath(source, start=target.parent)
        target.symlink_to(relative)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
