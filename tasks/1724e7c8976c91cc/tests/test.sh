#!/bin/bash
set -u

mkdir -p /logs/verifier

python3 - <<'PY'
import gzip
import hashlib
import json
import os
import stat
import sys
import tarfile
from pathlib import Path

ROOT = Path("/home/user/lfs_capsule")
SRC = ROOT / "source"
WORK = ROOT / "worktree"
OBJ = ROOT / "objects" / "sha256"
HANDOFF = ROOT / "handoff"
ARCHIVE = HANDOFF / "git-lfs-capsule-1.0.0.tar.gz"
MANIFEST = HANDOFF / "manifest.json"
CAPSULE = "git-lfs-capsule-1.0.0"
MTIME = 1704067200


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    Path("/logs/verifier/reward.txt").write_text("0\n", encoding="utf-8")
    sys.exit(0)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require_file(path: Path) -> None:
    if not path.is_file():
        fail(f"missing required file: {path}")


def require_dir(path: Path) -> None:
    if not path.is_dir():
        fail(f"missing required directory: {path}")


for path in [SRC / "README.md", SRC / "src/filter.py"]:
    require_file(path)
for path in [WORK, WORK / "assets", WORK / "src", OBJ, HANDOFF]:
    require_dir(path)
for path in [WORK / "README.md", WORK / "src/filter.py", WORK / ".gitattributes", MANIFEST, ARCHIVE]:
    require_file(path)

if (WORK / "README.md").read_bytes() != (SRC / "README.md").read_bytes():
    fail("worktree README.md does not match source")
if (WORK / "src/filter.py").read_bytes() != (SRC / "src/filter.py").read_bytes():
    fail("worktree src/filter.py does not match source")

expected_attrs = b"assets/*.bin filter=lfs diff=lfs merge=lfs -text\n"
if (WORK / ".gitattributes").read_bytes() != expected_attrs:
    fail(".gitattributes is not the required Git LFS rule")

expected_entries = []
for rel in ["assets/field-model.bin", "assets/sensor-calibration.bin"]:
    source_payload = (SRC / rel).read_bytes()
    digest = sha256_bytes(source_payload)
    size = len(source_payload)
    pointer = (
        f"version https://git-lfs.github.com/spec/v1\n"
        f"oid sha256:{digest}\n"
        f"size {size}\n"
    ).encode()
    pointer_path = WORK / rel
    require_file(pointer_path)
    if pointer_path.read_bytes() != pointer:
        fail(f"{rel} is not the exact Git LFS pointer")
    object_path = OBJ / digest[:2] / digest
    require_file(object_path)
    if object_path.read_bytes() != source_payload:
        fail(f"object payload mismatch for {rel}")
    expected_entries.append({"path": rel, "oid": f"sha256:{digest}", "size": size})

expected_manifest = {
    "archive": "git-lfs-capsule-1.0.0.tar.gz",
    "files": expected_entries,
    "version": "1.0.0",
}
expected_manifest_bytes = (json.dumps(expected_manifest, separators=(",", ":")) + "\n").encode()
if MANIFEST.read_bytes() != expected_manifest_bytes:
    fail("manifest content, key order, minification, or trailing newline is incorrect")

raw = ARCHIVE.read_bytes()
if len(raw) < 10 or raw[:2] != b"\x1f\x8b":
    fail("archive is not gzip")
if raw[3] != 0:
    fail("gzip stream stores optional header fields")
if int.from_bytes(raw[4:8], "little") != 0:
    fail("gzip mtime is not normalized to zero")

try:
    with tarfile.open(ARCHIVE, "r:gz") as tf:
        members = tf.getmembers()
        names = [m.name for m in members]
        expected_names = [
            f"{CAPSULE}",
            f"{CAPSULE}/manifest.json",
            f"{CAPSULE}/objects",
            f"{CAPSULE}/objects/sha256",
        ]
        for entry in expected_entries:
            digest = entry["oid"].split(":", 1)[1]
            expected_names.append(f"{CAPSULE}/objects/sha256/{digest[:2]}")
            expected_names.append(f"{CAPSULE}/objects/sha256/{digest[:2]}/{digest}")
        expected_names.extend([
            f"{CAPSULE}/worktree",
            f"{CAPSULE}/worktree/.gitattributes",
            f"{CAPSULE}/worktree/README.md",
            f"{CAPSULE}/worktree/assets",
            f"{CAPSULE}/worktree/assets/field-model.bin",
            f"{CAPSULE}/worktree/assets/sensor-calibration.bin",
            f"{CAPSULE}/worktree/src",
            f"{CAPSULE}/worktree/src/filter.py",
        ])
        expected_names = sorted(expected_names)
        if names != expected_names:
            fail(f"tar member order or file set is wrong: {names}")
        for member in members:
            if member.uid != 0 or member.gid != 0 or member.uname or member.gname:
                fail(f"{member.name} does not use numeric 0/0 ownership")
            if int(member.mtime) != MTIME:
                fail(f"{member.name} has non-deterministic mtime")
            mode = stat.S_IMODE(member.mode)
            if member.isdir() and mode != 0o755:
                fail(f"{member.name} directory mode is {oct(mode)}, expected 0755")
            if member.isfile() and mode != 0o644:
                fail(f"{member.name} file mode is {oct(mode)}, expected 0644")
        archive_manifest = tf.extractfile(f"{CAPSULE}/manifest.json").read()
        if archive_manifest != expected_manifest_bytes:
            fail("archived manifest does not match handoff manifest")
        for rel in ["README.md", "src/filter.py", ".gitattributes", "assets/field-model.bin", "assets/sensor-calibration.bin"]:
            archived = tf.extractfile(f"{CAPSULE}/worktree/{rel}").read()
            if archived != (WORK / rel).read_bytes():
                fail(f"archived worktree/{rel} does not match final worktree")
        for entry in expected_entries:
            digest = entry["oid"].split(":", 1)[1]
            archived = tf.extractfile(f"{CAPSULE}/objects/sha256/{digest[:2]}/{digest}").read()
            if sha256_bytes(archived) != digest:
                fail(f"archived object digest mismatch for {entry['path']}")
except Exception as exc:
    fail(f"archive validation error: {exc}")

print("ok")
Path("/logs/verifier/reward.txt").write_text("1\n", encoding="utf-8")
PY
