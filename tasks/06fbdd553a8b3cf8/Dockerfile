FROM ubuntu:24.04

WORKDIR /home/user/pki-lab

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash openssl python3 jq ca-certificates coreutils \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user

RUN set -eux; \
    mkdir -p /home/user/pki-lab/root/certs /home/user/pki-lab/root/private /home/user/pki-lab/incoming /home/user/pki-lab/out; \
    chmod 700 /home/user/pki-lab/root/private; \
    openssl genrsa -out /home/user/pki-lab/root/private/root.key.pem 3072; \
    chmod 600 /home/user/pki-lab/root/private/root.key.pem; \
    openssl req -x509 -new -key /home/user/pki-lab/root/private/root.key.pem \
      -sha256 -days 3650 -set_serial 0xA11CE \
      -subj "/C=US/O=Acme Edge Labs/OU=Trust/CN=Acme Edge Root CA" \
      -addext "basicConstraints=critical,CA:TRUE,pathlen:1" \
      -addext "keyUsage=critical,keyCertSign,cRLSign" \
      -addext "subjectKeyIdentifier=hash" \
      -out /home/user/pki-lab/root/certs/root.cert.pem; \
    openssl genrsa -out /home/user/pki-lab/incoming/edge-api.key.pem 2048; \
    openssl req -new -key /home/user/pki-lab/incoming/edge-api.key.pem \
      -subj "/C=US/O=Acme Edge Labs/OU=Edge Services/CN=edge-api.internal" \
      -out /home/user/pki-lab/incoming/edge-api.csr.pem; \
    openssl genrsa -out /home/user/pki-lab/incoming/old-edge-agent.key.pem 2048; \
    openssl req -new -key /home/user/pki-lab/incoming/old-edge-agent.key.pem \
      -subj "/C=US/O=Acme Edge Labs/OU=Edge Agents/CN=old-edge-agent-17" \
      -out /home/user/pki-lab/incoming/old-edge-agent.csr.pem; \
    chown -R user:user /home/user/pki-lab

USER user
WORKDIR /home/user/pki-lab
