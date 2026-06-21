# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Container for the localization-engineering task.
# Pre-populates the required project files and installs Python + pytest.
# Author: localization-setup

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

RUN set -e && \
    mkdir -p /home/user/project/locales && \
    chmod -R 777 /home/user

RUN cat > /home/user/project/locales/en.yaml <<'EOF'
greeting: "Hello"
farewell: "Goodbye"
EOF

RUN cat > /home/user/project/locales/es.yaml <<'EOF'
greeting: "Hola"
farewell: "Adiós"
EOF

RUN cat > /home/user/project/settings.toml <<'EOF'
[build]
version = "1.0.0"
lang_support = ["en", "es"]
EOF

RUN set -e && \
    find /home/user -type f -exec chmod 666 {} \; && \
    find /home/user -type d -exec chmod 777 {} \; && \
    chmod 755 /home/user

ENV LC_ALL=C.UTF-8