#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SKILL_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
OS_NAME=$(uname -s)
ARCH_NAME=$(uname -m)
OUTPUT_NAME="project-profile-capture-${OS_NAME}-${ARCH_NAME}"
BUILD_DIR="${SKILL_DIR}/.build"
PYINSTALLER_ARCH_ARGS=""

case "$ARCH_NAME" in
  x86_64|amd64|AMD64)
    ARCH_NAME="x86_64"
    ;;
  arm64|aarch64)
    ARCH_NAME="arm64"
    ;;
esac

case "$OS_NAME" in
  Darwin)
    PYINSTALLER_ARCH_ARGS="--target-arch ${ARCH_NAME}"
    ;;
  Linux)
    ;;
esac

OUTPUT_NAME="project-profile-capture-${OS_NAME}-${ARCH_NAME}"

rm -rf "$BUILD_DIR"
mkdir -p "$SKILL_DIR/dist" "$BUILD_DIR"

python3 -m PyInstaller \
  --onefile \
  --clean \
  --name "$OUTPUT_NAME" \
  --distpath "$SKILL_DIR/dist" \
  --workpath "$BUILD_DIR/work" \
  --specpath "$BUILD_DIR/spec" \
  $PYINSTALLER_ARCH_ARGS \
  "$SKILL_DIR/scripts/capture_project_profile.py"

chmod +x "$SKILL_DIR/dist/$OUTPUT_NAME"
rm -rf "$BUILD_DIR"

echo "$SKILL_DIR/dist/$OUTPUT_NAME"
