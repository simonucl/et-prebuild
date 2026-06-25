#!/bin/bash
set +e
mkdir -p /logs/verifier

python3 - <<'PY'
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path("/home/user/release_src/gateway-agent-2.7.0")
OUT = Path("/home/user/handoff")
ARCHIVE = OUT / "gateway-agent-2.7.0.tar.gz"
MANIFEST = OUT / "manifest.json"

SOURCE_BYTES = {
    "LICENSE": b"Copyright 2024 Acme Edge Systems\nSPDX-License-Identifier: Apache-2.0\n",
    "README.md": b"Gateway Agent 2.7.0\n===================\n\nOffline field gateway supervisor.\n",
    "bin/gateway-agent": b"#!/usr/bin/env bash\nset -euo pipefail\nprintf \"gateway-agent 2.7.0\\n\"\n",
    "docs/runbook.md": b"# Field Runbook\n\n1. Verify the service is active.\n2. Confirm the local spool is draining.\n",
    "etc/gateway-agent/config.yaml": b"listen: \"127.0.0.1:9443\"\nspool_dir: \"/var/lib/gateway-agent/spool\"\nretry_seconds: 15\n",
    "lib/systemd/system/gateway-agent.service": b"[Unit]\nDescription=Gateway Agent\nAfter=network-online.target\n\n[Service]\nExecStart=/usr/local/bin/gateway-agent --config /etc/gateway-agent/config.yaml\nRestart=on-failure\n\n[Install]\nWantedBy=multi-user.target\n",
}

REGULAR_MODES = {
    "LICENSE": "0644",
    "README.md": "0644",
    "bin/gateway-agent": "0755",
    "docs/runbook.md": "0644",
    "etc/gateway-agent/config.yaml": "0644",
    "lib/systemd/system/gateway-agent.service": "0644",
}


def fail(message):
    print(message)
    sys.exit(1)


if not SRC.is_dir():
    fail("source tree is missing")

for rel, expected in SOURCE_BYTES.items():
    path = SRC / rel
    if not path.is_file():
        fail(f"source file missing: {rel}")
    if path.read_bytes() != expected:
        fail(f"source file was modified: {rel}")

if not (SRC / "docs/current").is_symlink() or os.readlink(SRC / "docs/current") != "runbook.md":
    fail("source symlink docs/current was modified")

if not OUT.is_dir():
    fail("handoff directory is missing")

entries = sorted(p.name for p in OUT.iterdir())
if entries != ["gateway-agent-2.7.0.tar.gz", "manifest.json"]:
    fail(f"handoff directory contains unexpected entries: {entries}")

if not ARCHIVE.is_file() or not MANIFEST.is_file():
    fail("required handoff files are missing")

with tempfile.TemporaryDirectory() as td:
    tmp = Path(td)
    stage = tmp / "stage" / "gateway-agent-2.7.0"
    for rel, data in SOURCE_BYTES.items():
        dest = stage / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    os.symlink("runbook.md", stage / "docs/current")
    for d in sorted([p for p in stage.rglob("*") if p.is_dir()] + [stage]):
        d.chmod(0o755)
    for rel, mode in REGULAR_MODES.items():
        (stage / rel).chmod(int(mode, 8))
    expected_archive = tmp / "expected.tar.gz"
    cmd = (
        "LC_ALL=C tar --sort=name "
        "--mtime='2024-02-03 04:05:06 UTC' "
        "--owner=0 --group=0 --numeric-owner "
        "--format=gnu "
        "-cf - gateway-agent-2.7.0 | gzip -9 -n > "
        + str(expected_archive)
    )
    subprocess.run(["bash", "-c", cmd], cwd=tmp / "stage", check=True)
    expected_bytes = expected_archive.read_bytes()

actual_bytes = ARCHIVE.read_bytes()
if actual_bytes != expected_bytes:
    fail("archive bytes do not match the required deterministic tar.gz")

if actual_bytes[:10] != b"\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\x03":
    fail("gzip header is not level-9 gzip with no stored filename or timestamp")

archive_sha = hashlib.sha256(actual_bytes).hexdigest()
contents = []
for rel in sorted(REGULAR_MODES):
    contents.append({
        "path": rel,
        "type": "file",
        "mode": REGULAR_MODES[rel],
        "sha256": hashlib.sha256(SOURCE_BYTES[rel]).hexdigest(),
    })
contents.append({"path": "docs/current", "type": "symlink", "target": "runbook.md"})
contents.sort(key=lambda item: item["path"])
expected_manifest = {
    "name": "gateway-agent",
    "version": "2.7.0",
    "archive": "gateway-agent-2.7.0.tar.gz",
    "archive_sha256": archive_sha,
    "contents": contents,
}
expected_manifest_bytes = (json.dumps(expected_manifest, separators=(",", ":")) + "\n").encode()
if MANIFEST.read_bytes() != expected_manifest_bytes:
    fail("manifest content, key order, minification, digest, or trailing newline is incorrect")

print("ok")
PY
rc=$?

if [ "$rc" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi

exit "$rc"
