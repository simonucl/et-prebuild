# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install Python tooling and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Create a non-root user `user` (uid 1000 / gid 1000)
# ------------------------------------------------------------------
RUN if ! getent group 1000 >/dev/null; then \
        groupadd -g 1000 user; \
    fi && \
    if ! id -u 1000 >/dev/null 2>&1; then \
        useradd -m -u 1000 -g 1000 -s /bin/bash user; \
    fi

# ------------------------------------------------------------------
# Prepare initial filesystem state for the exercise
# ------------------------------------------------------------------
# Directories
RUN install -d -o 1000 -g 1000 -m 0755 /home/user/original_configs && \
    install -d -o 1000 -g 1000 -m 0755 /home/user/linked_configs

# Configuration files with required content
RUN cat >/home/user/original_configs/config1.conf <<'EOF'
version=1.0
name=PrimaryConfig
EOF

RUN cat >/home/user/original_configs/config2.conf <<'EOF'
version=2.1
name=SecondaryConfig
EOF

# Correct ownership and permissions
RUN chown 1000:1000 \
        /home/user/original_configs/config1.conf \
        /home/user/original_configs/config2.conf && \
    chmod 0644 \
        /home/user/original_configs/config1.conf \
        /home/user/original_configs/config2.conf

# ------------------------------------------------------------------
# Runtime environment setup
# ------------------------------------------------------------------
RUN chmod 755 /home/user

ENV PATH=/home/user/.local/bin:$PATH

# Maintainer="task setup for configuration-management exercise"