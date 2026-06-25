#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import gzip
import hashlib
import json
import shutil
import subprocess
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

if repo.exists():
    shutil.rmtree(repo)
binary_dir.mkdir(parents=True, exist_ok=True)

for source_name, relative in pool_map.items():
    target = repo / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(packages_dir / source_name, target)

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
    data = deb.read_bytes()
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

packages_text = ""
for record in records:
    for key, value in record.items():
        if "\n" in value:
            first, *rest = value.split("\n")
            packages_text += f"{key}: {first}\n"
            packages_text += "\n".join(rest) + "\n"
        else:
            packages_text += f"{key}: {value}\n"
    packages_text += "\n"

packages_path = binary_dir / "Packages"
packages_path.write_text(packages_text, encoding="utf-8")

with gzip.GzipFile(filename="", mode="wb", fileobj=(binary_dir / "Packages.gz").open("wb"), compresslevel=9, mtime=0) as gz:
    gz.write(packages_path.read_bytes())

def digest(path: Path, name: str) -> str:
    h = hashlib.new(name)
    h.update(path.read_bytes())
    return h.hexdigest()

index_paths = [
    ("main/binary-amd64/Packages", packages_path),
    ("main/binary-amd64/Packages.gz", binary_dir / "Packages.gz"),
]

release = (
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
    release += f" {digest(path, 'md5')} {path.stat().st_size} {rel}\n"
release += "SHA1:\n"
for rel, path in index_paths:
    release += f" {digest(path, 'sha1')} {path.stat().st_size} {rel}\n"
release += "SHA256:\n"
for rel, path in index_paths:
    release += f" {digest(path, 'sha256')} {path.stat().st_size} {rel}\n"
release_path.write_text(release, encoding="utf-8")

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

manifest = OrderedDict([
    ("repository", "/home/user/apt-lab/repo"),
    ("suite", "stable"),
    ("architecture", "amd64"),
    ("packages", manifest_packages),
    ("release_sha256", digest(release_path, "sha256")),
])
(repo / "repo-manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n", encoding="utf-8")
PY
