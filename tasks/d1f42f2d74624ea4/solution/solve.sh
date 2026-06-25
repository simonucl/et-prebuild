#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import base64
import hashlib
import json
import os
import shutil
import zipfile
from collections import OrderedDict
from pathlib import Path

src = Path("/app/nuget-src")
feed = Path("/app/nuget-feed/v3")
flat = feed / "flatcontainer" / "acme.edgerules"
verdir = flat / "1.4.0"
registration = feed / "registration" / "acme.edgerules"

if feed.exists():
    shutil.rmtree(feed)
verdir.mkdir(parents=True)
registration.mkdir(parents=True)

nuspec = (
    '<?xml version="1.0" encoding="utf-8"?>\n'
    '<package xmlns="http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd">'
    '<metadata>'
    '<id>Acme.EdgeRules</id>'
    '<version>1.4.0</version>'
    '<authors>Acme Platform</authors>'
    '<description>Offline edge routing rule helpers for Acme gateways.</description>'
    '<repository type="git" url="https://git.example.invalid/acme/edge-rules" commit="8f3d2ac91b7e" />'
    '<license type="file">LICENSE.txt</license>'
    '<readme>README.md</readme>'
    '<packageTypes><packageType name="Dependency" /></packageTypes>'
    '<dependencies><group targetFramework="net8.0" /></dependencies>'
    '</metadata>'
    '</package>\n'
).encode()

content_types = (
    '<?xml version="1.0" encoding="utf-8"?>\n'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml" />'
    '<Default Extension="dll" ContentType="application/octet" />'
    '<Default Extension="props" ContentType="application/xml" />'
    '<Default Extension="md" ContentType="text/markdown" />'
    '<Default Extension="txt" ContentType="text/plain" />'
    '<Default Extension="nuspec" ContentType="application/octet" />'
    '</Types>\n'
).encode()

rels = (
    '<?xml version="1.0" encoding="utf-8"?>\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Type="http://schemas.microsoft.com/packaging/2010/07/manifest" Target="/Acme.EdgeRules.nuspec" Id="R1" />'
    '</Relationships>\n'
).encode()

members = [
    ("[Content_Types].xml", content_types),
    ("_rels/.rels", rels),
    ("Acme.EdgeRules.nuspec", nuspec),
    ("lib/net8.0/Acme.EdgeRules.dll", (src / "lib/net8.0/Acme.EdgeRules.dll").read_bytes()),
    ("buildTransitive/Acme.EdgeRules.props", (src / "buildTransitive/Acme.EdgeRules.props").read_bytes()),
    ("README.md", (src / "README.md").read_bytes()),
    ("LICENSE.txt", (src / "LICENSE.txt").read_bytes()),
]

nupkg = verdir / "acme.edgerules.1.4.0.nupkg"
with zipfile.ZipFile(nupkg, "w") as zf:
    for name, data in members:
        info = zipfile.ZipInfo(name, (2024, 5, 6, 7, 8, 10))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        zf.writestr(info, data)

(verdir / "acme.edgerules.nuspec").write_bytes(nuspec)
(flat / "index.json").write_text(json.dumps(OrderedDict([("versions", ["1.4.0"])]), separators=(",", ":")) + "\n")

service = OrderedDict([
    ("version", "3.0.0"),
    ("resources", [
        OrderedDict([("@id", "flatcontainer/"), ("@type", "PackageBaseAddress/3.0.0")]),
        OrderedDict([("@id", "registration/"), ("@type", "RegistrationsBaseUrl/3.6.0")]),
    ]),
])
(feed / "index.json").write_text(json.dumps(service, separators=(",", ":")) + "\n")

pkg = nupkg.read_bytes()
sha512_b64 = base64.b64encode(hashlib.sha512(pkg).digest()).decode()
sha256_hex = hashlib.sha256(pkg).hexdigest()
entry = OrderedDict([
    ("@id", "registration/acme.edgerules/1.4.0.json"),
    ("packageContent", "flatcontainer/acme.edgerules/1.4.0/acme.edgerules.1.4.0.nupkg"),
    ("catalogEntry", OrderedDict([
        ("id", "Acme.EdgeRules"),
        ("version", "1.4.0"),
        ("authors", "Acme Platform"),
        ("description", "Offline edge routing rule helpers for Acme gateways."),
        ("licenseUrl", None),
        ("licenseExpression", None),
        ("listed", True),
        ("packageHash", sha512_b64),
        ("packageHashAlgorithm", "SHA512"),
        ("packageSize", len(pkg)),
        ("published", "2024-05-06T07:08:10Z"),
        ("repository", OrderedDict([
            ("type", "git"),
            ("url", "https://git.example.invalid/acme/edge-rules"),
            ("commit", "8f3d2ac91b7e"),
        ])),
        ("tags", ["edge", "rules", "offline"]),
    ])),
])
reg = OrderedDict([
    ("@id", "registration/acme.edgerules/index.json"),
    ("count", 1),
    ("items", [OrderedDict([
        ("@id", "registration/acme.edgerules/index.json#page/1.4.0/1.4.0"),
        ("lower", "1.4.0"),
        ("upper", "1.4.0"),
        ("count", 1),
        ("items", [entry]),
    ])]),
    ("packageSha256", sha256_hex),
])
(registration / "index.json").write_text(json.dumps(reg, separators=(",", ":")) + "\n")
PY
