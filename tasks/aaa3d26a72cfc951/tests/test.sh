#!/bin/bash
set -u

reward_file="${TASK_ROOT:-}/logs/verifier/reward.txt"
mkdir -p "$(dirname "$reward_file")"

if python3 - <<'PY'
import hashlib
import json
import shutil
import sys
import tempfile
import zipfile
import os
from pathlib import Path

root = Path(os.environ.get("TASK_ROOT") or "/")
lab = root / "home/user/vsix_lab"
src = lab / "src" / "extension"
dist = lab / "dist"
vsix_name = "acme-log-tools-0.9.1.vsix"
manifest_name = "vsix-manifest.json"
sha_name = "SHA256SUMS"

def fail(message):
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)

if not src.is_dir():
    fail("source extension directory is missing")
if not dist.is_dir():
    fail("dist directory is missing")

actual_dist = sorted(p.name for p in dist.iterdir())
if actual_dist != [sha_name, vsix_name, manifest_name]:
    fail(f"dist contains wrong files: {actual_dist}")

package = {
    "name": "acme-log-tools",
    "displayName": "Acme Log Tools",
    "description": "Offline syntax support for Acme service log captures.",
    "version": "0.9.1",
    "publisher": "acme-corp",
    "license": "MIT",
    "engines": {"vscode": "^1.92.0"},
    "categories": ["Programming Languages", "Snippets"],
    "contributes": {
        "languages": [
            {
                "id": "acme-log",
                "aliases": ["Acme Log", "acme-log"],
                "extensions": [".acmelog"],
                "configuration": "./syntaxes/acme-log.tmLanguage.json",
            }
        ],
        "snippets": [
            {
                "language": "acme-log",
                "path": "./snippets/acme-log.json",
            }
        ],
    },
}

content_types = (
    '<?xml version="1.0" encoding="utf-8"?>\n'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n'
    '  <Default Extension="json" ContentType="application/json"/>\n'
    '  <Default Extension="md" ContentType="text/markdown"/>\n'
    '  <Default Extension="txt" ContentType="text/plain"/>\n'
    '  <Override PartName="/extension.vsixmanifest" ContentType="text/xml"/>\n'
    '</Types>\n'
).encode()

vsixmanifest = (
    '<?xml version="1.0" encoding="utf-8"?>\n'
    '<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011">\n'
    '  <Metadata>\n'
    '    <Identity Id="acme-log-tools" Version="0.9.1" Language="en-US" Publisher="acme-corp"/>\n'
    '    <DisplayName>Acme Log Tools</DisplayName>\n'
    '    <Description xml:space="preserve">Offline syntax support for Acme service log captures.</Description>\n'
    '    <License>extension/LICENSE</License>\n'
    '    <Tags>acme,logs,syntax</Tags>\n'
    '    <Categories>Programming Languages,Snippets</Categories>\n'
    '  </Metadata>\n'
    '  <Installation>\n'
    '    <InstallationTarget Id="Microsoft.VisualStudio.Code"/>\n'
    '  </Installation>\n'
    '  <Dependencies/>\n'
    '  <Assets>\n'
    '    <Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json"/>\n'
    '  </Assets>\n'
    '</PackageManifest>\n'
).encode()

expected_members = [
    ("[Content_Types].xml", content_types),
    ("extension.vsixmanifest", vsixmanifest),
    ("extension/package.json", (json.dumps(package, separators=(",", ":")) + "\n").encode()),
    ("extension/README.md", (src / "README.md").read_bytes()),
    ("extension/LICENSE", (src / "LICENSE").read_bytes()),
    ("extension/syntaxes/acme-log.tmLanguage.json", (src / "syntaxes/acme-log.tmLanguage.json").read_bytes()),
    ("extension/snippets/acme-log.json", (src / "snippets/acme-log.json").read_bytes()),
]
expected_names = [name for name, _ in expected_members]

vsix_path = dist / vsix_name
if not vsix_path.is_file():
    fail("VSIX is missing")

try:
    with zipfile.ZipFile(vsix_path, "r") as zf:
        infos = zf.infolist()
        names = [info.filename for info in infos]
        if names != expected_names:
            fail(f"unexpected VSIX member order or members: {names}")
        if any(name.endswith("/") for name in names):
            fail("VSIX must not contain directory entries")
        contents = {}
        for info in infos:
            if info.date_time != (2026, 6, 25, 0, 0, 0):
                fail(f"{info.filename} has timestamp {info.date_time}")
            if info.compress_type != zipfile.ZIP_DEFLATED:
                fail(f"{info.filename} is not deflated")
            mode = (info.external_attr >> 16) & 0o7777
            if mode != 0o644:
                fail(f"{info.filename} mode is {oct(mode)}, expected 0644")
            contents[info.filename] = zf.read(info.filename)
except zipfile.BadZipFile:
    fail("VSIX is not a valid ZIP archive")

for name, expected in expected_members:
    if contents.get(name) != expected:
        fail(f"{name} content is wrong")
    if name.endswith(".json") and (not expected.endswith(b"\n") or expected.endswith(b"\n\n")):
        fail(f"{name} must end with exactly one newline")

with tempfile.TemporaryDirectory() as tmp:
    expected_zip = Path(tmp) / vsix_name
    with zipfile.ZipFile(expected_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for name, data in expected_members:
            info = zipfile.ZipInfo(name, date_time=(2026, 6, 25, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, data)
    if vsix_path.read_bytes() != expected_zip.read_bytes():
        fail("VSIX bytes are not the required deterministic archive")

def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

expected_manifest = {
    "package": "acme-log-tools",
    "version": "0.9.1",
    "vsix": vsix_name,
    "members": [
        {"path": name, "bytes": len(data), "sha256": sha_bytes(data)}
        for name, data in expected_members
    ],
    "vsix_sha256": sha_bytes(vsix_path.read_bytes()),
}
expected_manifest_raw = json.dumps(expected_manifest, separators=(",", ":")) + "\n"
actual_manifest_raw = (dist / manifest_name).read_text()
if actual_manifest_raw != expected_manifest_raw:
    fail("vsix-manifest.json content, key order, minification, or trailing newline is wrong")

expected_sums = (
    f"{sha_bytes(vsix_path.read_bytes())}  {vsix_name}\n"
    f"{sha_bytes(actual_manifest_raw.encode())}  {manifest_name}\n"
)
if (dist / sha_name).read_text() != expected_sums:
    fail("SHA256SUMS content is wrong")

for forbidden in ["NOTES.txt", ".DS_Store", "old-checksums.txt", "acme-log-tools-0.8.0.vsix"]:
    if forbidden in "\n".join(expected_names) or (dist / forbidden).exists():
        fail(f"forbidden file leaked or stale artifact remains: {forbidden}")

print("VSIX handoff validated")
PY
then
  echo 1 > "$reward_file"
else
  echo 0 > "$reward_file"
fi
