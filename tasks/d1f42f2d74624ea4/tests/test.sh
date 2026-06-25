#!/bin/bash
set -euo pipefail

mkdir -p /logs/verifier

python3 - <<'PY'
import base64
import hashlib
import json
import os
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

feed = Path("/app/nuget-feed/v3")
src = Path("/app/nuget-src")
errors = []

def fail(msg):
    errors.append(msg)

def read_json(path):
    data = path.read_bytes()
    if not data.endswith(b"\n") or data.endswith(b"\n\n"):
        fail(f"{path} must end with exactly one newline")
    if b"\n" in data[:-1]:
        fail(f"{path} must be single-line compact JSON")
    try:
        return json.loads(data)
    except Exception as exc:
        fail(f"{path} is not valid JSON: {exc}")
        return {}

expected_files = {
    "index.json",
    "flatcontainer/acme.edgerules/index.json",
    "flatcontainer/acme.edgerules/1.4.0/acme.edgerules.1.4.0.nupkg",
    "flatcontainer/acme.edgerules/1.4.0/acme.edgerules.nuspec",
    "registration/acme.edgerules/index.json",
}
actual_files = {
    str(p.relative_to(feed))
    for p in feed.rglob("*")
    if p.is_file()
}
if actual_files != expected_files:
    fail(f"feed file set mismatch: {sorted(actual_files)}")

nupkg = feed / "flatcontainer/acme.edgerules/1.4.0/acme.edgerules.1.4.0.nupkg"
nuspec_sidecar = feed / "flatcontainer/acme.edgerules/1.4.0/acme.edgerules.nuspec"

def bytes_or_empty(path, label):
    try:
        return path.read_bytes()
    except Exception as exc:
        fail(f"{label} missing or unreadable: {exc}")
        return b""

expected_order = [
    "[Content_Types].xml",
    "_rels/.rels",
    "Acme.EdgeRules.nuspec",
    "lib/net8.0/Acme.EdgeRules.dll",
    "buildTransitive/Acme.EdgeRules.props",
    "README.md",
    "LICENSE.txt",
]

try:
    with zipfile.ZipFile(nupkg) as zf:
        infos = zf.infolist()
        names = [i.filename for i in infos]
        if names != expected_order:
            fail(f"nupkg member order/content mismatch: {names}")
        for info in infos:
            if info.filename.endswith("/"):
                fail(f"directory entry present: {info.filename}")
            if info.date_time != (2024, 5, 6, 7, 8, 10):
                fail(f"{info.filename} has non-normalized timestamp {info.date_time}")
            if info.compress_type != zipfile.ZIP_DEFLATED:
                fail(f"{info.filename} is not deflated")
            mode = (info.external_attr >> 16) & 0o777
            if mode != 0o644:
                fail(f"{info.filename} mode is {oct(mode)}, expected 0o644")
        payload = {name: zf.read(name) for name in names}
except Exception as exc:
    fail(f"nupkg is not a valid zip: {exc}")
    payload = {}

sidecar_bytes = bytes_or_empty(nuspec_sidecar, "nuspec sidecar")

if payload.get("lib/net8.0/Acme.EdgeRules.dll") != bytes_or_empty(src / "lib/net8.0/Acme.EdgeRules.dll", "source DLL"):
    fail("DLL payload does not match source bytes")
if payload.get("buildTransitive/Acme.EdgeRules.props") != bytes_or_empty(src / "buildTransitive/Acme.EdgeRules.props", "source props"):
    fail("props payload does not match source bytes")
if payload.get("README.md") != bytes_or_empty(src / "README.md", "source README"):
    fail("README payload does not match source bytes")
if payload.get("LICENSE.txt") != bytes_or_empty(src / "LICENSE.txt", "source license"):
    fail("license payload does not match source bytes")
if payload.get("Acme.EdgeRules.nuspec") != sidecar_bytes:
    fail("nuspec sidecar does not match packaged nuspec")

try:
    root = ET.fromstring(sidecar_bytes)
    ns = {"n": "http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd"}
    def txt(path):
        elem = root.find(path, ns)
        return None if elem is None else elem.text
    expected_text = {
        "n:metadata/n:id": "Acme.EdgeRules",
        "n:metadata/n:version": "1.4.0",
        "n:metadata/n:authors": "Acme Platform",
        "n:metadata/n:description": "Offline edge routing rule helpers for Acme gateways.",
        "n:metadata/n:license": "LICENSE.txt",
        "n:metadata/n:readme": "README.md",
    }
    for path, value in expected_text.items():
        if txt(path) != value:
            fail(f"nuspec {path} mismatch")
    repo = root.find("n:metadata/n:repository", ns)
    if repo is None or repo.attrib != {"type": "git", "url": "https://git.example.invalid/acme/edge-rules", "commit": "8f3d2ac91b7e"}:
        fail("nuspec repository element mismatch")
    ptype = root.find("n:metadata/n:packageTypes/n:packageType", ns)
    if ptype is None or ptype.attrib.get("name") != "Dependency":
        fail("nuspec package type mismatch")
    group = root.find("n:metadata/n:dependencies/n:group", ns)
    if group is None or group.attrib.get("targetFramework") != "net8.0" or list(group):
        fail("nuspec dependency group mismatch")
except Exception as exc:
    fail(f"nuspec XML invalid: {exc}")

flat_index = read_json(feed / "flatcontainer/acme.edgerules/index.json")
if flat_index != {"versions": ["1.4.0"]}:
    fail("flat-container index mismatch")

service = read_json(feed / "index.json")
if service != {
    "version": "3.0.0",
    "resources": [
        {"@id": "flatcontainer/", "@type": "PackageBaseAddress/3.0.0"},
        {"@id": "registration/", "@type": "RegistrationsBaseUrl/3.6.0"},
    ],
}:
    fail("service index mismatch")

reg = read_json(feed / "registration/acme.edgerules/index.json")
pkg = nupkg.read_bytes() if nupkg.exists() else b""
expected_hash = base64.b64encode(hashlib.sha512(pkg).digest()).decode()
expected_sha256 = hashlib.sha256(pkg).hexdigest()
try:
    page = reg["items"][0]
    item = page["items"][0]
    catalog = item["catalogEntry"]
    if reg.get("@id") != "registration/acme.edgerules/index.json" or reg.get("count") != 1:
        fail("registration root metadata mismatch")
    if page.get("lower") != "1.4.0" or page.get("upper") != "1.4.0" or page.get("count") != 1:
        fail("registration page bounds mismatch")
    if item.get("packageContent") != "flatcontainer/acme.edgerules/1.4.0/acme.edgerules.1.4.0.nupkg":
        fail("registration packageContent mismatch")
    checks = {
        "id": "Acme.EdgeRules",
        "version": "1.4.0",
        "authors": "Acme Platform",
        "description": "Offline edge routing rule helpers for Acme gateways.",
        "packageHash": expected_hash,
        "packageHashAlgorithm": "SHA512",
        "packageSize": len(pkg),
        "published": "2024-05-06T07:08:10Z",
    }
    for key, value in checks.items():
        if catalog.get(key) != value:
            fail(f"catalogEntry {key} mismatch")
    if reg.get("packageSha256") != expected_sha256:
        fail("registration packageSha256 mismatch")
    if catalog.get("repository") != {"type": "git", "url": "https://git.example.invalid/acme/edge-rules", "commit": "8f3d2ac91b7e"}:
        fail("catalog repository mismatch")
    if catalog.get("tags") != ["edge", "rules", "offline"]:
        fail("catalog tags mismatch")
except Exception as exc:
    fail(f"registration shape invalid: {exc}")

if errors:
    print("FAIL: " + errors[0])
    Path("/logs/verifier/reward.txt").write_text("0\n")
    sys.exit(1)

print("PASS: NuGet feed is canonical")
Path("/logs/verifier/reward.txt").write_text("1\n")
PY
