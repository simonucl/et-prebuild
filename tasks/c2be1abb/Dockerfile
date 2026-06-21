# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help / labels from %help and %labels
LABEL Author="task-prep-generator"
LABEL Description="Environment for UTF-16LE -> UTF-8 conversion exercise with pytest pre-checks"

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip locales && \
    pip3 install --no-cache-dir pytest && \
    if ! id -u 1000 >/dev/null 2>&1; then useradd -m -u 1000 -s /bin/bash user; fi && \
    mkdir -p /home/user/scan_outputs

RUN python3 - << 'PY'
import pathlib
content = (
    "Open port: 22/ssh\n"
    "Deprecated protocol: SSLv3 detected\n"
    "Vulnerability: CVE-2023-1234\n"
)
path = pathlib.Path("/home/user/scan_outputs/vuln_scan_utf16le.txt")
path.write_text(content, encoding="utf-16")
PY

RUN chmod 644 /home/user/scan_outputs/vuln_scan_utf16le.txt && \
    chmod 755 /home/user