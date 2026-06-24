#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/../../.." && pwd)

for PLATFORM_ARCH in x86_64 arm64; do
  case "$PLATFORM_ARCH" in
    x86_64)
      DOCKER_PLATFORM="linux/amd64"
      ;;
    arm64)
      DOCKER_PLATFORM="linux/arm64"
      ;;
  esac

  docker run --rm \
    --platform "$DOCKER_PLATFORM" \
    -v "$REPO_DIR":/work \
    -w /work \
    python:3.11-slim \
    sh -c "apt-get update -qq && apt-get install -y -qq binutils >/dev/null && python -m pip install -q pyinstaller && python -m PyInstaller --onefile --clean --name project-profile-capture-Linux-${PLATFORM_ARCH} --distpath skills/project-profile-capture/dist --workpath skills/project-profile-capture/.build/linux-${PLATFORM_ARCH}-work --specpath skills/project-profile-capture/.build/linux-${PLATFORM_ARCH}-spec skills/project-profile-capture/scripts/capture_project_profile.py && chmod +x skills/project-profile-capture/dist/project-profile-capture-Linux-${PLATFORM_ARCH}"
done

rm -rf "$REPO_DIR/skills/project-profile-capture/.build"
