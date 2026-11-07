"""Offline checks for reproducible ORB-SLAM3/Pangolin source build scripts."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "tools/orb_slam3/build_pangolin.sh"
PIN = "dd801d244db3a8e27b7fe8020cd751404aa818fd"


@pytest.mark.skipif(shutil.which("bash") is None, reason="Bash unavailable")
def test_pangolin_build_script_is_valid_bash() -> None:
    subprocess.run(["bash", "-n", str(SCRIPT)], check=True)


@pytest.mark.skipif(shutil.which("bash") is None, reason="Bash unavailable")
def test_pangolin_build_script_help_does_not_download_or_build() -> None:
    result = subprocess.run(
        ["bash", str(SCRIPT), "--help"],
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Pangolin v0.6" in result.stdout
    assert "GCC 15" in result.stdout


@pytest.mark.skipif(shutil.which("bash") is None, reason="Bash unavailable")
def test_pangolin_build_rejects_invalid_jobs_before_git_or_cmake(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            "bash", str(SCRIPT),
            "--source", str(tmp_path / "nonexistent"),
            "--prefix", str(tmp_path / "prefix"),
            "--jobs", "0",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 2
    assert "--jobs must be a positive integer" in result.stderr
    assert not (tmp_path / "nonexistent").exists()


def test_pangolin_pin_and_compatibility_flag_are_explicit() -> None:
    source = SCRIPT.read_text(encoding="utf-8")
    assert f'PANGOLIN_REV="{PIN}"' in source
    assert 'git -C "$SOURCE_DIR" rev-parse HEAD' in source
    assert 'status --porcelain --untracked-files=no' in source
    assert '-DCMAKE_CXX_FLAGS="-include cstdint"' in source
    assert 'pangolin-build-manifest.json' in source
