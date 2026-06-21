FROM ubuntu:22.04

# Help / metadata from %labels
LABEL Author="Your Name"
LABEL Description="Container for libalpha mirroring task – provides upstream artefact and required tooling (rsync, pytest)."

# ------------------------------------------------------------------
# Basic OS packages
# ------------------------------------------------------------------
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        rsync \
        python3-pip \
        ca-certificates \
        tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Python tooling (pytest)
# ------------------------------------------------------------------
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Create the required upstream artefact
# ------------------------------------------------------------------
RUN mkdir -p /home/user/remote_repo/libalpha

RUN cat <<'EOF' > /home/user/remote_repo/libalpha/libalpha-1.2.3.tar.gz
This is libalpha binary version 1.2.3
EOF

RUN chmod 755 /home /home/user /home/user/remote_repo /home/user/remote_repo/libalpha && \
    chmod 644 /home/user/remote_repo/libalpha/libalpha-1.2.3.tar.gz

# ------------------------------------------------------------------
# Environment variables from %environment
# ------------------------------------------------------------------
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8