#!/bin/bash
set -u

mkdir -p /logs/verifier

python3 - <<'PY'
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import tarfile

release = Path("/home/user/release")
archive_path = release / "widget-2.4.1.tar.gz"
sums_path = release / "SHA256SUMS"
manifest_path = release / "widget-2.4.1.manifest.json"

expected_files = [
    ("LICENSE", "0644", b"MIT License\n\nCopyright (c) 2026 Widget Maintainers\n"),
    ("README.md", "0644", b"# Widget\n\nWidget is a tiny deterministic packaging sample used by release automation.\n"),
    ("docs/usage.md", "0644", b"# Usage\n\nRun scripts/widget-smoke from an environment with src on PYTHONPATH.\n"),
    ("pyproject.toml", "0644", b"[project]\nname = \"widget\"\nversion = \"2.4.1\"\nrequires-python = \">=3.10\"\n\n[tool.widget]\nprofile = \"release\"\n"),
    ("scripts/widget-smoke", "0755", b"#!/usr/bin/env bash\nset -euo pipefail\npython3 -c \"from widget import normalize_name; print(normalize_name('Widget Smoke Test'))\"\n"),
    ("src/widget/__init__.py", "0644", b"VERSION = \"2.4.1\"\n\ndef normalize_name(value: str) -> str:\n    return \"-\".join(value.strip().lower().split())\n"),
    ("src/widget/core.py", "0644", b"from . import normalize_name\n\ndef render_slug(parts):\n    return normalize_name(\" \".join(parts))\n"),
    ("src/widget/data/defaults.toml", "0644", b"[defaults]\nregion = \"us-east-1\"\nretries = 3\n"),
]

def fail(message):
    print(message, file=sys.stderr)
    Path("/logs/verifier/reward.txt").write_text("0\n", encoding="utf-8")
    sys.exit(1)

for path in (archive_path, sums_path, manifest_path):
    if not path.is_file():
        fail(f"missing required output: {path}")

source = Path("/home/user/src/widget")
for rel, _mode, data in expected_files:
    if (source / rel).read_bytes() != data:
        fail(f"source file was modified or has unexpected content: {rel}")

archive_bytes = archive_path.read_bytes()
if len(archive_bytes) < 18:
    fail("archive is too small to be a valid gzip file")
if archive_bytes[:3] != b"\x1f\x8b\x08":
    fail("archive does not have a gzip header")
flags = archive_bytes[3]
mtime = int.from_bytes(archive_bytes[4:8], "little")
if flags & 0x08:
    fail("gzip header stores an original filename")
if mtime != 0:
    fail("gzip header mtime is not zero")

archive_sha = hashlib.sha256(archive_bytes).hexdigest()
expected_sums = f"{archive_sha}  widget-2.4.1.tar.gz\n"
if sums_path.read_text(encoding="utf-8") != expected_sums:
    fail("SHA256SUMS does not exactly match the archive digest")

try:
    tar_bytes = gzip.decompress(archive_bytes)
except Exception as exc:
    fail(f"archive is not valid gzip: {exc}")

expected_member_names = [f"widget-2.4.1/{rel}" for rel, _mode, _data in expected_files]
try:
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:") as tar:
        members = tar.getmembers()
        names = [m.name for m in members]
        if names != expected_member_names:
            fail(f"archive members differ from expected order/content: {names}")
        for member, (rel, mode, data) in zip(members, expected_files):
            if not member.isfile():
                fail(f"archive member is not a regular file: {member.name}")
            if member.mtime != 1704067200:
                fail(f"archive member has wrong mtime: {member.name}")
            if member.uid != 0 or member.gid != 0:
                fail(f"archive member has wrong uid/gid: {member.name}")
            if member.uname not in ("", None) or member.gname not in ("", None):
                fail(f"archive member has non-empty uname/gname: {member.name}")
            if f"{member.mode & 0o777:04o}" != mode:
                fail(f"archive member has wrong mode: {member.name}")
            extracted = tar.extractfile(member).read()
            if extracted != data:
                fail(f"archive content differs for {member.name}")
except SystemExit:
    raise
except Exception as exc:
    fail(f"archive is not a valid tar stream: {exc}")

raw_manifest = manifest_path.read_bytes()
if not raw_manifest.endswith(b"\n") or raw_manifest.endswith(b"\n\n"):
    fail("manifest must have exactly one trailing newline")
if b"\n" in raw_manifest[:-1] or b" " in raw_manifest or b"\t" in raw_manifest:
    fail("manifest is not minified")
try:
    pairs = json.loads(raw_manifest.decode("utf-8"), object_pairs_hook=list)
except Exception as exc:
    fail(f"manifest is not valid JSON: {exc}")

top_keys = [key for key, _value in pairs]
if top_keys != ["name", "version", "source_date_epoch", "archive", "sha256", "size_bytes", "files"]:
    fail(f"manifest top-level keys are wrong: {top_keys}")
manifest = dict(pairs)
if manifest["name"] != "widget" or manifest["version"] != "2.4.1":
    fail("manifest package identity is wrong")
if manifest["source_date_epoch"] != 1704067200:
    fail("manifest source_date_epoch is wrong")
if manifest["archive"] != "widget-2.4.1.tar.gz":
    fail("manifest archive name is wrong")
if manifest["sha256"] != archive_sha:
    fail("manifest archive sha256 is wrong")
if manifest["size_bytes"] != len(archive_bytes):
    fail("manifest archive size is wrong")

files_value = manifest["files"]
if not isinstance(files_value, list) or len(files_value) != len(expected_files):
    fail("manifest files array has wrong length")
for item, (rel, mode, data) in zip(files_value, expected_files):
    if not isinstance(item, list):
        fail("manifest file entry did not preserve object pairs")
    keys = [key for key, _value in item]
    if keys != ["path", "mode", "size_bytes", "sha256"]:
        fail(f"manifest file entry keys are wrong for {rel}: {keys}")
    entry = dict(item)
    if entry != {
        "path": rel,
        "mode": mode,
        "size_bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }:
        fail(f"manifest file entry is wrong for {rel}")

if not re.fullmatch(r"[0-9a-f]{64}  widget-2\.4\.1\.tar\.gz\n", sums_path.read_text(encoding="utf-8")):
    fail("SHA256SUMS is not in standard lowercase sha256sum format")

Path("/logs/verifier/reward.txt").write_text("1\n", encoding="utf-8")
PY

if [ $? -ne 0 ]; then
  exit 1
fi
