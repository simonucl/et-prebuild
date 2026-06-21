# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Basic tooling
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        --no-install-recommends && \
    pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Ensure a non-root “user” account with UID/GID 1000 is present
# ------------------------------------------------------------------
RUN set -e && \
    if ! getent group 1000 >/dev/null 2>&1; then \
        groupadd -g 1000 user || true; \
    fi && \
    if ! id -u 1000 >/dev/null 2>&1; then \
        useradd -m -u 1000 -g 1000 user || true; \
    fi

# ------------------------------------------------------------------
# Prepare initial data set under /home/user/data/
# ------------------------------------------------------------------
RUN set -e && \
    install -d -m 700 /home/user/data/raw && \
    install -d -m 700 /home/user/data/reports && \
    chmod 700 /home/user/data && \
    printf "alpha\n"          > /home/user/data/raw/file_a.txt && \
    printf "beta\n"           > /home/user/data/raw/file_b.txt && \
    printf "summary report\n" > /home/user/data/reports/summary.txt && \
    chmod 600 /home/user/data/raw/file_a.txt && \
    chmod 600 /home/user/data/raw/file_b.txt && \
    chmod 600 /home/user/data/reports/summary.txt && \
    chown -R 1000:1000 /home/user

# ------------------------------------------------------------------
# Runtime environment setup (from %environment)
# ------------------------------------------------------------------
RUN chmod 755 /home/user
ENV PATH="/home/user/.local/bin:${PATH}"

# ------------------------------------------------------------------
# Clean up
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get clean && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Default runscript behavior
# ------------------------------------------------------------------
CMD ["bash"]