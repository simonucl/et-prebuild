#!/bin/bash
set -euo pipefail

src=/home/user/release/source
out=/home/user/release/handoff
name=edge-collector-v1.9.0-handoff

rm -rf "$out"
mkdir -p "$out/patches"

git -C "$src" bundle create \
  "$out/edge-collector-v1.9.0.bundle" \
  v1.8.0..release/v1.9 \
  refs/tags/v1.9.0

git -C "$src" format-patch \
  --binary \
  --full-index \
  --output-directory "$out/patches" \
  v1.8.0..release/v1.9 >/dev/null

python3 - <<'PY'
import hashlib
import json
from pathlib import Path
import subprocess

src = Path("/home/user/release/source")
out = Path("/home/user/release/handoff")

def git_rev(rev: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(src), "rev-parse", rev],
        text=True,
    ).strip()

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

patch_entries = []
for patch in sorted((out / "patches").glob("*.patch")):
    patch_entries.append({
        "path": f"patches/{patch.name}",
        "sha256": sha256(patch),
    })

manifest = {
    "schema_version": 1,
    "project": "edge-collector",
    "base_tag": "v1.8.0",
    "base_commit": git_rev("v1.8.0"),
    "target_ref": "refs/heads/release/v1.9",
    "target_tag": "v1.9.0",
    "target_commit": git_rev("release/v1.9"),
    "bundle": {
        "path": "edge-collector-v1.9.0.bundle",
        "sha256": sha256(out / "edge-collector-v1.9.0.bundle"),
    },
    "patches": patch_entries,
    "archive": {
        "path": "edge-collector-v1.9.0-handoff.tar.gz",
        "file_count": 2 + len(patch_entries),
    },
}

(out / "manifest.json").write_text(
    json.dumps(manifest, separators=(",", ":")) + "\n",
    encoding="utf-8",
)
PY

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/$name/patches"
cp "$out/edge-collector-v1.9.0.bundle" "$tmp/$name/"
cp "$out/manifest.json" "$tmp/$name/"
cp "$out"/patches/*.patch "$tmp/$name/patches/"

tar --sort=name \
  --mtime='2024-04-01 00:00:00Z' \
  --owner=0 --group=0 --numeric-owner \
  --mode='u+rw,go+r-w,a+X' \
  -C "$tmp" -cf - "$name" \
  | gzip -n > "$out/edge-collector-v1.9.0-handoff.tar.gz"
