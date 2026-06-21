# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels converted from %labels
LABEL Author="Apptainer Task Preparer"
LABEL Description="Initial state for DevSecOps policy benchmark exercise"

# ------------------------------------------------------------------
# %post section
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create the non-privileged user and its home directory
RUN set -eux && \
    if ! id -u user >/dev/null 2>&1; then \
        echo "user:x:1000:1000:User,,,:/home/user:/bin/bash" >> /etc/passwd && \
        echo "user:x:1000:" >> /etc/group ; \
    fi && \
    mkdir -p /home/user && \
    chown 1000:1000 /home/user

# Create the policy directory and reference policy script
RUN mkdir -p /home/user/policy && \
    cat >/home/user/policy/check_policy.sh <<'EOF'
#!/bin/bash
sleep 0.05
echo "Policy PASSED"
EOF

RUN chmod 755 /home/user/policy && \
    chmod 755 /home/user/policy/check_policy.sh && \
    chown -R 1000:1000 /home/user/policy

# ------------------------------------------------------------------
# %environment section
# ------------------------------------------------------------------
ENV PATH="/home/user/policy:${PATH}"

# ------------------------------------------------------------------
# %help section
# This container seeds the filesystem with:
#   • /home/user/policy/check_policy.sh  – a reference policy script
# Pytest is pre-installed so automated grading can run.
# ------------------------------------------------------------------