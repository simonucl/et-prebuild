FROM ubuntu:22.04

# Help text
# This container provides the initial state for the “legacy tool version audit”
# exercise. The tool is installed at /home/user/legacy/bin/old_tool, and pytest
# is available for test execution.

RUN set -e && \
    echo "=== Installing Python, pip and pytest ===" && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN set -e && \
    echo "=== Creating initial directory structure for the exercise ===" && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    mkdir -p /home/user/legacy/bin && \
    chmod 0755 /home/user/legacy && \
    chmod 0755 /home/user/legacy/bin

RUN cat >/home/user/legacy/bin/old_tool <<'EOF'
#!/usr/bin/env bash
echo "old_tool version v0.9.8-legacy"
EOF

RUN chmod 0755 /home/user/legacy/bin/old_tool

RUN echo "=== Clean-up apt caches ===" && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

LABEL Author="Your_Name"
LABEL Description="Container for legacy tool version audit exercise"