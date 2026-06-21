# syntax=docker/dockerfile:1
FROM ubuntu:22.04

LABEL Author="artifact-filtering-setup"

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        ca-certificates \
        curl && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/build && \
    chmod 755 /home/user /home/user/build

RUN cat > /home/user/build/artifacts.json <<'JSON'
[
  {
    "name": "core-lib",
    "version": "1.2.3",
    "sha256": "abc123def456abc123def456abc123def456abc123def456abc123def456"
  },
  {
    "name": "ui-lib",
    "version": "2.0.1",
    "sha256": "fedcba654321fedcba654321fedcba654321fedcba654321fedcba654321"
  },
  {
    "name": "cli-tool",
    "version": "1.2.0",
    "sha256": "789ghi789ghi789ghi789ghi789ghi789ghi789ghi789ghi789ghi789ghi"
  }
]
JSON

RUN cat > /home/user/build/artifact_schema.json <<'JSON'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Artifact",
  "type": "object",
  "required": ["name", "version", "sha256"],
  "properties": {
    "name":   { "type": "string" },
    "version":{ "type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$" },
    "sha256": { "type": "string", "pattern": "^[a-f0-9]{64}$" }
  }
}
JSON

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked chmod 644 /home/user/build/artifacts.json /home/user/build/artifact_schema.json && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Artifact filtering container. Launching shell...
CMD echo "Artifact filtering container. Launching shell..." && exec /bin/bash "$@"