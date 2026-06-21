# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install Python and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Prepare initial filesystem state for the exercise
# Everything lives under /home/user
# ------------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user/webapp/config && \
    mkdir -p /home/user/monitor

# settings.yaml (initial content)
RUN cat > /home/user/webapp/config/settings.yaml <<'YAML'
version: 1.0
debug: false
database:
  host: localhost
  port: 5432
YAML

# service.toml (initial content)
RUN cat > /home/user/monitor/service.toml <<'TOML'
[server]
port = 9000

[logging]
level = "debug"
TOML

# ------------------------------------------------------------------
# Relax permissions so the non-root runtime user can modify files
# ------------------------------------------------------------------
RUN chmod -R a+rwx /home/user

# ------------------------------------------------------------------
# Labels (from %labels)
# ------------------------------------------------------------------
LABEL Author="ChatGPT" \
      Description="Initial state for configuration-update task (YAML & TOML)"

# ------------------------------------------------------------------
# Help (from %help)
# ------------------------------------------------------------------
# This container sets up the starting environment for the configuration
# file editing task. It installs Python/pytest for test execution and
# places the required files under /home/user exactly as described in the
# task specification.