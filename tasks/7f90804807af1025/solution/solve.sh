#!/bin/bash
set -euo pipefail

LAB="${TUF_LAB:-/home/user/tuf_lab}"
REPO="$LAB/repository"
META="$REPO/metadata"
KEYS="$LAB/keys"

python3 - <<'PY'
import base64
import hashlib
import json
import os
import pathlib
import subprocess
import tempfile

lab = pathlib.Path(os.environ.get("TUF_LAB", "/home/user/tuf_lab"))
repo = lab / "repository"
meta = repo / "metadata"
keys = lab / "keys"
meta.mkdir(parents=True, exist_ok=True)

for path in meta.iterdir():
    if path.name not in {"root.json", "targets.json", "snapshot.json", "timestamp.json"}:
        if path.is_file() or path.is_symlink():
            path.unlink()

roles = {
    "root": {
        "key": keys / "root.ed25519.pem",
        "version": 3,
        "expires": "2027-06-25T00:00:00Z",
    },
    "targets": {
        "key": keys / "targets.ed25519.pem",
        "version": 7,
        "expires": "2026-09-01T00:00:00Z",
    },
    "snapshot": {
        "key": keys / "snapshot.ed25519.pem",
        "version": 11,
        "expires": "2026-07-15T00:00:00Z",
    },
    "timestamp": {
        "key": keys / "timestamp.ed25519.pem",
        "version": 19,
        "expires": "2026-06-26T00:00:00Z",
    },
}

def public_der(private_key: pathlib.Path) -> bytes:
    return subprocess.check_output([
        "openssl", "pkey", "-in", str(private_key), "-pubout", "-outform", "DER"
    ])

def key_record(role: str) -> dict:
    der = public_der(roles[role]["key"])
    return {
        "keyid": hashlib.sha256(der).hexdigest(),
        "keytype": "ed25519",
        "scheme": "ed25519",
        "keyval": {"public": base64.b64encode(der).decode("ascii")},
    }

key_records = {role: key_record(role) for role in roles}

def canonical(obj: dict) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")

def sign(role: str, signed: dict) -> str:
    with tempfile.TemporaryDirectory() as tmp_s:
        tmp = pathlib.Path(tmp_s)
        payload = tmp / "signed.json"
        sig = tmp / "sig.bin"
        payload.write_bytes(canonical(signed))
        subprocess.run([
            "openssl", "pkeyutl", "-sign", "-rawin",
            "-inkey", str(roles[role]["key"]),
            "-in", str(payload),
            "-out", str(sig),
        ], check=True)
        return sig.read_bytes().hex()

def write_metadata(role: str, signed: dict) -> bytes:
    envelope = {
        "signatures": [{"keyid": key_records[role]["keyid"], "sig": sign(role, signed)}],
        "signed": signed,
    }
    raw = json.dumps(envelope, separators=(",", ":")).encode("utf-8") + b"\n"
    (meta / f"{role}.json").write_bytes(raw)
    return raw

def file_meta(path: pathlib.Path) -> dict:
    data = path.read_bytes()
    return {"length": len(data), "hashes": {"sha256": hashlib.sha256(data).hexdigest()}}

root_signed = {
    "_type": "root",
    "spec_version": "1.0.31",
    "version": roles["root"]["version"],
    "expires": roles["root"]["expires"],
    "consistent_snapshot": False,
    "keys": {
        key_records["root"]["keyid"]: {k: v for k, v in key_records["root"].items() if k != "keyid"},
        key_records["targets"]["keyid"]: {k: v for k, v in key_records["targets"].items() if k != "keyid"},
        key_records["snapshot"]["keyid"]: {k: v for k, v in key_records["snapshot"].items() if k != "keyid"},
        key_records["timestamp"]["keyid"]: {k: v for k, v in key_records["timestamp"].items() if k != "keyid"},
    },
    "roles": {
        "root": {"keyids": [key_records["root"]["keyid"]], "threshold": 1},
        "targets": {"keyids": [key_records["targets"]["keyid"]], "threshold": 1},
        "snapshot": {"keyids": [key_records["snapshot"]["keyid"]], "threshold": 1},
        "timestamp": {"keyids": [key_records["timestamp"]["keyid"]], "threshold": 1},
    },
}
root_raw = write_metadata("root", root_signed)

targets_signed = {
    "_type": "targets",
    "spec_version": "1.0.31",
    "version": roles["targets"]["version"],
    "expires": roles["targets"]["expires"],
    "targets": {
        "app/config.yaml": file_meta(repo / "targets/app/config.yaml"),
        "bin/edge-tool.sh": file_meta(repo / "targets/bin/edge-tool.sh"),
    },
    "delegations": {},
}
targets_raw = write_metadata("targets", targets_signed)

def metadata_meta(name: str, version: int, raw: bytes) -> dict:
    return {
        "version": version,
        "length": len(raw),
        "hashes": {"sha256": hashlib.sha256(raw).hexdigest()},
    }

snapshot_signed = {
    "_type": "snapshot",
    "spec_version": "1.0.31",
    "version": roles["snapshot"]["version"],
    "expires": roles["snapshot"]["expires"],
    "meta": {
        "root.json": metadata_meta("root.json", roles["root"]["version"], root_raw),
        "targets.json": metadata_meta("targets.json", roles["targets"]["version"], targets_raw),
    },
}
snapshot_raw = write_metadata("snapshot", snapshot_signed)

timestamp_signed = {
    "_type": "timestamp",
    "spec_version": "1.0.31",
    "version": roles["timestamp"]["version"],
    "expires": roles["timestamp"]["expires"],
    "meta": {
        "snapshot.json": metadata_meta("snapshot.json", roles["snapshot"]["version"], snapshot_raw),
    },
}
write_metadata("timestamp", timestamp_signed)
PY

chmod 0644 "$META"/root.json "$META"/targets.json "$META"/snapshot.json "$META"/timestamp.json
