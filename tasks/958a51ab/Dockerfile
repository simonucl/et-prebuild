# Converted from Apptainer definition file
FROM ubuntu:22.04

# Basic tooling
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Create directory tree
RUN mkdir -p /home/user/support/input

# Create legacy ISO‑8859‑1 file
RUN python3 - <<'PY'
import pathlib

legacy_bytes = bytes.fromhex(
    "43 61 66 E9 20 4D FC 6E 73 74 65 72 20 2D 20 "
    "72 E9 75 6E 69 6F 6E 20 E0 20 31 34 68 2E 0A"
)
path = pathlib.Path("/home/user/support/input/legacy_notes.txt")
path.write_bytes(legacy_bytes)
PY

# Permissions
RUN chmod 0755 /home/user && \
    chmod -R 0755 /home/user/support && \
    chmod 0644 /home/user/support/input/legacy_notes.txt && \
    chmod 0777 /home/user/support

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONIOENCODING=utf-8