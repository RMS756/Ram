#!/usr/bin/env bash
# Fetch the official MELON implementation at the pinned commit (not vendored: no upstream licence) and verify it.
# usage: scripts/fetch_melon_upstream.sh [target_dir]   (default /home/user/upstream/MELON)
set -euo pipefail
DEST="${1:-/home/user/upstream/MELON}"
URL="https://github.com/ucsb-mlsec/MELON"
COMMIT="$(python3 -c "import json;print(json.load(open('$(dirname "$0")/../third_party/MELON_PIN.json'))['repositories'][0]['commit'])")"
SHA="$(python3 -c "import json;print(json.load(open('$(dirname "$0")/../third_party/MELON_PIN.json'))['sha256'])")"
[ -d "$DEST/.git" ] || git clone -q "$URL" "$DEST"
git -C "$DEST" checkout -q "$COMMIT"
GOT="$(sha256sum "$DEST/pi_detector.py" | cut -d' ' -f1)"
[ "$GOT" = "$SHA" ] || { echo "sha256 mismatch: $GOT != $SHA" >&2; exit 1; }
echo "MELON pinned at $COMMIT in $DEST (pi_detector.py sha256 verified)"
