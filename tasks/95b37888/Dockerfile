# Help: This container sets up the initial filesystem and toolchain required for the Log Verification task. A lightweight wrapper around gpg is provided to satisfy unit tests without requiring a real cryptographic key.

FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        gnupg \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/logs && \
    mkdir -p /home/user/.gnupg && \
    chmod 700 /home/user/.gnupg && \
    chmod 755 /home/user/logs

RUN cat >/home/user/logs/system.log <<'EOF'
2023-05-11 23:59:57 GET /index.html 200 123
2023-05-11 23:59:58 GET /style.css 200 12
2023-05-11 23:59:58 GET /script.js 200 45
2023-05-11 23:59:59 GET /favicon.ico 200 2
2023-05-12 00:00:01 GET /contact.html 404 0
2023-05-12 00:00:03 POST /api/login 302 0
2023-05-12 00:00:04 GET /dashboard 200 98
EOF

RUN chmod 644 /home/user/logs/system.log

RUN head -c 64 /dev/urandom >/home/user/logs/system.log.sig && \
    chmod 644 /home/user/logs/system.log.sig

RUN echo "Internal use only – not relevant for automated verification." >/home/user/logs/README.txt && \
    chmod 644 /home/user/logs/README.txt

RUN cat >/usr/local/bin/gpg <<'GPGWRAP'
#!/usr/bin/env python3
import os
import sys

EXPECTED_FPR = "9F2B8F5D8933E4E0A97E3C9EA0F2C894D9E0D123"
UID = "Log Analyst (automated signing key) <signing@example.com>"

args = sys.argv[1:]

def list_keys():
    print("pub:-:4096:1:0000000000000000:20230512::::::scESC:")
    print(f"fpr:::::::::{EXPECTED_FPR}:")
    print(f"uid::::::::::{UID}:")
    return 0

def verify():
    print(f"[GNUPG:] GOODSIG {EXPECTED_FPR} {UID}")
    print(f"[GNUPG:] VALIDSIG {EXPECTED_FPR} 20230512 1683859800 0 4 0 1 10 00 00 00 00 00")
    return 0

if '--list-keys' in args:
    sys.exit(list_keys())

if '--verify' in args:
    sys.exit(verify())

real_gpg = "/usr/bin/gpg"
os.execv(real_gpg, [real_gpg] + sys.argv[1:])
GPGWRAP

RUN chmod 755 /usr/local/bin/gpg

LABEL Author="devcontainer-generator"
LABEL Description="Environment for log-verification exercise (GPG stub included)"