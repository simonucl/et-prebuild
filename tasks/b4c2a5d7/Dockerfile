# syntax=docker/dockerfile:1
FROM ubuntu:22.04

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip \
        ca-certificates \
        grep coreutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/reports/policy

RUN cat <<'EOF' > /home/user/reports/vuln_report.csv
CVE_ID,SEVERITY,DESCRIPTION,AFFECTED_PACKAGE
CVE-2023-1111,MEDIUM,OpenSSL minor issue,openssl
CVE-2023-2222,CRITICAL,Kernel privilege escalation,linux-kernel
CVE-2023-3333,LOW,Typo in man page,man-db
CVE-2023-4444,CRITICAL,Remote code execution,libssh
CVE-2023-5555,HIGH,Potential DoS in zlib,zlib
EOF

RUN chmod -R 0777 /home/user && chmod 755 /home/user

ENV PYTHONIOENCODING=UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH