# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------------------
# %post section
# ------------------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the evaluation framework
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------------------
# Prepare initial filesystem state expected by the tests
# ------------------------------------------------------------------------------
# Create /home/user and required sub-directory
RUN mkdir -p /home/user/admin

# Set directory permissions to 0755
RUN chmod 0755 /home/user/admin

# Create the initial user_accounts.txt file with exactly 4 bytes: "test"
RUN printf 'test' > /home/user/admin/user_accounts.txt

# Set file permissions to 0644
RUN chmod 0644 /home/user/admin/user_accounts.txt

# Give ownership to UID 1000 if possible
RUN chown -R 1000:1000 /home/user || true

# ------------------------------------------------------------------------------
# %environment section
# ------------------------------------------------------------------------------
# Ensure correct permissions on home directory
RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV HOME=/home/user