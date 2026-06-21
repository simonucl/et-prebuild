FROM ubuntu:22.04

# Labels
LABEL Author="DevSecOpsContainer"
LABEL Description="Sets up initial state for policy-as-code disk-usage assignment"

# Install Python and pytest
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directories
RUN mkdir -p /home/user/policy-code/tests

# policy.yaml
RUN cat <<'EOF' > /home/user/policy-code/policy.yaml
apiVersion: v1
kind: Policy
metadata:
  name: sample-policy
spec:
  description: Sample security policy file.
#
EOF
RUN truncate -s 113 /home/user/policy-code/policy.yaml

# README.md
RUN cat <<'EOF' > /home/user/policy-code/README.md
# Policy Code

This repository contains sample policy code used for disk usage testing.
EOF
RUN truncate -s 88 /home/user/policy-code/README.md

# script.sh
RUN cat <<'EOF' > /home/user/policy-code/script.sh
#!/bin/bash
# Sample enforcement script
echo "Enforcing policy..."
EOF
RUN truncate -s 67 /home/user/policy-code/script.sh && chmod 755 /home/user/policy-code/script.sh

# tests/test1.txt
RUN echo "dummy test file" > /home/user/policy-code/tests/test1.txt && \
    truncate -s 16 /home/user/policy-code/tests/test1.txt

# Permissions
RUN chmod 755 /home/user && \
    chmod 755 /home/user/policy-code && \
    chmod 755 /home/user/policy-code/tests && \
    chmod 644 /home/user/policy-code/*.yaml && \
    chmod 644 /home/user/policy-code/*.md && \
    chmod 644 /home/user/policy-code/tests/*.txt

# Environment
ENV PATH="$PATH:/usr/local/bin"

# Runscript equivalent
CMD echo "Container for Policy-as-Code disk-usage assignment." && \
    echo "Use this image as the execution environment for the grading tasks."