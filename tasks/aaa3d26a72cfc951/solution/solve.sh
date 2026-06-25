#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import hashlib
import json
import shutil
import zipfile
import os
from pathlib import Path

root = Path(os.environ.get("TASK_ROOT") or "/")
lab = root / "home/user/vsix_lab"
src = lab / "src" / "extension"
dist = lab / "dist"
dist.mkdir(parents=True, exist_ok=True)
for child in list(dist.iterdir()):
    if child.is_dir():
        shutil.rmtree(child)
    else:
        child.unlink()

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

members = [
    ("[Content_Types].xml", content_types),
    ("extension.vsixmanifest", vsixmanifest),
    ("extension/package.json", (json.dumps(package, separators=(",", ":")) + "\n").encode()),
    ("extension/README.md", (src / "README.md").read_bytes()),
    ("extension/LICENSE", (src / "LICENSE").read_bytes()),
    ("extension/syntaxes/acme-log.tmLanguage.json", (src / "syntaxes/acme-log.tmLanguage.json").read_bytes()),
    ("extension/snippets/acme-log.json", (src / "snippets/acme-log.json").read_bytes()),
]

zip_path = dist / "acme-log-tools-0.9.1.vsix"
with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for name, data in members:
        info = zipfile.ZipInfo(name, date_time=(2026, 6, 25, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        zf.writestr(info, data)

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

manifest = {
    "package": "acme-log-tools",
    "version": "0.9.1",
    "vsix": "acme-log-tools-0.9.1.vsix",
    "members": [
        {"path": name, "bytes": len(data), "sha256": sha(data)}
        for name, data in members
    ],
    "vsix_sha256": sha(zip_path.read_bytes()),
}
(dist / "vsix-manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n")

vsix_sha = sha(zip_path.read_bytes())
manifest_sha = sha((dist / "vsix-manifest.json").read_bytes())
(dist / "SHA256SUMS").write_text(
    f"{vsix_sha}  acme-log-tools-0.9.1.vsix\n"
    f"{manifest_sha}  vsix-manifest.json\n"
)
PY
