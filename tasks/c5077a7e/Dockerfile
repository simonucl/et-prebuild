# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create initial directory structure and data file
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

RUN cat <<'EOF' > /home/user/user_accounts.txt
john ENABLED
mary DISABLED
peter ENABLED
susan DISABLED
david DISABLED
EOF

RUN chmod 0644 /home/user/user_accounts.txt

# Clean up APT cache
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get clean && rm -rf /var/lib/apt/lists/*

# Environment setup
RUN chmod 755 /home/user
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1

# Run script
CMD ["bash"]