#!/bin/bash
set -euo pipefail

BASE="${APP_ROOT:-/app}"
SRC="$BASE/source/edge-filter"
REPO="$BASE/repo"
POOL="$REPO/pool/main/e/edge-filter"
DIST="$REPO/dists/stable/main/source"

rm -rf "$REPO"
mkdir -p "$POOL" "$DIST"

python3 - <<'PY'
import gzip
import hashlib
import io
import lzma
import os
from pathlib import Path
import tarfile

base = Path(os.environ.get("APP_ROOT", "/app"))
src = base / "source" / "edge-filter"
repo = base / "repo"
pool = repo / "pool/main/e/edge-filter"
dist = repo / "dists/stable/main/source"
mtime = 1712016000

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def md5(data):
    return hashlib.md5(data).hexdigest()

def sha1(data):
    return hashlib.sha1(data).hexdigest()

def tar_payload(entries):
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.GNU_FORMAT) as tf:
        for arcname, srcpath, mode in entries:
            data = srcpath.read_bytes()
            info = tarfile.TarInfo(arcname)
            info.size = len(data)
            info.mode = mode
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            info.mtime = mtime
            tf.addfile(info, io.BytesIO(data))
    return buf.getvalue()

orig_entries = [
    ("edge-filter-1.2.0/LICENSE", src / "LICENSE", 0o644),
    ("edge-filter-1.2.0/README.md", src / "README.md", 0o644),
    ("edge-filter-1.2.0/src/filter.py", src / "src/filter.py", 0o644),
]
debian_entries = [
    ("debian/changelog", src / "debian/changelog", 0o644),
    ("debian/control", src / "debian/control", 0o644),
    ("debian/rules", src / "debian/rules", 0o755),
]

orig_tar = tar_payload(orig_entries)
orig = gzip.compress(orig_tar, compresslevel=9, mtime=0)
debian_tar = tar_payload(debian_entries)
debian = lzma.compress(debian_tar, preset=9, format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC64)

orig_name = "edge-filter_1.2.0.orig.tar.gz"
debian_name = "edge-filter_1.2.0-1.debian.tar.xz"
dsc_name = "edge-filter_1.2.0-1.dsc"
(pool / orig_name).write_bytes(orig)
(pool / debian_name).write_bytes(debian)

def file_line(algo, data, name):
    digest = {"sha256": sha256, "md5": md5}[algo](data)
    return f" {digest} {len(data)} {name}\n"

dsc = (
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
)
(pool / dsc_name).write_text(dsc, encoding="utf-8")
dsc_bytes = dsc.encode()

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
)
sources_bytes = sources.encode()
(dist / "Sources").write_bytes(sources_bytes)
(dist / "Sources.gz").write_bytes(gzip.compress(sources_bytes, compresslevel=9, mtime=0))
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
    f" {md5(sources_bytes)} {len(sources_bytes):16d} main/source/Sources\n"
    f" {md5(sources_gz)} {len(sources_gz):16d} main/source/Sources.gz\n"
    "SHA1:\n"
    f" {sha1(sources_bytes)} {len(sources_bytes):16d} main/source/Sources\n"
    f" {sha1(sources_gz)} {len(sources_gz):16d} main/source/Sources.gz\n"
    "SHA256:\n"
    f" {sha256(sources_bytes)} {len(sources_bytes):16d} main/source/Sources\n"
    f" {sha256(sources_gz)} {len(sources_gz):16d} main/source/Sources.gz\n"
)
(repo / "dists/stable/Release").write_text(release, encoding="utf-8")

final_files = [
    "SHA256SUMS",
    "dists/stable/Release",
    "dists/stable/main/source/Sources",
    "dists/stable/main/source/Sources.gz",
    f"pool/main/e/edge-filter/{debian_name}",
    f"pool/main/e/edge-filter/{dsc_name}",
    f"pool/main/e/edge-filter/{orig_name}",
]
sum_lines = []
for rel in sorted(p for p in final_files if p != "SHA256SUMS"):
    data = (repo / rel).read_bytes()
    sum_lines.append(f"{sha256(data)}  {rel}\n")
(repo / "SHA256SUMS").write_text("".join(sum_lines), encoding="utf-8")
PY
