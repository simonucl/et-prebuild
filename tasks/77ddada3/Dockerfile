# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from %labels
LABEL Author="devsecops-task-prep" \
      Description="Base image for small DevSecOps port-inventory exercise"

# ----------------------------
# %post: System dependencies
# ----------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ----------------------------
# %post: Python tooling
# ----------------------------
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ----------------------------
# %post: Runtime user setup
# ----------------------------
RUN groupadd -g 1000 user || true && \
    useradd -m -u 1000 -g 1000 user || true

# ----------------------------
# %post: Pre-provisioned files
# ----------------------------
RUN mkdir -p /home/user/devsecops/policy

RUN cat > /home/user/devsecops/policy/inventory.txt <<'EOF'
22:ssh/tcp
53:dns/udp
80:http/tcp
443:https/tcp
8080:http-alt/tcp
EOF

# ----------------------------
# %post: Permissions
# ----------------------------
RUN chmod 0755 /home/user && \
    chmod 0755 /home/user/devsecops && \
    chmod 0755 /home/user/devsecops/policy && \
    chmod 0644 /home/user/devsecops/policy/inventory.txt && \
    chown -R 1000:1000 /home/user

# ----------------------------
# %environment
# ----------------------------
ENV PATH=/usr/local/bin:/usr/bin:/bin

# ----------------------------
# %help
# ----------------------------
# This image provides the initial filesystem state for the
# “network-exposure” policy exercise. Pytest is pre-installed so that the
# automated grading harness can run its tests.

USER user
WORKDIR /home/user