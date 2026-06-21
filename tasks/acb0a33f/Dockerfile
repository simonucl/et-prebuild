# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create non-privileged user `user`
RUN set -eux && \
    if ! id -u user >/dev/null 2>&1; then \
        useradd -m -s /bin/bash user; \
    fi && \
    mkdir -p /home/user && \
    chown -R user:user /home/user

# Seed file: /home/user/sample.env
RUN cat >/home/user/sample.env <<'EOF'
# Sample environment file
EOF

RUN chown user:user /home/user/sample.env && \
    chmod 644 /home/user/sample.env

# Environment setup
ENV PATH=/usr/local/bin:$PATH

RUN chmod 755 /home/user

# Run script
CMD echo "Container for CI/CD workspace setup task. Run your commands inside the shell." && exec /bin/bash "$@"

# Labels
LABEL Author="CI-Task-Builder"
LABEL Description="Apptainer image seeded for platform-engineer workspace task"