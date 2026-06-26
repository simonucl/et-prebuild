#!/bin/bash
set -u

mkdir -p /logs/verifier

fail() {
  echo "FAIL: $*" >&2
  echo 0 > /logs/verifier/reward.txt
  exit 1
}

BASE="${APP_ROOT:-/app}"
REPO="$BASE/repo"
SRC="$BASE/source/edge-filter"

[ -d "$REPO" ] || fail "missing repository root"
[ -d "$SRC" ] || fail "missing staged source tree"

python3 - <<'PY' || fail "repository content is incorrect"
import gzip
import hashlib
import io
import lzma
import os
from pathlib import Path
import tarfile

base = Path(os.environ.get("APP_ROOT", "/app"))
repo = base / "repo"
src = base / "source/edge-filter"
pool = repo / "pool/main/e/edge-filter"
dist = repo / "dists/stable/main/source"
mtime = 1712016000

expected_files = [
    "SHA256SUMS",
    "dists/stable/Release",
    "dists/stable/main/source/Sources",
    "dists/stable/main/source/Sources.gz",
    "pool/main/e/edge-filter/edge-filter_1.2.0-1.debian.tar.xz",
    "pool/main/e/edge-filter/edge-filter_1.2.0-1.dsc",
    "pool/main/e/edge-filter/edge-filter_1.2.0.orig.tar.gz",
]
actual_files = sorted(str(p.relative_to(repo)) for p in repo.rglob("*") if p.is_file())
if actual_files != expected_files:
    raise AssertionError(f"unexpected repository files: {actual_files}")

source_snapshot = {
    "README.md": b"# edge-filter\n\nSmall deterministic packet filter used by the edge appliance tests.\n",
    "LICENSE": b"MIT\n",
    "src/filter.py": b'def normalize_rule(line: str) -> str:\n    return " ".join(line.strip().split()).lower()\n\n\ndef accept(rule: str) -> bool:\n    return normalize_rule(rule).startswith("allow ")\n',
    "debian/control": b"Source: edge-filter\nSection: net\nPriority: optional\nMaintainer: Acme Edge Packaging <packaging@example.invalid>\nBuild-Depends: debhelper-compat (= 13), python3\nStandards-Version: 4.7.0\nHomepage: https://example.invalid/edge-filter\nRules-Requires-Root: no\n\nPackage: edge-filter\nArchitecture: all\nDepends: ${misc:Depends}, python3\nDescription: deterministic edge packet filter helper\n Small helper library used by edge appliances to normalize packet rules.\n",
    "debian/changelog": b"edge-filter (1.2.0-1) stable; urgency=medium\n\n  * Release deterministic source package for offline repository import.\n\n -- Acme Edge Packaging <packaging@example.invalid>  Tue, 02 Apr 2024 00:00:00 +0000\n",
    "debian/rules": b"#!/usr/bin/make -f\n%:\n\tdh $@\n",
}
for rel, expected in source_snapshot.items():
    path = src / rel
    if not path.is_file() or path.read_bytes() != expected:
        raise AssertionError(f"source file was modified: {rel}")

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def md5(data):
    return hashlib.md5(data).hexdigest()

def sha1(data):
    return hashlib.sha1(data).hexdigest()

def read_gzip_no_name(path):
    raw = path.read_bytes()
    if raw[:2] != b"\x1f\x8b":
        raise AssertionError(f"{path.name} is not gzip")
    if raw[3] & 0x08:
        raise AssertionError(f"{path.name} stores an original filename")
    if raw[4:8] != b"\x00\x00\x00\x00":
        raise AssertionError(f"{path.name} gzip mtime is not zero")
    return gzip.decompress(raw)

def check_tar(raw, expected):
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as tf:
        members = tf.getmembers()
        names = [m.name for m in members]
        if names != [e[0] for e in expected]:
            raise AssertionError(f"tar members/order mismatch: {names}")
        for member, (name, content, mode) in zip(members, expected):
            if not member.isfile():
                raise AssertionError(f"{name} is not a regular file")
            if member.mode != mode or member.uid != 0 or member.gid != 0 or member.uname != "" or member.gname != "" or member.mtime != mtime:
                raise AssertionError(f"{name} tar metadata is not normalized")
            data = tf.extractfile(member).read()
            if data != content:
                raise AssertionError(f"{name} content is wrong")

orig_name = "edge-filter_1.2.0.orig.tar.gz"
debian_name = "edge-filter_1.2.0-1.debian.tar.xz"
dsc_name = "edge-filter_1.2.0-1.dsc"
orig = (pool / orig_name).read_bytes()
debian = (pool / debian_name).read_bytes()
dsc_bytes = (pool / dsc_name).read_bytes()

orig_tar = read_gzip_no_name(pool / orig_name)
check_tar(orig_tar, [
    ("edge-filter-1.2.0/LICENSE", source_snapshot["LICENSE"], 0o644),
    ("edge-filter-1.2.0/README.md", source_snapshot["README.md"], 0o644),
    ("edge-filter-1.2.0/src/filter.py", source_snapshot["src/filter.py"], 0o644),
])
try:
    debian_tar = lzma.decompress(debian, format=lzma.FORMAT_XZ)
except Exception as exc:
    raise AssertionError(f"debian tar is not valid xz: {exc}")
check_tar(debian_tar, [
    ("debian/changelog", source_snapshot["debian/changelog"], 0o644),
    ("debian/control", source_snapshot["debian/control"], 0o644),
    ("debian/rules", source_snapshot["debian/rules"], 0o755),
])

expected_dsc = (
    "Format: 3.0 (quilt)\n"
    "Source: edge-filter\n"
    "Binary: edge-filter\n"
    "Architecture: all\n"
    "Version: 1.2.0-1\n"
    "Maintainer: Acme Edge Packaging <packaging@example.invalid>\n"
    "Homepage: https://example.invalid/edge-filter\n"
    "Standards-Version: 4.7.0\n"
    "Build-Depends: debhelper-compat (= 13), python3\n"
    "Package-List:\n"
    " edge-filter deb net optional arch=all\n"
    "Checksums-Sha256:\n"
    f" {sha256(orig)} {len(orig)} {orig_name}\n"
    f" {sha256(debian)} {len(debian)} {debian_name}\n"
    "Files:\n"
    f" {md5(orig)} {len(orig)} {orig_name}\n"
    f" {md5(debian)} {len(debian)} {debian_name}\n"
).encode()
if dsc_bytes != expected_dsc:
    raise AssertionError("dsc content, field order, checksums, or newline is incorrect")

sources = (
    "Package: edge-filter\n"
    "Binary: edge-filter\n"
    "Version: 1.2.0-1\n"
    "Maintainer: Acme Edge Packaging <packaging@example.invalid>\n"
    "Build-Depends: debhelper-compat (= 13), python3\n"
    "Architecture: all\n"
    "Standards-Version: 4.7.0\n"
    "Format: 3.0 (quilt)\n"
    "Directory: pool/main/e/edge-filter\n"
    "Files:\n"
    f" {md5(dsc_bytes)} {len(dsc_bytes)} {dsc_name}\n"
    f" {md5(orig)} {len(orig)} {orig_name}\n"
    f" {md5(debian)} {len(debian)} {debian_name}\n"
    "Checksums-Sha256:\n"
    f" {sha256(dsc_bytes)} {len(dsc_bytes)} {dsc_name}\n"
    f" {sha256(orig)} {len(orig)} {orig_name}\n"
    f" {sha256(debian)} {len(debian)} {debian_name}\n"
    "Homepage: https://example.invalid/edge-filter\n"
).encode()
if (dist / "Sources").read_bytes() != sources:
    raise AssertionError("Sources content, field order, checksums, or newline is incorrect")
if read_gzip_no_name(dist / "Sources.gz") != sources:
    raise AssertionError("Sources.gz payload does not match Sources")
sources_gz = (dist / "Sources.gz").read_bytes()

release = (
    "Origin: Acme Offline Source Repository\n"
    "Label: Acme Source\n"
    "Suite: stable\n"
    "Codename: stable\n"
    "Date: Tue, 02 Apr 2024 00:00:00 UTC\n"
    "Architectures: source\n"
    "Components: main\n"
    "Description: Offline deterministic Debian source repository\n"
    "MD5Sum:\n"
    f" {md5(sources)} {len(sources):16d} main/source/Sources\n"
    f" {md5(sources_gz)} {len(sources_gz):16d} main/source/Sources.gz\n"
    "SHA1:\n"
    f" {sha1(sources)} {len(sources):16d} main/source/Sources\n"
    f" {sha1(sources_gz)} {len(sources_gz):16d} main/source/Sources.gz\n"
    "SHA256:\n"
    f" {sha256(sources)} {len(sources):16d} main/source/Sources\n"
    f" {sha256(sources_gz)} {len(sources_gz):16d} main/source/Sources.gz\n"
).encode()
if (repo / "dists/stable/Release").read_bytes() != release:
    raise AssertionError("Release content, checksum sections, sizes, or newline is incorrect")

expected_sums = "".join(
    f"{sha256((repo / rel).read_bytes())}  {rel}\n"
    for rel in sorted(p for p in expected_files if p != "SHA256SUMS")
).encode()
if (repo / "SHA256SUMS").read_bytes() != expected_sums:
    raise AssertionError("SHA256SUMS content, ordering, spacing, or newline is incorrect")
PY

echo 1 > /logs/verifier/reward.txt
