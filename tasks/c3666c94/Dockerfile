# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Container for the configuration-editing exercise.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/project/.github/workflows

RUN cat > /home/user/project/.github/workflows/build.yml <<'EOF'
name: Build Pipeline
on:
  push:
    branches: [ "main" ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run build
        run: echo "Building..."
EOF

RUN cat > /home/user/project/config.toml <<'EOF'
[server]
port = 8080
EOF

RUN chmod -R 777 /home/user

LABEL Author="Demo"