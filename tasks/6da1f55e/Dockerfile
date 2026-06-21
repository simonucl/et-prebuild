# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author: example
# Description: Environment for k8s-operator version-bump task with pytest installed.

# ---------- Install Python and Pytest ----------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ---------- Create non-root user (uid 1000) ----------
# If the UID already exists we ignore the error.
RUN useradd -m -u 1000 -s /bin/bash user || true

# ---------- Prepare initial repository state ----------
RUN mkdir -p /home/user/k8s-operator

# VERSION file
RUN echo "1.2.3" > /home/user/k8s-operator/VERSION

# CHANGELOG.md file (exact byte content, including trailing blank line)
RUN cat << 'EOF' > /home/user/k8s-operator/CHANGELOG.md
## [1.2.3] - 2023-07-01
### Changed
- Fixed reconciliation loop bug.

EOF

# ---------- Permissions ----------
# Make sure every runtime user can read/write the repo
RUN chmod -R a+rwX /home/user

# ---------- Environment setup ----------
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

RUN chmod 755 /home/user && \
    if [ -x /usr/bin/python3 ] && [ ! -e /usr/bin/python ]; then \
        ln -s /usr/bin/python3 /usr/local/bin/python; \
    fi

LABEL Author="example" \
      Description="Environment for k8s-operator version-bump task with pytest installed."

# This container sets up a tiny sample Git repository for a fictional
# Kubernetes operator under /home/user/k8s-operator.
# It also provides Python 3 and pytest so that the automated grading
# infrastructure can validate the initial filesystem state.