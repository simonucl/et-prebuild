#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import gzip
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

lab = Path("/home/user/apt_lab")
src = lab / "packages"
repo = lab / "repo"
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

if repo.exists():
    shutil.rmtree(repo)
(repo / "dists/bookworm/main/binary-amd64").mkdir(parents=True)

records = []
for package in sorted(pool_paths):
    rel = pool_paths[package]
    source_deb = src / rel.name
    dest_deb = repo / rel
    dest_deb.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_deb, dest_deb)

    control = subprocess.check_output(
        ["dpkg-deb", "-f", str(dest_deb)], text=True
    )
    data = {}
    current = None
    for line in control.splitlines():
        if not line:
            continue
        if line.startswith((" ", "\t")) and current:
            data[current] += "\n" + line
        else:
            key, value = line.split(":", 1)
            current = key
            data[key] = value.strip()
    data["Filename"] = rel.as_posix()
    data["Size"] = str(dest_deb.stat().st_size)
    data["SHA256"] = hashlib.sha256(dest_deb.read_bytes()).hexdigest()
    records.append(data)

packages_text = ""
for data in records:
    for key in field_order:
        if key in data:
            packages_text += f"{key}: {data[key]}\n"
    packages_text += "\n"

packages_path = repo / "dists/bookworm/main/binary-amd64/Packages"
packages_path.write_text(packages_text, encoding="utf-8")
packages_gz_path = packages_path.with_name("Packages.gz")
with gzip.GzipFile(filename="", mode="wb", fileobj=packages_gz_path.open("wb"), compresslevel=9, mtime=0) as gz:
    gz.write(packages_path.read_bytes())

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

packages_rel = Path("main/binary-amd64/Packages")
packages_gz_rel = Path("main/binary-amd64/Packages.gz")
release = (
    "Origin: Acme Offline\n"
    "Label: Acme Edge Apt\n"
    "Suite: stable\n"
    "Codename: bookworm\n"
    "Date: Thu, 25 Jun 2026 00:00:00 UTC\n"
    "Architectures: amd64\n"
    "Components: main\n"
    "Description: Acme edge offline repository\n"
    "SHA256:\n"
    f" {digest(packages_path)} {packages_path.stat().st_size} {packages_rel.as_posix()}\n"
    f" {digest(packages_gz_path)} {packages_gz_path.stat().st_size} {packages_gz_rel.as_posix()}\n"
)
release_path = repo / "dists/bookworm/Release"
release_path.write_text(release, encoding="utf-8")

manifest = {
    "repo": "/home/user/apt_lab/repo",
    "codename": "bookworm",
    "suite": "stable",
    "architecture": "amd64",
    "packages": ["edge-meter=1.4.0-1", "edge-relay=0.8.2-2"],
    "release_sha256": digest(release_path),
    "packages_sha256": digest(packages_path),
    "packages_gz_sha256": digest(packages_gz_path),
}
(repo / "manifest.json").write_text(
    json.dumps(manifest, separators=(",", ":")) + "\n",
    encoding="utf-8",
)
PY
