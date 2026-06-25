#!/bin/bash
set -euo pipefail

ROOT=/home/user/lfs_capsule
SRC="$ROOT/source"
WORK="$ROOT/worktree"
OBJ="$ROOT/objects"
HANDOFF="$ROOT/handoff"
VERSION=1.0.0
ARCHIVE=git-lfs-capsule-${VERSION}.tar.gz
CAPSULE=git-lfs-capsule-${VERSION}

rm -rf "$WORK" "$OBJ" "$HANDOFF"
mkdir -p "$WORK/assets" "$WORK/src" "$OBJ/sha256" "$HANDOFF"

cp "$SRC/README.md" "$WORK/README.md"
cp "$SRC/src/filter.py" "$WORK/src/filter.py"
printf 'assets/*.bin filter=lfs diff=lfs merge=lfs -text\n' > "$WORK/.gitattributes"

python3 - <<'PY'
import hashlib
import json
from pathlib import Path

root = Path("/home/user/lfs_capsule")
src = root / "source"
work = root / "worktree"
objects = root / "objects" / "sha256"
entries = []

for rel in ["assets/field-model.bin", "assets/sensor-calibration.bin"]:
    payload = (src / rel).read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    size = len(payload)
    object_path = objects / digest[:2] / digest
    object_path.parent.mkdir(parents=True, exist_ok=True)
    object_path.write_bytes(payload)
    (work / rel).write_text(
        f"version https://git-lfs.github.com/spec/v1\n"
        f"oid sha256:{digest}\n"
        f"size {size}\n",
        encoding="utf-8",
    )
    entries.append({"path": rel, "oid": f"sha256:{digest}", "size": size})

manifest = {
    "archive": "git-lfs-capsule-1.0.0.tar.gz",
    "files": entries,
    "version": "1.0.0",
}
(root / "handoff" / "manifest.json").write_text(
    json.dumps(manifest, separators=(",", ":")) + "\n",
    encoding="utf-8",
)
PY

find "$WORK" "$OBJ" "$HANDOFF" -type d -exec chmod 0755 {} +
find "$WORK" "$OBJ" "$HANDOFF" -type f -exec chmod 0644 {} +

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/$CAPSULE"
cp "$HANDOFF/manifest.json" "$TMP/$CAPSULE/manifest.json"
cp -a "$WORK" "$TMP/$CAPSULE/worktree"
cp -a "$OBJ" "$TMP/$CAPSULE/objects"
find "$TMP/$CAPSULE" -type d -exec chmod 0755 {} +
find "$TMP/$CAPSULE" -type f -exec chmod 0644 {} +

tar --sort=name \
  --mtime='UTC 2024-01-01 00:00:00' \
  --owner=0 --group=0 --numeric-owner \
  -cf - -C "$TMP" "$CAPSULE" | gzip -n > "$HANDOFF/$ARCHIVE"
chmod 0644 "$HANDOFF/$ARCHIVE"
