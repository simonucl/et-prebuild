# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help:
# This container image sets up the initial filesystem and dependencies for the
# "API stability problems" exercise. It contains:
#   • Python 3 and pytest
#   • /home/user/project/logs/api_access.log pre-populated with 13 lines
# The student is expected to create /home/user/project/output and the required
# artefacts during their solution.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/project/logs

RUN chmod 0777 /home/user && \
    chmod 0777 /home/user/project && \
    chmod 0755 /home/user/project/logs

RUN cat > /home/user/project/logs/api_access.log <<'EOF'
2023-04-15T09:59:12Z [REQ0001] GET /health 200 23
2023-04-15T10:00:01Z [REQ0002] POST /login 200 345
2023-04-15T10:15:32Z [REQ0003] GET /users 200 134
2023-04-15T10:16:05Z [REQ0004] GET /users/42 404 56
2023-04-15T10:20:45Z [REQ0005] POST /orders 500 678
2023-04-15T10:21:12Z [REQ0006] GET /orders/99 200 2451
2023-04-15T10:22:30Z [REQ0007] GET /metrics 200 78
2023-04-15T11:03:19Z [REQ0008] PUT /users/42 200 3120
2023-04-15T11:10:00Z [REQ0009] DELETE /orders/12 204 89
2023-04-16T08:00:01Z [REQ0010] GET /health 200 25
2023-04-16T08:05:45Z [REQ0011] POST /login 400 48
2023-04-16T09:30:22Z [REQ0012] POST /orders 201 92
2023-04-16T09:45:12Z [REQ0013] GET /users 503 158
EOF

RUN chmod 0644 /home/user/project/logs/api_access.log

RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

LABEL Author="Apptainer Setup Bot"
LABEL Description="Environment for API stability log filtering task with pytest pre-installed."