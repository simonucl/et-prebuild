#!/bin/bash
set -euo pipefail

base=${PKI_LAB_ROOT:-/home/user/pki-lab}
int="$base/intermediate"
out="$base/out"

rm -rf "$int" "$out"
mkdir -p "$int"/{certs,crl,newcerts,private,csr} "$out"/{certs,crl}
touch "$int/index.txt"
echo 2000 > "$int/serial"
echo 2000 > "$int/crlnumber"

openssl genrsa -out "$int/private/intermediate.key.pem" 3072
chmod 600 "$int/private/intermediate.key.pem"

cat > "$int/openssl.cnf" <<EOF
[ ca ]
default_ca = CA_default

[ CA_default ]
dir               = $int
certs             = \$dir/certs
crl_dir           = \$dir/crl
new_certs_dir     = \$dir/newcerts
database          = \$dir/index.txt
serial            = \$dir/serial
crlnumber         = \$dir/crlnumber
certificate       = \$dir/certs/intermediate.cert.pem
private_key       = \$dir/private/intermediate.key.pem
default_md        = sha256
default_days      = 825
default_crl_days  = 30
preserve          = no
policy            = policy_any
copy_extensions   = none
unique_subject    = no

[ policy_any ]
countryName             = supplied
stateOrProvinceName     = optional
localityName            = optional
organizationName        = supplied
organizationalUnitName  = supplied
commonName              = supplied
emailAddress            = optional

[ req ]
distinguished_name = req_dn
prompt = no

[ req_dn ]
C = US
O = Acme Edge Labs
OU = Issuing
CN = Acme Edge Issuing CA

[ v3_intermediate_ca ]
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints = critical, CA:true, pathlen:0
keyUsage = critical, keyCertSign, cRLSign

[ server_cert ]
basicConstraints = critical, CA:false
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @server_alt_names

[ server_alt_names ]
DNS.1 = edge-api.internal
DNS.2 = edge-api.service.consul
IP.1 = 10.42.0.15

[ client_cert ]
basicConstraints = critical, CA:false
keyUsage = critical, digitalSignature
extendedKeyUsage = clientAuth
subjectAltName = @client_alt_names

[ client_alt_names ]
URI.1 = spiffe://edge.local/agent/old-edge-agent-17

[ crl_ext ]
authorityKeyIdentifier = keyid:always
EOF

openssl req -new -key "$int/private/intermediate.key.pem" \
  -config "$int/openssl.cnf" \
  -out "$int/csr/intermediate.csr.pem"

openssl x509 -req -in "$int/csr/intermediate.csr.pem" \
  -CA "$base/root/certs/root.cert.pem" \
  -CAkey "$base/root/private/root.key.pem" \
  -set_serial 0x1000 -days 1825 -sha256 \
  -extfile "$int/openssl.cnf" -extensions v3_intermediate_ca \
  -out "$int/certs/intermediate.cert.pem"

cp "$int/certs/intermediate.cert.pem" "$out/intermediate.cert.pem"
cat "$out/intermediate.cert.pem" "$base/root/certs/root.cert.pem" > "$out/chain.pem"

openssl ca -batch -config "$int/openssl.cnf" \
  -extensions server_cert -days 397 -notext -md sha256 \
  -in "$base/incoming/edge-api.csr.pem" \
  -out "$out/certs/edge-api.cert.pem"

openssl ca -batch -config "$int/openssl.cnf" \
  -extensions client_cert -days 397 -notext -md sha256 \
  -in "$base/incoming/old-edge-agent.csr.pem" \
  -out "$out/certs/old-edge-agent.cert.pem"

openssl ca -batch -config "$int/openssl.cnf" \
  -revoke "$out/certs/old-edge-agent.cert.pem" \
  -crl_reason keyCompromise

openssl ca -batch -config "$int/openssl.cnf" \
  -gencrl -crlexts crl_ext \
  -out "$out/crl/intermediate.crl.pem"

python3 - <<'PY'
import hashlib
import json
from pathlib import Path

import os

out = Path(os.environ.get("PKI_LAB_ROOT", "/home/user/pki-lab")) / "out"
paths = [
    "intermediate.cert.pem",
    "chain.pem",
    "certs/edge-api.cert.pem",
    "certs/old-edge-agent.cert.pem",
    "crl/intermediate.crl.pem",
]
manifest = {
    "bundle": "edge-pki",
    "issuer": "Acme Edge Issuing CA",
    "server_cert": "certs/edge-api.cert.pem",
    "revoked": ["certs/old-edge-agent.cert.pem"],
    "crl": "crl/intermediate.crl.pem",
    "sha256": {p: hashlib.sha256((out / p).read_bytes()).hexdigest() for p in paths},
}
(out / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n", encoding="utf-8")
PY
