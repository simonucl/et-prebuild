#!/bin/bash
set -u

mkdir -p /logs/verifier
reward_file=/logs/verifier/reward.txt
echo 0 > "$reward_file"

fail() {
  echo "FAIL: $*" >&2
  echo 0 > "$reward_file"
  exit 1
}

cd /home/user/repo_lab || fail "missing /home/user/repo_lab"

python3 <<'PY' || fail "repository metadata validation failed"
import gzip
import hashlib
import json
import os
import re
import sys
from pathlib import Path

root = Path("/home/user/repo_lab")
packages_path = root / "dists/stable/main/binary-amd64/Packages"
packages_gz_path = root / "dists/stable/main/binary-amd64/Packages.gz"
release_path = root / "dists/stable/Release"
manifest_path = root / "manifest.json"


def die(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def read_bytes(path):
    if not path.is_file():
        die(f"missing regular file: {path}")
    return path.read_bytes()


packages_data = read_bytes(packages_path)
packages_gz_data = read_bytes(packages_gz_path)
release_text = read_bytes(release_path).decode()
manifest_raw = read_bytes(manifest_path)

if gzip.decompress(packages_gz_data) != packages_data:
    die("Packages.gz does not decompress exactly to Packages")

if len(packages_gz_data) < 10 or packages_gz_data[:2] != b"\x1f\x8b":
    die("Packages.gz is not a gzip stream")
flags = packages_gz_data[3]
mtime = int.from_bytes(packages_gz_data[4:8], "little")
if flags & 0x08 or mtime != 0:
    die("Packages.gz must be made with no embedded filename and no embedded timestamp")

stanzas = []
for block in packages_data.decode().strip().split("\n\n"):
    fields = {}
    current = None
    for line in block.splitlines():
        if line.startswith(" "):
            continue
        if ":" not in line:
            die(f"malformed Packages line: {line!r}")
        key, value = line.split(":", 1)
        fields[key] = value.strip()
        current = key
    if fields:
        stanzas.append(fields)

expected = [
    ("acme-metrics-agent", "1.4.1", "amd64", "pool/main/a/acme-metrics-agent/acme-metrics-agent_1.4.1_amd64.deb"),
    ("acme-metrics-tools", "0.9.0", "all", "pool/main/a/acme-metrics-tools/acme-metrics-tools_0.9.0_all.deb"),
]

actual = [(s.get("Package"), s.get("Version"), s.get("Architecture"), s.get("Filename")) for s in stanzas]
if actual != expected:
    die(f"unexpected published package set/order: {actual!r}")

for stanza, (_, _, _, filename) in zip(stanzas, expected):
    deb = root / filename
    data = read_bytes(deb)
    size = str(len(data))
    sha = hashlib.sha256(data).hexdigest()
    if stanza.get("Size") != size:
        die(f"wrong Size for {filename}")
    if stanza.get("SHA256") != sha:
        die(f"wrong SHA256 for {filename}")
    if "MD5sum" not in stanza or "SHA1" not in stanza:
        die(f"missing expected checksum fields for {filename}")

if b"Version: 1.4.0\n" in packages_data:
    die("superseded acme-metrics-agent 1.4.0 is still published")

def digest(path):
    data = read_bytes(path)
    return hashlib.sha256(data).hexdigest(), len(data)

packages_sha, packages_size = digest(packages_path)
packages_gz_sha, packages_gz_size = digest(packages_gz_path)
expected_release = (
    "Archive: stable\n"
    "Codename: stable\n"
    "Suite: stable\n"
    "Component: main\n"
    "Origin: Acme Offline Ops\n"
    "Label: Acme Metrics Local Repo\n"
    "Architectures: amd64\n"
    "Date: Wed, 15 Jan 2025 00:00:00 +0000\n"
    "SHA256:\n"
    f" {packages_sha} {packages_size} main/binary-amd64/Packages\n"
    f" {packages_gz_sha} {packages_gz_size} main/binary-amd64/Packages.gz\n"
)
if release_text != expected_release:
    die("Release file content is not exactly the required metadata")

if not manifest_raw.endswith(b"\n") or b"\n" in manifest_raw[:-1]:
    die("manifest.json must be one minified JSON line with one trailing newline")

agent_deb = root / expected[0][3]
tools_deb = root / expected[1][3]
expected_manifest = {
    "architecture": "amd64",
    "component": "main",
    "packages": [
        {
            "name": "acme-metrics-agent",
            "version": "1.4.1",
            "filename": expected[0][3],
            "sha256": hashlib.sha256(read_bytes(agent_deb)).hexdigest(),
        },
        {
            "name": "acme-metrics-tools",
            "version": "0.9.0",
            "filename": expected[1][3],
            "sha256": hashlib.sha256(read_bytes(tools_deb)).hexdigest(),
        },
    ],
    "suite": "stable",
}
expected_manifest_raw = json.dumps(expected_manifest, separators=(",", ":")).encode() + b"\n"
if manifest_raw != expected_manifest_raw:
    die("manifest.json content is not exactly the required minified JSON")

for extra in [root / "dists/stable/InRelease", root / "dists/stable/Release.gpg"]:
    if extra.exists():
        die(f"unexpected signing artifact: {extra}")
PY

mkdir -p /tmp/apt-empty /tmp/apt-state/lists/partial /tmp/apt-cache/archives/partial
cat > /tmp/acme-local.sources.list <<'EOF'
deb [trusted=yes] file:/home/user/repo_lab stable main
EOF

apt_opts=(
  -o Dir::Etc::sourcelist=/tmp/acme-local.sources.list
  -o Dir::Etc::sourceparts=/tmp/apt-empty
  -o Dir::Etc::main=/dev/null
  -o Dir::State::lists=/tmp/apt-state/lists
  -o Dir::Cache=/tmp/apt-cache
  -o APT::Get::List-Cleanup=0
)

apt-get "${apt_opts[@]}" update >/tmp/acme-apt-update.log 2>&1 || {
  cat /tmp/acme-apt-update.log >&2
  fail "apt-get update could not read the repaired file repository"
}

apt-cache "${apt_opts[@]}" policy acme-metrics-agent acme-metrics-tools >/tmp/acme-policy.log 2>&1 || fail "apt-cache policy failed"
grep -q 'Candidate: 1.4.1' /tmp/acme-policy.log || fail "acme-metrics-agent candidate is not 1.4.1"
grep -q 'Candidate: 0.9.0' /tmp/acme-policy.log || fail "acme-metrics-tools candidate is not 0.9.0"
if grep -q '1.4.0' /tmp/acme-policy.log; then
  cat /tmp/acme-policy.log >&2
  fail "superseded acme-metrics-agent 1.4.0 is visible to APT"
fi

apt-get "${apt_opts[@]}" -s install acme-metrics-agent=1.4.1 acme-metrics-tools=0.9.0 >/tmp/acme-install.log 2>&1 || {
  cat /tmp/acme-install.log >&2
  fail "APT cannot simulate installing the published packages"
}

echo 1 > "$reward_file"
