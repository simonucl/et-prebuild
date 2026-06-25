#!/bin/bash
set -u

mkdir -p /logs/verifier

if python3 - <<'PY'
import gzip
import io
import hashlib
import json
import shutil
import subprocess
import sys
from collections import OrderedDict
from pathlib import Path

root = Path("/home/user/apt-lab")
packages_dir = root / "packages"
repo = root / "repo"
binary_dir = repo / "dists/stable/main/binary-amd64"
release_path = repo / "dists/stable/Release"

pool_map = {
    "acme-edge-agent_1.4.0_amd64.deb": "pool/main/a/acme-edge-agent/acme-edge-agent_1.4.0_amd64.deb",
    "acme-edge-rules_2026.6-1_amd64.deb": "pool/main/a/acme-edge-rules/acme-edge-rules_2026.6-1_amd64.deb",
}

def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)

def read(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except FileNotFoundError:
        fail(f"missing required file: {path}")

def digest_bytes(data: bytes, name: str) -> str:
    h = hashlib.new(name)
    h.update(data)
    return h.hexdigest()

def digest(path: Path, name: str) -> str:
    return digest_bytes(read(path), name)

expected_files = {
    "dists/stable/Release",
    "dists/stable/main/binary-amd64/Packages",
    "dists/stable/main/binary-amd64/Packages.gz",
    "pool/main/a/acme-edge-agent/acme-edge-agent_1.4.0_amd64.deb",
    "pool/main/a/acme-edge-rules/acme-edge-rules_2026.6-1_amd64.deb",
    "repo-manifest.json",
}
actual_files = {
    str(path.relative_to(repo))
    for path in repo.rglob("*")
    if path.is_file()
}
if actual_files != expected_files:
    fail(f"repository file set is wrong: {sorted(actual_files)}")

for source_name, relative in pool_map.items():
    if read(packages_dir / source_name) != read(repo / relative):
        fail(f"{relative} does not exactly match staged package bytes")

def control_fields(deb: Path) -> OrderedDict:
    text = subprocess.check_output(["dpkg-deb", "-f", str(deb)], text=True)
    fields = OrderedDict()
    current = None
    for line in text.splitlines():
        if line.startswith(" ") and current:
            fields[current] += "\n" + line
        elif ":" in line:
            key, value = line.split(":", 1)
            fields[key] = value.lstrip()
            current = key
    return fields

records = []
for source_name, relative in pool_map.items():
    deb = repo / relative
    fields = control_fields(deb)
    data = read(deb)
    record = OrderedDict()
    for key in ["Package", "Version", "Architecture", "Maintainer", "Installed-Size", "Depends", "Section", "Priority"]:
        record[key] = fields.get(key, "")
    record["Filename"] = relative
    record["Size"] = str(len(data))
    record["MD5sum"] = hashlib.md5(data).hexdigest()
    record["SHA1"] = hashlib.sha1(data).hexdigest()
    record["SHA256"] = hashlib.sha256(data).hexdigest()
    record["Description"] = fields["Description"]
    records.append(record)
records.sort(key=lambda item: item["Package"])

expected_packages = ""
for record in records:
    for key, value in record.items():
        if "\n" in value:
            first, *rest = value.split("\n")
            expected_packages += f"{key}: {first}\n"
            expected_packages += "\n".join(rest) + "\n"
        else:
            expected_packages += f"{key}: {value}\n"
    expected_packages += "\n"
if read(binary_dir / "Packages") != expected_packages.encode():
    fail("Packages content, field order, checksums, description continuation, sorting, or trailing blank lines are incorrect")

buf = io.BytesIO()
with gzip.GzipFile(filename="", mode="wb", fileobj=buf, compresslevel=9, mtime=0) as gz:
    gz.write(expected_packages.encode())
expected_gz = buf.getvalue()
if read(binary_dir / "Packages.gz") != expected_gz:
    fail("Packages.gz is not the required deterministic gzip stream")
try:
    if gzip.decompress(read(binary_dir / "Packages.gz")) != expected_packages.encode():
        fail("Packages.gz does not decompress to Packages")
except Exception as exc:
    fail(f"Packages.gz is not valid gzip: {exc}")

index_paths = [
    ("main/binary-amd64/Packages", binary_dir / "Packages"),
    ("main/binary-amd64/Packages.gz", binary_dir / "Packages.gz"),
]
expected_release = (
    "Origin: Acme Edge Offline\n"
    "Label: Acme Edge Offline\n"
    "Suite: stable\n"
    "Codename: stable\n"
    "Date: Thu, 25 Jun 2026 00:00:00 UTC\n"
    "Architectures: amd64\n"
    "Components: main\n"
    "Description: Offline Acme edge package repository\n"
    "MD5Sum:\n"
)
for rel, path in index_paths:
    expected_release += f" {digest(path, 'md5')} {path.stat().st_size} {rel}\n"
expected_release += "SHA1:\n"
for rel, path in index_paths:
    expected_release += f" {digest(path, 'sha1')} {path.stat().st_size} {rel}\n"
expected_release += "SHA256:\n"
for rel, path in index_paths:
    expected_release += f" {digest(path, 'sha256')} {path.stat().st_size} {rel}\n"
if read(release_path) != expected_release.encode():
    fail("Release content, field order, checksum sections, sizes, paths, or trailing newline are incorrect")

manifest_packages = []
for record in records:
    deb = repo / record["Filename"]
    manifest_packages.append(OrderedDict([
        ("name", record["Package"]),
        ("version", record["Version"]),
        ("filename", record["Filename"]),
        ("sha256", record["SHA256"]),
        ("size_bytes", deb.stat().st_size),
    ]))
expected_manifest = OrderedDict([
    ("repository", "/home/user/apt-lab/repo"),
    ("suite", "stable"),
    ("architecture", "amd64"),
    ("packages", manifest_packages),
    ("release_sha256", digest(release_path, "sha256")),
])
expected_manifest_bytes = json.dumps(expected_manifest, separators=(",", ":")).encode() + b"\n"
if read(repo / "repo-manifest.json") != expected_manifest_bytes:
    fail("repo-manifest.json content, key order, digest, minification, or trailing newline is incorrect")

print("ok")
PY
then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
  exit 1
fi
