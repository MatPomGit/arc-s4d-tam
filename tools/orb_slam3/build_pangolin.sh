#!/usr/bin/env bash
# Reproducible Pangolin v0.6 compatibility build for the pinned ORB-SLAM3 baseline.
set -euo pipefail

PANGOLIN_URL="https://github.com/stevenlovegrove/Pangolin.git"
PANGOLIN_REV="dd801d244db3a8e27b7fe8020cd751404aa818fd"

SOURCE_DIR="artifacts/baselines/orb_slam3/pangolin-source"
PREFIX_DIR="artifacts/baselines/orb_slam3/pangolin-prefix"
JOBS="4"

usage() {
  cat <<'EOF'
Usage: tools/orb_slam3/build_pangolin.sh [--source DIR] [--prefix DIR] [--jobs N]

Build Pangolin v0.6 from the exact pinned source commit. GCC 15 no longer
supplies <cstdint> transitively in some headers; the build injects
-include cstdint via CMake CXX flags, without modifying upstream source.
The install remains local to --prefix. No sudo or system packages are changed.

After installation, pass CMAKE_PREFIX_PATH and LD_LIBRARY_PATH to
tools/orb_slam3/build_runner.sh.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source) [[ $# -ge 2 ]] || { usage >&2; exit 2; }; SOURCE_DIR="$2"; shift 2 ;;
    --prefix) [[ $# -ge 2 ]] || { usage >&2; exit 2; }; PREFIX_DIR="$2"; shift 2 ;;
    --jobs) [[ $# -ge 2 ]] || { usage >&2; exit 2; }; JOBS="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

[[ "$JOBS" =~ ^[1-9][0-9]*$ ]] || { echo "--jobs must be a positive integer" >&2; exit 2; }
SOURCE_DIR="$(realpath -m "$SOURCE_DIR")"
PREFIX_DIR="$(realpath -m "$PREFIX_DIR")"

if [[ ! -d "$SOURCE_DIR/.git" ]]; then
  if [[ -e "$SOURCE_DIR" ]]; then
    echo "Refusing to overwrite a non-Git Pangolin source path: $SOURCE_DIR" >&2
    exit 1
  fi
  mkdir -p "$(dirname "$SOURCE_DIR")"
  git clone --depth 1 --branch v0.6 "$PANGOLIN_URL" "$SOURCE_DIR"
fi

ACTUAL_REV="$(git -C "$SOURCE_DIR" rev-parse HEAD)"
if [[ "$ACTUAL_REV" != "$PANGOLIN_REV" ]]; then
  echo "Pangolin revision mismatch: expected $PANGOLIN_REV, got $ACTUAL_REV" >&2
  exit 1
fi
if [[ -n "$(git -C "$SOURCE_DIR" status --porcelain --untracked-files=no)" ]]; then
  echo "Pangolin tracked sources are modified; refusing unpinned build" >&2
  exit 1
fi

mkdir -p "$PREFIX_DIR"
cmake -S "$SOURCE_DIR" -B "$SOURCE_DIR/build" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
  -DCMAKE_INSTALL_PREFIX="$PREFIX_DIR" \
  -DCMAKE_CXX_FLAGS="-include cstdint" \
  -DBUILD_TESTS=OFF \
  -DBUILD_EXAMPLES=OFF \
  -DBUILD_TOOLS=OFF

cmake --build "$SOURCE_DIR/build" --parallel "$JOBS"
cmake --install "$SOURCE_DIR/build"

python3 - "$PREFIX_DIR/pangolin-build-manifest.json" "$ACTUAL_REV" "$PREFIX_DIR" <<'PY'
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

manifest_file = Path(sys.argv[1])
revision = sys.argv[2]
prefix = Path(sys.argv[3])
libraries = sorted(
    file for file in prefix.rglob("libpangolin*") if file.is_file()
)
if not libraries:
    raise SystemExit(f"No installed Pangolin library found below {prefix}")

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

manifest = {
    "schema": "s4dtam-pangolin-source-build/v1",
    "upstream": "https://github.com/stevenlovegrove/Pangolin.git",
    "revision": revision,
    "source_patch": "none",
    "cmake_cxx_flags": "-include cstdint",
    "cmake_policy_version_minimum": "3.5",
    "install_prefix": str(prefix),
    "platform": platform.platform(),
    "compiler": subprocess.run(
        ["c++", "--version"], text=True, capture_output=True, check=True
    ).stdout.splitlines()[0],
    "libraries_sha256": {
        str(path.relative_to(prefix)): sha256(path) for path in libraries
    },
}
manifest_file.write_text(
    json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
PY

echo "Pangolin v0.6 built at commit $ACTUAL_REV"
echo "Build manifest: $PREFIX_DIR/pangolin-build-manifest.json"
echo "For the ORB-SLAM3 build, export CMAKE_PREFIX_PATH=$PREFIX_DIR"
