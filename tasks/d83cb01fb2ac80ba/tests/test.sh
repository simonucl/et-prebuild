#!/bin/bash
set -euo pipefail

mkdir -p /logs/verifier

python3 - <<'PY'
import hashlib
import json
import sys
import zipfile
from pathlib import Path

reward_path = Path("/logs/verifier/reward.txt")
repo = Path("/app/mirror/registry.acme.test/acme/edgeaudit")
src = Path("/app/provider-src")
archive_name = "terraform-provider-edgeaudit_0.4.2_linux_amd64.zip"
archive_path = repo / archive_name

def fail(message: str) -> None:
    print(f"FAIL: {message}")
    reward_path.write_text("0\n", encoding="utf-8")
    sys.exit(0)

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

expected_source = {}
source_manifest = src / "SOURCE.sha256"
if not source_manifest.is_file():
    fail("missing source checksum manifest")
for line in source_manifest.read_text(encoding="utf-8").splitlines():
    digest, path = line.split(maxsplit=1)
    expected_source[Path(path).name] = digest

for name, expected_digest in expected_source.items():
    candidate = src / name
    if not candidate.is_file():
        fail(f"source file was removed: {name}")
    if sha256_bytes(candidate.read_bytes()) != expected_digest:
        fail(f"source file was modified: {name}")

expected_files = {
    "index.json",
    "0.4.2.json",
    archive_name,
    "manifest.json",
}
actual_files = {
    str(path.relative_to(repo))
    for path in repo.rglob("*")
    if path.is_file() or path.is_symlink()
}
if actual_files != expected_files:
    fail(f"mirror file set mismatch: {sorted(actual_files)}")

if any(path.is_symlink() for path in repo.rglob("*")):
    fail("mirror must not contain symlinks")

if (repo / "index.json").read_text(encoding="utf-8") != '{"versions":{"0.4.2":{"protocols":["5.0"]}}}\n':
    fail("index.json content, key order, minification, or trailing newline is incorrect")

expected_zip_members = [
    ("terraform-provider-edgeaudit_v0.4.2", 0o755),
    ("LICENSE.txt", 0o644),
]

if not archive_path.is_file():
    fail("missing linux_amd64 provider ZIP")

with zipfile.ZipFile(archive_path, "r") as zf:
    infos = zf.infolist()
    names = [info.filename for info in infos]
    if names != [name for name, _mode in expected_zip_members]:
        fail(f"ZIP member order or file set is wrong: {names}")
    for info, (name, mode) in zip(infos, expected_zip_members):
        if info.date_time != (2024, 1, 1, 0, 0, 0):
            fail(f"ZIP timestamp is not normalized for {name}")
        if info.compress_type != zipfile.ZIP_DEFLATED:
            fail(f"ZIP member is not deflated: {name}")
        actual_mode = (info.external_attr >> 16) & 0o777
        if actual_mode != mode:
            fail(f"ZIP mode for {name} is {oct(actual_mode)}, expected {oct(mode)}")
        if zf.read(name) != (src / name).read_bytes():
            fail(f"ZIP payload bytes do not match source for {name}")

zip_bytes = archive_path.read_bytes()
zip_sha = sha256_bytes(zip_bytes)
zip_size = len(zip_bytes)

try:
    version_doc = json.loads((repo / "0.4.2.json").read_text(encoding="utf-8"))
except json.JSONDecodeError as exc:
    fail(f"0.4.2.json is not valid JSON: {exc}")

expected_version_text = (
    '{"archives":{"linux_amd64":{"url":"'
    + archive_name
    + '","hashes":["zh:'
    + zip_sha
    + '"]}}}\n'
)
if (repo / "0.4.2.json").read_text(encoding="utf-8") != expected_version_text:
    fail("0.4.2.json content, hash, key order, minification, or trailing newline is incorrect")
if set(version_doc.get("archives", {}).keys()) != {"linux_amd64"}:
    fail("0.4.2.json must describe only linux_amd64")

expected_manifest_text = (
    '{"hostname":"registry.acme.test","namespace":"acme","type":"edgeaudit",'
    '"version":"0.4.2","platform":"linux_amd64","archive":"'
    + archive_name
    + '","sha256":"'
    + zip_sha
    + '","size":'
    + str(zip_size)
    + "}\n"
)
if (repo / "manifest.json").read_text(encoding="utf-8") != expected_manifest_text:
    fail("manifest.json content, derived values, key order, minification, or trailing newline is incorrect")

reward_path.write_text("1\n", encoding="utf-8")
print("PASS: Terraform provider mirror repaired")
PY
