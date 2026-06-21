# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python and Pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Prepare home and localization directory
RUN mkdir -p /home/user/localization && \
    chmod 0777 /home/user/localization

# Create build log with localization messages
RUN cat > /home/user/localization/build.log <<'EOF'
2023-10-01 12:01:22 INFO  [i18n] Loaded locale en_US
2023-10-01 12:01:23 WARN  [i18n] Missing key 'WELCOME_MESSAGE' in locale es_ES
2023-10-01 12:01:24 INFO  [core] Starting renderer
2023-10-01 12:01:25 WARN  [i18n] Missing key 'GOODBYE_MESSAGE' in locale fr_FR
2023-10-01 12:01:26 ERROR [db] Connection refused
2023-10-01 12:01:27 WARN  [i18n] Missing key 'LOGIN_BUTTON' in locale es_ES
EOF

RUN chmod 0644 /home/user/localization/build.log

# Environment setup
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8

LABEL Author="localizer" \
      Description="Environment for the Missing Translation extraction task"