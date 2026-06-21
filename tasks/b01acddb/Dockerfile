# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help:
# This container prepares the filesystem and dependencies needed for the
# “API-gateway smoke-tests” exercise.

LABEL Author="ChatGPT – Apptainer setup"
LABEL Description="Initial state for API-gateway smoke-tests task"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/api-gateway/test_results

RUN cat >/home/user/api-gateway/config.yaml <<'YAML_EOF'
api:
  base_url: "https://dev.example.com/v1"
  timeout: 30
logging:
  level: "info"
YAML_EOF

RUN cat >/home/user/api-gateway/config.toml <<'TOML_EOF'
[api]
base_url = "https://dev.example.com/v1"
timeout   = 30

[logging]
level = "info"
TOML_EOF

RUN chmod -R 0777 /home/user/api-gateway

RUN chmod 755 /home/user

ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"