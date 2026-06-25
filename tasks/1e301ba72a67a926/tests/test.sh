#!/bin/bash
set -u

mkdir -p /logs/verifier
reward=0

fail() {
  echo "$1" >&2
  echo "$reward" > /logs/verifier/reward.txt
  exit 0
}

src=/home/user/tf-mirror-lab/source/provider
mirror=/home/user/tf-mirror-lab/mirror/registry.terraform.io/acme/firewall
zip_name=terraform-provider-acmefirewall_0.4.2_linux_amd64.zip
zip_path="$mirror/$zip_name"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

[ -d "$mirror" ] || fail "mirror directory is missing"

mapfile -t mirror_files < <(find "$mirror" -mindepth 1 -maxdepth 1 -printf '%f\n' | sort)
expected_files=$'0.4.2.json\nSHA256SUMS\nindex.json\nterraform-provider-acmefirewall_0.4.2_linux_amd64.zip'
actual_files=$(printf '%s\n' "${mirror_files[@]}")
[ "$actual_files" = "$expected_files" ] || fail "mirror directory contains unexpected files: [$actual_files]"

if ! find "$src" -type f -printf '%P\0' \
  | sort -z \
  | xargs -0 -I{} sha256sum "$src/{}" \
  | sed "s#$src/##" > "$tmp/source.sha256"; then
  fail "could not hash provider source"
fi
cmp -s /opt/tf-mirror-lab/source.sha256 "$tmp/source.sha256" || fail "provider source tree was modified"

[ -f "$zip_path" ] || fail "provider zip is missing"
[ -f "$mirror/index.json" ] || fail "index.json is missing"
[ -f "$mirror/0.4.2.json" ] || fail "0.4.2.json is missing"
[ -f "$mirror/SHA256SUMS" ] || fail "SHA256SUMS is missing"

if ! python3 - <<'PY'
import hashlib
import json
import sys
import zipfile
from pathlib import Path

src = Path("/home/user/tf-mirror-lab/source/provider")
mirror = Path("/home/user/tf-mirror-lab/mirror/registry.terraform.io/acme/firewall")
zip_name = "terraform-provider-acmefirewall_0.4.2_linux_amd64.zip"
zip_path = mirror / zip_name

def fail(message):
    print(message, file=sys.stderr)
    sys.exit(1)

expected_names = ["terraform-provider-acmefirewall_v0.4.2", "LICENSE.txt"]
expected_modes = {
    "terraform-provider-acmefirewall_v0.4.2": 0o755,
    "LICENSE.txt": 0o644,
}

try:
    with zipfile.ZipFile(zip_path, "r") as zf:
        infos = zf.infolist()
        names = [info.filename for info in infos]
        if names != expected_names:
            fail(f"unexpected zip members or order: {names}")
        if any(name.endswith("/") for name in names):
            fail("zip must not contain directory entries")
        for info in infos:
            if info.date_time != (2024, 6, 1, 0, 0, 0):
                fail(f"{info.filename} has non-normalized timestamp {info.date_time}")
            if info.compress_type != zipfile.ZIP_DEFLATED:
                fail(f"{info.filename} is not deflated")
            mode = (info.external_attr >> 16) & 0o7777
            if mode != expected_modes[info.filename]:
                fail(f"{info.filename} has mode {oct(mode)}, expected {oct(expected_modes[info.filename])}")
            if zf.read(info.filename) != (src / info.filename).read_bytes():
                fail(f"{info.filename} content does not match source")
except zipfile.BadZipFile:
    fail("provider zip is not a valid zip archive")

digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
expected_index = (
    '{"versions":{"0.4.2":{"protocols":["5.0"],'
    '"platforms":[{"os":"linux","arch":"amd64"}]}}}\n'
)
if (mirror / "index.json").read_text() != expected_index:
    fail("index.json content, key order, minification, or trailing newline is incorrect")

expected_version = (
    '{"archives":{"linux_amd64":{"url":"terraform-provider-acmefirewall_0.4.2_linux_amd64.zip",'
    f'"hashes":["zh:{digest}"]}}}}}}\n'
)
if (mirror / "0.4.2.json").read_text() != expected_version:
    fail("0.4.2.json content, digest, key order, minification, or trailing newline is incorrect")

expected_sha = f"{digest}  {zip_name}\n"
if (mirror / "SHA256SUMS").read_text() != expected_sha:
    fail("SHA256SUMS has the wrong digest, spacing, filename, or newline")
PY
then
  fail "metadata or provider zip validation failed"
fi

reward=1
echo "$reward" > /logs/verifier/reward.txt
echo "all checks passed"
