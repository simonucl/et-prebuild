#!/bin/bash
set -u

mkdir -p /logs/verifier

python3 - <<'PY'
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path

lab = Path("/home/user/apt_lab")
src = lab / "packages"
repo = lab / "repo"
dist = repo / "dists/bookworm/main/binary-amd64"
release_path = repo / "dists/bookworm/Release"
manifest_path = repo / "manifest.json"

pool_paths = {
    "edge-meter": Path("pool/main/e/edge-meter/edge-meter_1.4.0-1_amd64.deb"),
    "edge-relay": Path("pool/main/e/edge-relay/edge-relay_0.8.2-2_amd64.deb"),
}
field_order = [
    "Package",
    "Version",
    "Architecture",
    "Maintainer",
    "Installed-Size",
    "Depends",
    "Section",
    "Priority",
    "Homepage",
    "Filename",
    "Size",
    "SHA256",
    "Description",
]

def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)

def read(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except FileNotFoundError:
        fail(f"missing required file: {path}")

def digest(path: Path) -> str:
    return hashlib.sha256(read(path)).hexdigest()

def parse_control(deb: Path) -> dict[str, str]:
    try:
        control = subprocess.check_output(["dpkg-deb", "-f", str(deb)], text=True)
    except subprocess.CalledProcessError as exc:
        fail(f"could not read deb control metadata from {deb}: {exc}")
    data = {}
    current = None
    for line in control.splitlines():
        if not line:
            continue
        if line.startswith((" ", "\t")) and current:
            data[current] += "\n" + line
        else:
            if ":" not in line:
                fail(f"malformed control line in {deb}: {line!r}")
            key, value = line.split(":", 1)
            current = key
            data[key] = value.strip()
    return data

expected_repo_files = {
    "manifest.json",
    "dists/bookworm/Release",
    "dists/bookworm/main/binary-amd64/Packages",
    "dists/bookworm/main/binary-amd64/Packages.gz",
}
expected_repo_files.update(path.as_posix() for path in pool_paths.values())
actual_repo_files = {
    p.relative_to(repo).as_posix()
    for p in repo.rglob("*")
    if p.is_file()
}
if actual_repo_files != expected_repo_files:
    fail(f"repository file set is wrong: {sorted(actual_repo_files)}")

records = []
for package in sorted(pool_paths):
    rel = pool_paths[package]
    source_deb = src / rel.name
    repo_deb = repo / rel
    if read(source_deb) != read(repo_deb):
        fail(f"{rel} bytes do not match the staged package")
    data = parse_control(repo_deb)
    data["Filename"] = rel.as_posix()
    data["Size"] = str(repo_deb.stat().st_size)
    data["SHA256"] = digest(repo_deb)
    records.append(data)

expected_packages = ""
for data in records:
    for key in field_order:
        if key in data:
            expected_packages += f"{key}: {data[key]}\n"
    expected_packages += "\n"

packages_path = dist / "Packages"
packages_bytes = read(packages_path)
if packages_bytes != expected_packages.encode():
    fail("Packages content, field order, sorting, checksums, sizes, or trailing blank lines are incorrect")

packages_gz_path = dist / "Packages.gz"
packages_gz_bytes = read(packages_gz_path)
if packages_gz_bytes[:3] != b"\x1f\x8b\x08":
    fail("Packages.gz does not start with a gzip header")
if packages_gz_bytes[3] != 0:
    fail("Packages.gz stores optional gzip header fields such as an original filename")
if packages_gz_bytes[4:8] != b"\x00\x00\x00\x00":
    fail("Packages.gz gzip mtime is not zero")
try:
    if gzip.decompress(packages_gz_bytes) != packages_bytes:
        fail("Packages.gz does not decompress to the exact Packages bytes")
except OSError as exc:
    fail(f"Packages.gz is not valid gzip: {exc}")

release_expected = (
    "Origin: Acme Offline\n"
    "Label: Acme Edge Apt\n"
    "Suite: stable\n"
    "Codename: bookworm\n"
    "Date: Thu, 25 Jun 2026 00:00:00 UTC\n"
    "Architectures: amd64\n"
    "Components: main\n"
    "Description: Acme edge offline repository\n"
    "SHA256:\n"
    f" {digest(packages_path)} {packages_path.stat().st_size} main/binary-amd64/Packages\n"
    f" {digest(packages_gz_path)} {packages_gz_path.stat().st_size} main/binary-amd64/Packages.gz\n"
)
if read(release_path) != release_expected.encode():
    fail("Release content, header fields, checksum section, ordering, sizes, or trailing newline is incorrect")

manifest_expected = {
    "repo": "/home/user/apt_lab/repo",
    "codename": "bookworm",
    "suite": "stable",
    "architecture": "amd64",
    "packages": ["edge-meter=1.4.0-1", "edge-relay=0.8.2-2"],
    "release_sha256": digest(release_path),
    "packages_sha256": digest(packages_path),
    "packages_gz_sha256": digest(packages_gz_path),
}
expected_manifest_bytes = json.dumps(manifest_expected, separators=(",", ":")).encode() + b"\n"
if read(manifest_path) != expected_manifest_bytes:
    fail("manifest.json content, key order, hashes, minification, or trailing newline is incorrect")

print("ok")
PY

if [ "$?" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
