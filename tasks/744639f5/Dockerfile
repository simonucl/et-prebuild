# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------
# Install Python, pip, and pytest
# ------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Prepare initial configuration files for the student to refactor
# ------------------------------------------------------------
RUN mkdir -p /home/user/configs

# 1. /home/user/configs/app.yml
RUN cat > /home/user/configs/app.yml <<'YAML'
app_name: SampleApp
debug: true
version: 2.0.3
database:
  host: localhost
  port: 5432
YAML

# 2. /home/user/configs/db.toml
RUN cat > /home/user/configs/db.toml <<'TOML'
[connection]
host = "localhost"
port = 5432
user = "appuser"

[settings]
max_connections = 150
TOML

# Ensure the non-privileged runtime user can read/write the configs
RUN chmod -R a+rwX /home/user

# ------------------------------------------------------------
# Environment settings (from %environment)
# ------------------------------------------------------------
RUN chmod 755 /home/user

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Guarantee that `python` maps to Python 3 if it's absent
RUN if ! command -v python >/dev/null 2>&1; then \
        ln -s /usr/bin/python3 /usr/local/bin/python; \
    fi