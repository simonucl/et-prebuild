# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="example"
LABEL Description="Initial state for symbolic-link audit task"

# --------------------------------------------------------------------
# Install system dependencies and Python tooling
# --------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# --------------------------------------------------------------------
# Create the required directory / file structure
# --------------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user/db_data/bigdata && \
    mkdir -p /home/user/db_data/fastdata && \
    mkdir -p /home/user/db_archives/2023_09_prod && \
    mkdir -p /home/user/db_archives/2023_10_maint && \
    mkdir -p /home/user/configs && \
    echo "-- placeholder SQL config" > /home/user/configs/new_config.sql && \
    rm -f /home/user/current_db_data && \
    rm -f /home/user/db_archives/latest && \
    rm -f /home/user/query_conf_active.sql && \
    rm -f /home/user/symlink_audit.log || true

# --------------------------------------------------------------------
# Ensure write permissions for /home/user
# --------------------------------------------------------------------
RUN chmod -R 777 /home/user

# --------------------------------------------------------------------
# Environment setup
# --------------------------------------------------------------------
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# --------------------------------------------------------------------
# Clean up apt caches to keep image small
# --------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------------------
# Help:
# This container provides the initial filesystem state for the
# “symbolic-link audit” task. The required source directories and files
# are present under /home/user/, while the symbolic links and the audit
# log that the learner must create are intentionally absent.
# Pytest is installed for automated grading.
# --------------------------------------------------------------------

CMD ["/bin/bash"]