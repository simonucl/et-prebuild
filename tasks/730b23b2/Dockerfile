# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Labels (from %labels)
# ------------------------------------------------------------------
LABEL Author="backup-admin-exercise" \
      Description="Initial state for the backup administrator task"

# ------------------------------------------------------------------
# Basic tooling required by the exercise and the test harness
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Prepare initial directory tree under /home/user/projects
# ------------------------------------------------------------------
RUN set -eux && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    mkdir -p /home/user/projects/site1 && \
    mkdir -p /home/user/projects/site2/data && \
    chmod 0755 /home/user/projects && \
    chmod 0755 /home/user/projects/site1 && \
    chmod 0755 /home/user/projects/site2 && \
    chmod 0755 /home/user/projects/site2/data && \
    printf "<html>Site1</html>\n" > /home/user/projects/site1/index.html && \
    printf "theme: minimal\n"      > /home/user/projects/site1/config.yml && \
    printf "# Site2\n"             > /home/user/projects/site2/README.md && \
    printf "Info\n"                > /home/user/projects/site2/data/info.txt && \
    chmod 0644 /home/user/projects/site1/index.html && \
    chmod 0644 /home/user/projects/site1/config.yml && \
    chmod 0644 /home/user/projects/site2/README.md && \
    chmod 0644 /home/user/projects/site2/data/info.txt

# ------------------------------------------------------------------
# Environment variables (from %environment)
# ------------------------------------------------------------------
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Ensure permissions as specified in %environment
RUN chmod 0755 /home/user

# ------------------------------------------------------------------
# Help (from %help)
# Initial state for the backup administrator task
# ------------------------------------------------------------------