#!/bin/bash
mkdir -p /logs/verifier

python3 - <<'PY'
import base64
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile

lab = pathlib.Path(os.environ.get("TUF_LAB", "/home/user/tuf_lab"))
repo = lab / "repository"
meta = repo / "metadata"
keys = lab / "keys"

def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    raise SystemExit(1)

expected_files = ["root.json", "snapshot.json", "targets.json", "timestamp.json"]
if not meta.is_dir():
    fail("metadata directory is missing")
actual_files = sorted(p.name for p in meta.iterdir() if p.is_file() or p.is_symlink())
if actual_files != expected_files:
    fail(f"metadata directory contains {actual_files}, expected {expected_files}")

roles = {
    "root": ("root.ed25519.pem", 3, "2027-06-25T00:00:00Z"),
    "targets": ("targets.ed25519.pem", 7, "2026-09-01T00:00:00Z"),
    "snapshot": ("snapshot.ed25519.pem", 11, "2026-07-15T00:00:00Z"),
    "timestamp": ("timestamp.ed25519.pem", 19, "2026-06-26T00:00:00Z"),
}

def public_der(role: str) -> bytes:
    key = keys / roles[role][0]
    if not key.is_file():
        fail(f"missing private key for {role}")
    return subprocess.check_output([
        "openssl", "pkey", "-in", str(key), "-pubout", "-outform", "DER"
    ])

def key_record(role: str) -> dict:
    der = public_der(role)
    return {
        "keyid": hashlib.sha256(der).hexdigest(),
        "keytype": "ed25519",
        "scheme": "ed25519",
        "keyval": {"public": base64.b64encode(der).decode("ascii")},
    }

key_records = {role: key_record(role) for role in roles}

def load_envelope(role: str) -> tuple[bytes, dict]:
    path = meta / f"{role}.json"
    raw = path.read_bytes()
    if not raw.endswith(b"\n") or raw.count(b"\n") != 1:
        fail(f"{role}.json must have exactly one trailing newline")
    try:
        obj = json.loads(raw)
    except Exception as exc:
        fail(f"{role}.json is not valid JSON: {exc}")
    if list(obj.keys()) != ["signatures", "signed"]:
        fail(f"{role}.json top-level key order is wrong")
    if json.dumps(obj, separators=(",", ":")).encode("utf-8") + b"\n" != raw:
        fail(f"{role}.json is not minified JSON")
    return raw, obj

def canonical(obj: dict) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")

def verify_signature(role: str, signed: dict, signature_hex: str) -> None:
    try:
        signature = bytes.fromhex(signature_hex)
    except ValueError:
        fail(f"{role}.json signature is not lowercase hex")
    if signature_hex != signature_hex.lower() or len(signature) != 64:
        fail(f"{role}.json signature has wrong format or length")
    with tempfile.TemporaryDirectory() as tmp_s:
        tmp = pathlib.Path(tmp_s)
        pub = tmp / "key.pub.der"
        payload = tmp / "signed.json"
        sig = tmp / "sig.bin"
        pub.write_bytes(public_der(role))
        payload.write_bytes(canonical(signed))
        sig.write_bytes(signature)
        res = subprocess.run([
            "openssl", "pkeyutl", "-verify", "-rawin", "-pubin",
            "-inkey", str(pub), "-keyform", "DER",
            "-sigfile", str(sig), "-in", str(payload),
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            fail(f"{role}.json signature does not verify")

raw = {}
env = {}
for role in ("root", "targets", "snapshot", "timestamp"):
    raw[role], env[role] = load_envelope(role)
    signatures = env[role]["signatures"]
    if not isinstance(signatures, list) or len(signatures) != 1:
        fail(f"{role}.json must contain exactly one signature")
    sig = signatures[0]
    if list(sig.keys()) != ["keyid", "sig"]:
        fail(f"{role}.json signature object key order is wrong")
    if sig["keyid"] != key_records[role]["keyid"]:
        fail(f"{role}.json is signed by the wrong keyid")
    verify_signature(role, env[role]["signed"], sig["sig"])

root = env["root"]["signed"]
if list(root.keys()) != ["_type", "spec_version", "version", "expires", "consistent_snapshot", "keys", "roles"]:
    fail("root.json signed object key order is wrong")
if root["_type"] != "root" or root["spec_version"] != "1.0.31" or root["version"] != 3 or root["expires"] != roles["root"][2]:
    fail("root.json identity/version/expiry is wrong")
if root["consistent_snapshot"] is not False:
    fail("root.json consistent_snapshot must be false")
expected_keys = {rec["keyid"]: {k: v for k, v in rec.items() if k != "keyid"} for rec in key_records.values()}
if root["keys"] != expected_keys:
    fail("root.json keys do not match the staged Ed25519 public keys")
expected_roles = {
    role: {"keyids": [key_records[role]["keyid"]], "threshold": 1}
    for role in ("root", "targets", "snapshot", "timestamp")
}
if root["roles"] != expected_roles:
    fail("root.json roles are incorrect")

def target_meta(rel: str) -> dict:
    data = (repo / "targets" / rel).read_bytes()
    return {"length": len(data), "hashes": {"sha256": hashlib.sha256(data).hexdigest()}}

targets = env["targets"]["signed"]
if list(targets.keys()) != ["_type", "spec_version", "version", "expires", "targets", "delegations"]:
    fail("targets.json signed object key order is wrong")
if targets["_type"] != "targets" or targets["version"] != 7 or targets["expires"] != roles["targets"][2]:
    fail("targets.json identity/version/expiry is wrong")
expected_targets = {
    "app/config.yaml": target_meta("app/config.yaml"),
    "bin/edge-tool.sh": target_meta("bin/edge-tool.sh"),
}
if targets["targets"] != expected_targets or targets["delegations"] != {}:
    fail("targets.json target metadata is incorrect")

def meta_record(role: str) -> dict:
    return {
        "version": roles[role][1],
        "length": len(raw[role]),
        "hashes": {"sha256": hashlib.sha256(raw[role]).hexdigest()},
    }

snapshot = env["snapshot"]["signed"]
if list(snapshot.keys()) != ["_type", "spec_version", "version", "expires", "meta"]:
    fail("snapshot.json signed object key order is wrong")
if snapshot["_type"] != "snapshot" or snapshot["version"] != 11 or snapshot["expires"] != roles["snapshot"][2]:
    fail("snapshot.json identity/version/expiry is wrong")
if snapshot["meta"] != {"root.json": meta_record("root"), "targets.json": meta_record("targets")}:
    fail("snapshot.json metadata hashes, lengths, or versions are wrong")

timestamp = env["timestamp"]["signed"]
if list(timestamp.keys()) != ["_type", "spec_version", "version", "expires", "meta"]:
    fail("timestamp.json signed object key order is wrong")
if timestamp["_type"] != "timestamp" or timestamp["version"] != 19 or timestamp["expires"] != roles["timestamp"][2]:
    fail("timestamp.json identity/version/expiry is wrong")
if timestamp["meta"] != {"snapshot.json": meta_record("snapshot")}:
    fail("timestamp.json snapshot metadata is wrong")

for rel, expected_mode in (("app/config.yaml", 0o644), ("bin/edge-tool.sh", 0o755)):
    path = repo / "targets" / rel
    if not path.is_file():
        fail(f"target {rel} is missing")
    if path.stat().st_mode & 0o777 != expected_mode:
        fail(f"target {rel} mode was modified")

print("offline TUF metadata set validated")
PY

if [ $? -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
