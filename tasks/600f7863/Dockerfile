# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Diagnostic-Bundle-Task"
LABEL Description="Environment with reference log data for the diagnostic bundle exercise"

#------------------------------------------------------------------
# 1. Base OS packages
#------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        tar \
        gzip \
        coreutils \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

#------------------------------------------------------------------
# 2. Python tooling for the test-runner
#------------------------------------------------------------------
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

#------------------------------------------------------------------
# 3. Prepare reference data under /home/user/support_data/
#------------------------------------------------------------------
RUN mkdir -p /home/user/support_data/app1/logs && \
    mkdir -p /home/user/support_data/app2/logs

# --- app1 logs ---------------------------------------------------
RUN cat >/home/user/support_data/app1/logs/application.log <<'EOF'
2023-12-25 10:15:00 INFO Application started
2023-12-25 10:15:05 ERROR Failed to connect to database
EOF

RUN cat >/home/user/support_data/app1/logs/error.log <<'EOF'
[2023-12-25 10:15:05] ERROR Database connection failure
EOF

# --- app2 logs ---------------------------------------------------
RUN cat >/home/user/support_data/app2/logs/server.log <<'EOF'
2023-12-25 11:00:00 INFO Server initialized
EOF

RUN cat >/home/user/support_data/app2/logs/access.log <<'EOF'
127.0.0.1 - - [25/Dec/2023:11:00:01 +0000] "GET /health HTTP/1.1" 200 2
EOF

#------------------------------------------------------------------
# 4. Permissions
#------------------------------------------------------------------
RUN find /home/user/support_data -type d -exec chmod 0755 {} + && \
    find /home/user/support_data -type f -exec chmod 0644 {} + && \
    chmod 0777 /home/user

#------------------------------------------------------------------
# Environment settings
#------------------------------------------------------------------
RUN chmod 755 /home/user

ENV PYTHONIOENCODING=UTF-8

# Help:
# Environment with reference log data for the diagnostic bundle exercise