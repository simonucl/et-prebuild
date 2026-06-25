#!/bin/bash
set -u

mkdir -p /logs/verifier
reward=0

fail() {
  echo "FAIL: $*" >&2
  echo "$reward" > /logs/verifier/reward.txt
  exit 0
}

repo=/home/user/aptrepo
pkg="$repo/pool/main/e/edge-agent/edge-agent_1.2.3_all.deb"
pkgdir="$repo/dists/stable/main/binary-amd64"
packages="$pkgdir/Packages"
packages_gz="$pkgdir/Packages.gz"
release="$repo/dists/stable/Release"
sources=/home/user/apt-client/sources.list

command -v apt-ftparchive >/dev/null 2>&1 || fail "apt-ftparchive is not installed"
command -v python3 >/dev/null 2>&1 || fail "python3 is not installed"

[ -f "$pkg" ] || fail "expected .deb package is missing"
sha256sum -c /opt/aptrepo-expected/edge-agent_1.2.3_all.deb.sha256 >/tmp/pkg.sha256.check 2>&1 || fail "the staged .deb package was modified"

[ -f "$packages" ] || fail "Packages file is missing"
[ -f "$packages_gz" ] || fail "Packages.gz file is missing"
[ -f "$release" ] || fail "Release file is missing"
[ -f "$sources" ] || fail "sources.list is missing"

tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

(cd "$repo" && apt-ftparchive packages pool > "$tmpdir/Packages.expected") || fail "could not generate expected Packages file"
cmp -s "$tmpdir/Packages.expected" "$packages" || fail "Packages is not the exact apt-ftparchive index for pool/"

gzip -n -c "$packages" > "$tmpdir/Packages.gz.expected" || fail "could not generate expected Packages.gz"
cmp -s "$tmpdir/Packages.gz.expected" "$packages_gz" || fail "Packages.gz is not the deterministic gzip -n form of Packages"

printf 'deb [trusted=yes] file:/home/user/aptrepo stable main\n' > "$tmpdir/sources.expected"
cmp -s "$tmpdir/sources.expected" "$sources" || fail "sources.list does not point exactly at the trusted local file repository"

python3 - "$repo" "$release" <<'PY' || fail "Release metadata or checksums are incorrect"
import hashlib
import sys
from pathlib import Path

repo = Path(sys.argv[1])
release_path = Path(sys.argv[2])
lines = release_path.read_text().splitlines()

required_fields = {
    "Origin": "Acme Offline",
    "Label": "Acme Edge",
    "Suite": "stable",
    "Codename": "stable",
    "Architectures": "amd64",
    "Components": "main",
}

fields = {}
sections = {}
current = None
for line in lines:
    if not line:
        continue
    if not line.startswith(" ") and ":" in line:
        key, value = line.split(":", 1)
        value = value.strip()
        if key in {"MD5Sum", "SHA1", "SHA256", "SHA512"}:
            current = key
            sections[current] = []
        else:
            fields[key] = value
            current = None
    elif line.startswith(" ") and current:
        parts = line.split()
        if len(parts) != 3:
            raise SystemExit(f"bad checksum line in {current}: {line!r}")
        digest, size, rel = parts
        sections[current].append((digest, int(size), rel))
    else:
        raise SystemExit(f"unparseable Release line: {line!r}")

for key, expected in required_fields.items():
    if fields.get(key) != expected:
        raise SystemExit(f"{key} is {fields.get(key)!r}, expected {expected!r}")

expected_paths = [
    "main/binary-amd64/Packages",
    "main/binary-amd64/Packages.gz",
]
algos = {
    "MD5Sum": "md5",
    "SHA1": "sha1",
    "SHA256": "sha256",
    "SHA512": "sha512",
}

for section, algo in algos.items():
    entries = sections.get(section)
    if entries is None:
        raise SystemExit(f"missing {section} section")
    if [rel for _, _, rel in entries] != expected_paths:
        raise SystemExit(f"{section} paths/order are wrong: {entries!r}")
    for digest, size, rel in entries:
        data = (repo / "dists/stable" / rel).read_bytes()
        if size != len(data):
            raise SystemExit(f"{section} size for {rel} is wrong")
        actual = hashlib.new(algo, data).hexdigest()
        if digest != actual:
            raise SystemExit(f"{section} digest for {rel} is wrong")
PY

empty_parts="$tmpdir/empty-sourceparts"
state="$tmpdir/state"
cache="$tmpdir/cache"
mkdir -p "$empty_parts" "$state/lists/partial" "$cache/archives/partial"

apt-get \
  -o Dir::Etc::sourcelist="$sources" \
  -o Dir::Etc::sourceparts="$empty_parts" \
  -o Dir::Etc::main=/dev/null \
  -o Dir::State="$state" \
  -o Dir::Cache="$cache" \
  -o Debug::NoLocking=1 \
  update >/tmp/aptrepo-update.log 2>&1 || fail "apt-get update could not use the local repository"

apt-cache \
  -o Dir::Etc::sourcelist="$sources" \
  -o Dir::Etc::sourceparts="$empty_parts" \
  -o Dir::Etc::main=/dev/null \
  -o Dir::State="$state" \
  -o Dir::Cache="$cache" \
  policy edge-agent > "$tmpdir/policy.txt" 2>&1 || fail "apt-cache policy failed"

grep -q 'Candidate: 1.2.3' "$tmpdir/policy.txt" || fail "edge-agent candidate is not version 1.2.3"

reward=1
echo "$reward" > /logs/verifier/reward.txt
exit 0
