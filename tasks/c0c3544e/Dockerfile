# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help / labels from definition file
LABEL Author="incident_setup_bot"
LABEL Description="Container prepared for the incident-analysis task with initial INI configuration files and pytest installed."

# Environment variables
ENV LC_ALL=C
ENV LANG=C

# Post section
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/incident_configs

RUN cat <<'EOF' > /home/user/incident_configs/service1.ini
[network]
port = 8080
host = 0.0.0.0

[auth]
method = token

[performance]
debug_mode = false
EOF

RUN cat <<'EOF' > /home/user/incident_configs/service2.ini
[network]
port = 65535
host = 192.168.1.50

[auth]
method = none

[performance]
debug_mode = true
EOF

RUN cat <<'EOF' > /home/user/incident_configs/service3.ini
[network]
port = 443
host = 10.0.0.1

[auth]
method = oauth

[performance]
debug_mode = false
EOF

RUN chmod -R a+rX /home/user && chmod 755 /home/user