# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# %post
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create the directory tree expected by the grading tests
RUN mkdir -p /home/user/network/logs && \
    chmod 0777 /home/user /home/user/network /home/user/network/logs

# Create the UTF-16 LE (with BOM) input file exactly as specified
RUN python3 - <<'PY'
import os, codecs

dir_path = "/home/user/network/logs"
file_path = os.path.join(dir_path, "connection_report_utf16le.txt")

lines = [
    "2023-07-21 10:12:05 192.168.1.10 OK\r\n",
    "2023-07-21 10:14:27 192.168.1.11 FAILED\r\n",
    "2023-07-21 10:15:32 192.168.1.12 OK\r\n",
    "2023-07-21 10:17:43 192.168.1.13 FAILED\r\n",
]

with open(file_path, "wb") as fb:
    # Write UTF-16 LE BOM
    fb.write(codecs.BOM_UTF16_LE)
    # Encode each line as UTF-16 LE and write them
    for line in lines:
        fb.write(line.encode("utf-16-le"))

# Permissions: 0644 (rw-r--r--) — accepted by the tests
os.chmod(file_path, 0o644)
PY

# ------------------------------------------------------------------
# %environment
# ------------------------------------------------------------------
RUN chmod 755 /home/user

# ------------------------------------------------------------------
# %labels
# ------------------------------------------------------------------
LABEL Author="Connection-Report-Task Builder" \
      Description="Initial container setup for connection-health report exercise."

# ------------------------------------------------------------------
# %help
# This image sets up the initial state for the connection-health report
# conversion task and includes pytest for automated grading.
# ------------------------------------------------------------------