#!/bin/bash
set -u
mkdir -p /logs/verifier

python3 - <<'PY'
import gzip
import hashlib
import io
import json
import os
import sys
import tarfile
from pathlib import Path

reward = Path("/logs/verifier/reward.txt")

def fail(msg):
    print(f"FAIL: {msg}")
    reward.write_text("0\n")
    sys.exit(1)

def sha256(data):
    return hashlib.sha256(data).hexdigest()

src = Path("/app/collection-src/acme/edge_ops")
out = Path("/app/galaxy")
artifact_rel = Path("artifacts/acme-edge_ops-1.2.3.tar.gz")
artifact = out / artifact_rel
payload_paths = [
    "README.md",
    "LICENSE",
    "docs/usage.md",
    "plugins/module_utils/client.py",
    "plugins/modules/edge_status.py",
    "roles/edge_agent/tasks/main.yml",
]
expected_source = {
    "galaxy.yml": b"namespace: acme\nname: edge_ops\nversion: 1.2.3\nreadme: README.md\nauthors:\n  - Acme Platform <platform@acme.invalid>\ndescription: Offline automation helpers for Acme edge gateways.\nlicense_file: LICENSE\ntags:\n  - edge\n  - offline\n  - automation\ndependencies: {}\nrepository: https://git.example.invalid/acme/edge-ops\ndocumentation: https://docs.example.invalid/acme/edge-ops\nhomepage: https://example.invalid/acme/edge-ops\nissues: https://git.example.invalid/acme/edge-ops/issues\n",
    "README.md": b"# Acme Edge Ops\n\nOffline Ansible collection for edge gateway diagnostics.\n",
    "LICENSE": b"Apache License\nVersion 2.0, January 2004\nhttps://www.apache.org/licenses/\n",
    "docs/usage.md": b"# Usage\n\nRun acme.edge_ops.edge_status to collect local edge health facts.\n",
    "plugins/module_utils/client.py": b"from __future__ import annotations\n\ndef normalize_status(payload):\n    return {\n        \"node\": payload.get(\"node\", \"unknown\"),\n        \"healthy\": bool(payload.get(\"healthy\")),\n        \"services\": sorted(payload.get(\"services\", [])),\n    }\n",
    "plugins/modules/edge_status.py": b"#!/usr/bin/python\nfrom __future__ import annotations\n\nfrom ansible.module_utils.basic import AnsibleModule\nfrom ansible_collections.acme.edge_ops.plugins.module_utils.client import normalize_status\n\ndef main():\n    module = AnsibleModule(argument_spec={\"node\": {\"type\": \"str\", \"required\": True}})\n    result = normalize_status({\"node\": module.params[\"node\"], \"healthy\": True, \"services\": [\"agent\", \"proxy\"]})\n    module.exit_json(changed=False, edge_status=result)\n\nif __name__ == \"__main__\":\n    main()\n",
    "roles/edge_agent/tasks/main.yml": b"---\n- name: ensure edge agent directory exists\n  ansible.builtin.file:\n    path: /var/lib/acme-edge\n    state: directory\n    mode: \"0755\"\n",
    "tests/fixture.tmp": b"scratch data that must not be packaged\n",
}

for rel, data in expected_source.items():
    path = src / rel
    if not path.is_file() or path.read_bytes() != data:
        fail(f"source file was modified or missing: {rel}")

actual_files = sorted(str(p.relative_to(out)) for p in out.rglob("*") if p.is_file())
expected_files = sorted([str(artifact_rel), "index.json", "SHA256SUMS"])
if actual_files != expected_files:
    fail(f"handoff file set is wrong: {actual_files}")

if not artifact.is_file():
    fail("artifact is missing")

gz_bytes = artifact.read_bytes()
if len(gz_bytes) < 10 or gz_bytes[:2] != b"\x1f\x8b":
    fail("artifact is not a gzip stream")
if int.from_bytes(gz_bytes[4:8], "little") != 0:
    fail("gzip mtime is not zero")
if gz_bytes[3] & 0x08:
    fail("gzip stream stores an original filename")
if gz_bytes[8] != 2:
    fail("gzip stream does not advertise maximum compression")

files_entries = []
for name in payload_paths:
    data = expected_source[name]
    files_entries.append({
        "name": name,
        "ftype": "file",
        "chksum_type": "sha256",
        "chksum_sha256": sha256(data),
        "size": len(data),
    })
files_json = json.dumps({"files": files_entries, "format": 1}, separators=(",", ":")).encode() + b"\n"
manifest = {
    "collection_info": {
        "namespace": "acme",
        "name": "edge_ops",
        "version": "1.2.3",
        "authors": ["Acme Platform <platform@acme.invalid>"],
        "readme": "README.md",
        "tags": ["edge", "offline", "automation"],
        "description": "Offline automation helpers for Acme edge gateways.",
        "license": [],
        "license_file": "LICENSE",
        "dependencies": {},
        "repository": "https://git.example.invalid/acme/edge-ops",
        "documentation": "https://docs.example.invalid/acme/edge-ops",
        "homepage": "https://example.invalid/acme/edge-ops",
        "issues": "https://git.example.invalid/acme/edge-ops/issues",
    },
    "file_manifest_file": {
        "name": "FILES.json",
        "ftype": "file",
        "chksum_type": "sha256",
        "chksum_sha256": sha256(files_json),
        "format": 1,
    },
    "format": 1,
}
manifest_json = json.dumps(manifest, separators=(",", ":")).encode() + b"\n"
expected_members = [
    ("MANIFEST.json", manifest_json),
    ("FILES.json", files_json),
    *[(name, expected_source[name]) for name in payload_paths],
]

try:
    tar_payload = gzip.decompress(gz_bytes)
except Exception as exc:
    fail(f"cannot decompress artifact: {exc}")

try:
    with tarfile.open(fileobj=io.BytesIO(tar_payload), mode="r:") as tf:
        members = tf.getmembers()
        names = [m.name for m in members]
        if names != [name for name, _ in expected_members]:
            fail(f"tar member order is wrong: {names}")
        for member, (name, data) in zip(members, expected_members):
            if member.isdir():
                fail(f"unexpected directory entry: {member.name}")
            if not member.isfile():
                fail(f"non-regular tar member: {member.name}")
            if member.mode != 0o644 or member.uid != 0 or member.gid != 0 or member.uname != "" or member.gname != "":
                fail(f"tar metadata is not normalized for {member.name}")
            if member.mtime != 1717200000:
                fail(f"tar mtime is wrong for {member.name}")
            extracted = tf.extractfile(member).read()
            if extracted != data:
                fail(f"tar member content is wrong for {member.name}")
except Exception as exc:
    fail(f"cannot read tar archive: {exc}")

expected_index = {
    "format": 1,
    "namespace": "acme",
    "name": "edge_ops",
    "version": "1.2.3",
    "artifact": str(artifact_rel),
    "sha256": sha256(gz_bytes),
    "size_bytes": len(gz_bytes),
    "manifest_sha256": sha256(manifest_json),
    "files_sha256": sha256(files_json),
}
expected_index_bytes = json.dumps(expected_index, separators=(",", ":")).encode() + b"\n"
if (out / "index.json").read_bytes() != expected_index_bytes:
    fail("index.json content, key order, digests, size, or newline is incorrect")

expected_sums = f"{sha256(gz_bytes)}  {artifact_rel}\n".encode()
if (out / "SHA256SUMS").read_bytes() != expected_sums:
    fail("SHA256SUMS content is incorrect")

reward.write_text("1\n")
print("PASS")
PY

if [ $? -ne 0 ]; then
  exit 1
fi
