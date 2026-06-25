#!/bin/bash
set -uo pipefail

mkdir -p /logs/verifier

python3 - <<'PY'
import hashlib
import json
import os
import sys
import zipfile
from pathlib import Path

reward = Path("/logs/verifier/reward.txt")
out = Path("/home/user/handoff")
epub = out / "field-runbook-2.0.0.epub"
manifest_path = out / "manifest.json"

def fail(message):
    print(f"FAIL: {message}")
    reward.write_text("0\n")
    sys.exit(0)

def expect_equal(actual, expected, message):
    if actual != expected:
        fail(f"{message}: expected {expected!r}, got {actual!r}")

if not out.is_dir():
    fail("/home/user/handoff is missing")

expected_files = ["field-runbook-2.0.0.epub", "manifest.json"]
actual_files = sorted(p.name for p in out.iterdir())
expect_equal(actual_files, expected_files, "handoff directory entries")

if not epub.is_file():
    fail("missing EPUB")
if not manifest_path.is_file():
    fail("missing manifest.json")

expected_entries = [
    "mimetype",
    "META-INF/container.xml",
    "OEBPS/content.opf",
    "OEBPS/nav.xhtml",
    "OEBPS/chapters/intro.xhtml",
    "OEBPS/chapters/ops.xhtml",
    "OEBPS/styles/book.css",
    "OEBPS/images/logo.svg",
]

expected_payloads = {
    "mimetype": b"application/epub+zip",
    "META-INF/container.xml": b'''<?xml version="1.0" encoding="UTF-8"?>\n<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n  <rootfiles>\n    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>\n  </rootfiles>\n</container>\n''',
    "OEBPS/content.opf": b'''<?xml version="1.0" encoding="UTF-8"?>\n<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="pub-id">\n  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n    <dc:identifier id="pub-id">urn:uuid:3b1e14b9-8b51-43dd-9c4a-7630e0d2b30f</dc:identifier>\n    <dc:title>Field Runbook</dc:title>\n    <dc:language>en</dc:language>\n    <dc:creator>Acme Operations</dc:creator>\n    <meta property="dcterms:modified">2024-01-01T00:00:00Z</meta>\n  </metadata>\n  <manifest>\n    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>\n    <item id="intro" href="chapters/intro.xhtml" media-type="application/xhtml+xml"/>\n    <item id="ops" href="chapters/ops.xhtml" media-type="application/xhtml+xml"/>\n    <item id="css" href="styles/book.css" media-type="text/css"/>\n    <item id="logo" href="images/logo.svg" media-type="image/svg+xml"/>\n  </manifest>\n  <spine>\n    <itemref idref="intro"/>\n    <itemref idref="ops"/>\n  </spine>\n</package>\n''',
    "OEBPS/nav.xhtml": b'''<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">\n<head><title>Field Runbook Navigation</title><link rel="stylesheet" type="text/css" href="styles/book.css"/></head>\n<body>\n<nav epub:type="toc" id="toc">\n<h1>Field Runbook</h1>\n<ol>\n<li><a href="chapters/intro.xhtml">Introduction</a></li>\n<li><a href="chapters/ops.xhtml">Operating Checklist</a></li>\n</ol>\n</nav>\n</body>\n</html>\n''',
    "OEBPS/chapters/intro.xhtml": b'''<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" lang="en">\n<head><title>Introduction</title><link rel="stylesheet" type="text/css" href="../styles/book.css"/></head>\n<body>\n<h1>Introduction</h1>\n<p>This runbook is used by the Acme field team before a maintenance window.</p>\n<ul>\n<li>Verify the relay is reachable.</li>\n<li>Record the ticket number.</li>\n</ul>\n</body>\n</html>\n''',
    "OEBPS/chapters/ops.xhtml": b'''<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" lang="en">\n<head><title>Operating Checklist</title><link rel="stylesheet" type="text/css" href="../styles/book.css"/></head>\n<body>\n<h1>Operating Checklist</h1>\n<p>Follow this checklist in order.</p>\n<ol>\n<li>Put the relay into drain mode.</li>\n<li>Confirm the queue depth is zero.</li>\n<li>Resume traffic and capture the health probe.</li>\n</ol>\n</body>\n</html>\n''',
    "OEBPS/styles/book.css": b'''body { font-family: sans-serif; line-height: 1.45; }\nnav ol { padding-left: 1.5em; }\ncode { font-family: monospace; }\n''',
    "OEBPS/images/logo.svg": b'''<svg xmlns="http://www.w3.org/2000/svg" width="160" height="48" viewBox="0 0 160 48">\n  <rect width="160" height="48" fill="#f5f5f5"/>\n  <text x="16" y="30" font-family="sans-serif" font-size="18">Acme Ops</text>\n</svg>\n''',
}

try:
    with zipfile.ZipFile(epub, "r") as zf:
        infos = zf.infolist()
        expect_equal([info.filename for info in infos], expected_entries, "EPUB member order")
        for index, info in enumerate(infos):
            if info.is_dir():
                fail(f"directory entry is not allowed: {info.filename}")
            expect_equal(info.date_time, (2024, 1, 1, 0, 0, 0), f"{info.filename} timestamp")
            mode = (info.external_attr >> 16) & 0o777
            expect_equal(mode, 0o644, f"{info.filename} permissions")
            if index == 0:
                expect_equal(info.compress_type, zipfile.ZIP_STORED, "mimetype compression")
            else:
                expect_equal(info.compress_type, zipfile.ZIP_DEFLATED, f"{info.filename} compression")
            data = zf.read(info.filename)
            expect_equal(data, expected_payloads[info.filename], f"{info.filename} payload")
except zipfile.BadZipFile:
    fail("EPUB is not a valid ZIP file")

try:
    raw_manifest = manifest_path.read_text()
    manifest = json.loads(raw_manifest)
except Exception as exc:
    fail(f"manifest.json is not valid JSON: {exc}")

digest = hashlib.sha256(epub.read_bytes()).hexdigest()
expected_manifest = {
    "name": "field-runbook",
    "version": "2.0.0",
    "epub": "field-runbook-2.0.0.epub",
    "sha256": digest,
    "entries": expected_entries,
}
expected_raw_manifest = json.dumps(expected_manifest, separators=(",", ":")) + "\n"
expect_equal(raw_manifest, expected_raw_manifest, "manifest minified content/key order")

reward.write_text("1\n")
print("ok")
PY
