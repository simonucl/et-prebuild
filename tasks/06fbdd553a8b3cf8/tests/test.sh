#!/bin/bash
set -u

mkdir -p /logs/verifier
reward=0

if python3 - <<'PY'
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path

base = Path(os.environ.get("PKI_LAB_ROOT", "/home/user/pki-lab"))
root_cert = base / "root/certs/root.cert.pem"
root_key = base / "root/private/root.key.pem"
int_dir = base / "intermediate"
out = base / "out"

paths = {
    "intermediate_key": int_dir / "private/intermediate.key.pem",
    "intermediate_cert": out / "intermediate.cert.pem",
    "chain": out / "chain.pem",
    "server": out / "certs/edge-api.cert.pem",
    "client": out / "certs/old-edge-agent.cert.pem",
    "crl": out / "crl/intermediate.crl.pem",
    "manifest": out / "manifest.json",
}

def fail(message: str) -> None:
    print(message)
    raise SystemExit(1)

def run(args, input_text=None) -> str:
    proc = subprocess.run(args, input=input_text, text=True, capture_output=True)
    if proc.returncode != 0:
        fail(f"command failed: {' '.join(map(str, args))}\n{proc.stderr.strip()}")
    return proc.stdout

for label, path in paths.items():
    if not path.is_file():
        fail(f"missing required file: {label} at {path}")

if stat.S_IMODE(paths["intermediate_key"].stat().st_mode) != 0o600:
    fail("intermediate private key mode must be 0600")

key_bits = run(["openssl", "rsa", "-in", str(paths["intermediate_key"]), "-noout", "-text"])
if "Private-Key: (3072 bit, 2 primes)" not in key_bits:
    fail("intermediate private key must be RSA 3072-bit")

root_text = run(["openssl", "x509", "-in", str(root_cert), "-noout", "-subject", "-issuer", "-serial", "-text"])
if "subject=C=US, O=Acme Edge Labs, OU=Trust, CN=Acme Edge Root CA" not in root_text:
    fail("root certificate subject is wrong")
if "issuer=C=US, O=Acme Edge Labs, OU=Trust, CN=Acme Edge Root CA" not in root_text:
    fail("root certificate must be self-issued")
if "serial=0A11CE" not in root_text:
    fail("root certificate serial is wrong")
if "CA:TRUE, pathlen:1" not in root_text or "Certificate Sign, CRL Sign" not in root_text:
    fail("root certificate CA constraints are wrong")
root_pub_from_key = run(["openssl", "pkey", "-in", str(root_key), "-pubout"])
root_pub_from_cert = run(["openssl", "x509", "-in", str(root_cert), "-pubkey", "-noout"])
if root_pub_from_key != root_pub_from_cert:
    fail("root private key does not match root certificate")

run(["openssl", "verify", "-CAfile", str(root_cert), str(paths["intermediate_cert"])])

chain_bytes = paths["chain"].read_bytes()
expected_chain = paths["intermediate_cert"].read_bytes() + root_cert.read_bytes()
if chain_bytes != expected_chain:
    fail("chain.pem must contain intermediate cert followed by root cert exactly")

def cert_text(path: Path) -> str:
    return run(["openssl", "x509", "-in", str(path), "-noout", "-subject", "-issuer", "-serial", "-text", "-purpose"])

int_text = cert_text(paths["intermediate_cert"])
if "subject=C=US, O=Acme Edge Labs, OU=Issuing, CN=Acme Edge Issuing CA" not in int_text:
    fail("intermediate certificate subject is wrong")
if "issuer=C=US, O=Acme Edge Labs, OU=Trust, CN=Acme Edge Root CA" not in int_text:
    fail("intermediate certificate issuer is wrong")
if "serial=1000" not in int_text:
    fail("intermediate certificate serial must be 1000")
if "CA:TRUE, pathlen:0" not in int_text:
    fail("intermediate certificate must be constrained to pathlen 0")
if "X509v3 Basic Constraints: critical" not in int_text or "X509v3 Key Usage: critical" not in int_text:
    fail("intermediate certificate must mark constraints and key usage critical")
if "Certificate Sign, CRL Sign" not in int_text:
    fail("intermediate certificate key usage must allow certificate and CRL signing")

run(["openssl", "verify", "-CAfile", str(paths["chain"]), str(paths["server"])])
server_text = cert_text(paths["server"])
if "subject=C=US, O=Acme Edge Labs, OU=Edge Services, CN=edge-api.internal" not in server_text:
    fail("server certificate subject is wrong")
if "CA:FALSE" not in server_text:
    fail("server certificate must not be a CA")
for token in ["DNS:edge-api.internal", "DNS:edge-api.service.consul", "IP Address:10.42.0.15"]:
    if token not in server_text:
        fail(f"server certificate missing SAN {token}")
if "TLS Web Server Authentication" not in server_text:
    fail("server certificate missing serverAuth EKU")
if "Digital Signature, Key Encipherment" not in server_text:
    fail("server certificate key usage is wrong")
if "SSL server : Yes" not in server_text:
    fail("server certificate is not accepted for SSL server purpose")

run(["openssl", "verify", "-CAfile", str(paths["chain"]), str(paths["client"])])
client_text = cert_text(paths["client"])
if "subject=C=US, O=Acme Edge Labs, OU=Edge Agents, CN=old-edge-agent-17" not in client_text:
    fail("client certificate subject is wrong")
if "CA:FALSE" not in client_text:
    fail("client certificate must not be a CA")
if "URI:spiffe://edge.local/agent/old-edge-agent-17" not in client_text:
    fail("client certificate missing SPIFFE URI SAN")
if "TLS Web Client Authentication" not in client_text:
    fail("client certificate missing clientAuth EKU")
if "Digital Signature" not in client_text or "Key Encipherment" in client_text:
    fail("client certificate key usage is wrong")
if "SSL client : Yes" not in client_text:
    fail("client certificate is not accepted for SSL client purpose")

crl_text = run(["openssl", "crl", "-in", str(paths["crl"]), "-noout", "-issuer", "-text"])
if "Issuer: C=US, O=Acme Edge Labs, OU=Issuing, CN=Acme Edge Issuing CA" not in crl_text:
    fail("CRL issuer is wrong")
client_serial = re.search(r"serial=([0-9A-F]+)", client_text)
if not client_serial or f"Serial Number: {client_serial.group(1)}" not in crl_text:
    fail("CRL does not revoke the old-edge-agent certificate serial")
if "Key Compromise" not in crl_text:
    fail("CRL must record keyCompromise as the revocation reason")

revoked = subprocess.run(
    ["openssl", "verify", "-CAfile", str(paths["chain"]), "-CRLfile", str(paths["crl"]), "-crl_check", str(paths["client"])],
    capture_output=True,
    text=True,
)
if revoked.returncode == 0 or "certificate revoked" not in (revoked.stderr + revoked.stdout):
    fail("client certificate is not rejected as revoked")

server_ok = subprocess.run(
    ["openssl", "verify", "-CAfile", str(paths["chain"]), "-CRLfile", str(paths["crl"]), "-crl_check", str(paths["server"])],
    capture_output=True,
    text=True,
)
if server_ok.returncode != 0:
    fail("server certificate should not be revoked")

raw_manifest = paths["manifest"].read_text(encoding="utf-8")
expected_hash_paths = [
    "intermediate.cert.pem",
    "chain.pem",
    "certs/edge-api.cert.pem",
    "certs/old-edge-agent.cert.pem",
    "crl/intermediate.crl.pem",
]
expected_manifest = {
    "bundle": "edge-pki",
    "issuer": "Acme Edge Issuing CA",
    "server_cert": "certs/edge-api.cert.pem",
    "revoked": ["certs/old-edge-agent.cert.pem"],
    "crl": "crl/intermediate.crl.pem",
    "sha256": {p: hashlib.sha256((out / p).read_bytes()).hexdigest() for p in expected_hash_paths},
}
expected_raw = json.dumps(expected_manifest, separators=(",", ":")) + "\n"
if raw_manifest != expected_raw:
    fail("manifest.json content, key order, minification, hashes, or trailing newline is incorrect")

unexpected = []
for p in out.rglob("*"):
    if p.is_file():
        rel = p.relative_to(out).as_posix()
        if rel not in set(expected_hash_paths + ["manifest.json"]):
            unexpected.append(rel)
if unexpected:
    fail(f"out directory contains unexpected files: {unexpected}")

print("all checks passed")
PY
then
  reward=1
fi

echo "$reward" > /logs/verifier/reward.txt
exit 0
