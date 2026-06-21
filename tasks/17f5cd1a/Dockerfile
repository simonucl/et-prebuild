FROM ubuntu:22.04

RUN set -e && \
    echo "Updating package lists and installing Python tooling..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating workspace directory structure and sample log files..." && \
    mkdir -p /home/user && \
    chmod 0755 /home/user

ENV WORKSPACE=/home/user/api_tests

RUN mkdir -p "${WORKSPACE}" && \
    chmod 0777 "${WORKSPACE}" && \
    mkdir -p "${WORKSPACE}/logs/serviceA" && \
    mkdir -p "${WORKSPACE}/logs/serviceB" && \
    mkdir -p "${WORKSPACE}/logs/serviceC/archive"

RUN cat > "${WORKSPACE}/logs/serviceA/2024-06-08.log" <<'EOF'
OK: ping 200
FAIL: /users endpoint returned 500
OK: /orders endpoint returned 201
EOF

RUN cat > "${WORKSPACE}/logs/serviceB/2024-06-08.log" <<'EOF'
FAIL: token refresh failed
FAIL: login API timeout
OK: healthcheck 200
EOF

RUN cat > "${WORKSPACE}/logs/serviceC/2024-06-07.log" <<'EOF'
OK: initial handshake 200
FAIL: search API 502
OK: teardown 200
EOF

RUN cat > "${WORKSPACE}/logs/serviceC/archive/2024-05-30.log" <<'EOF'
FAIL: should not be included because old
OK: cleanup complete
EOF

RUN find "${WORKSPACE}/logs" -type f -exec chmod 0644 {} + && \
    echo "Container setup for API log-processing task completed."

WORKDIR /home/user/api_tests

CMD ["sh", "-c", "chmod 755 /home/user && echo 'This container is ready for the API-tests workspace task.' && echo 'Your working directory is /home/user/api_tests'"]