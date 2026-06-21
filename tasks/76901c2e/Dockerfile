# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Basic tooling
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Create an unprivileged user entry that matches the typical host UID/GID
# (UID 1000/GID 1000). This guarantees ownership of the files created
# below for most CI environments.
# ------------------------------------------------------------------
RUN set -e && \
    if ! getent group 1000 >/dev/null; then \
        groupadd -g 1000 usergroup; \
    fi && \
    if ! getent passwd 1000 >/dev/null; then \
        useradd -m -u 1000 -g 1000 -s /bin/bash user; \
    fi

# ------------------------------------------------------------------
# Prepare initial directory structure and files for the task
# ------------------------------------------------------------------
RUN set -e && \
    install -d -m 0755 /home/user/corp/policies && \
    install -d -m 0755 /home/user/corp/projects && \
    install -d -m 0755 /home/user/corp/finance && \
    touch /home/user/corp/policies/company_policy.txt && \
    chmod 600 /home/user/corp/policies/company_policy.txt && \
    install -d -m 0755 /home/user/corp/projects/bob_project && \
    touch /home/user/corp/finance/payroll.xls && \
    chmod 775 /home/user/corp/finance/payroll.xls && \
    chown -R 1000:1000 /home/user || true

# Ensure correct permissions on home directory
RUN chmod 755 /home/user

# ------------------------------------------------------------------
# Environment configuration
# ------------------------------------------------------------------
ENV PYTHONUSERBASE=/home/user/.local

# ------------------------------------------------------------------
# %runscript (informational)
# Container for permission-handling task.
# Run your commands inside an interactive shell or execute your script directly.
# ------------------------------------------------------------------