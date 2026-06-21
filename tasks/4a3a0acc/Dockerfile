FROM ubuntu:22.04

# Help:
# This container provides the initial state required for the
# webapp performance-benchmarking exercise.

LABEL Author="devops-task-prep"
LABEL Description="Container for webapp log performance benchmarking task"

RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/logs && \
    chmod 777 /home/user/logs

RUN cat > /home/user/logs/webapp.log <<'EOF'
2023-10-01T10:00:01Z INFO method=GET path=/api/items            status=200 response_time=100ms
2023-10-01T10:00:02Z INFO method=POST path=/api/items           status=201 response_time=150ms
2023-10-01T10:00:03Z INFO method=GET path=/api/items/42         status=200 response_time=120ms
2023-10-01T10:00:04Z INFO method=PUT path=/api/items/42         status=200 response_time=130ms
2023-10-01T10:00:05Z INFO method=GET path=/api/items            status=200 response_time=110ms
2023-10-01T10:00:06Z INFO method=DELETE path=/api/items/42      status=204 response_time=140ms
2023-10-01T10:00:07Z INFO method=GET path=/api/items            status=200 response_time=115ms
2023-10-01T10:00:08Z INFO method=POST path=/api/items           status=201 response_time=125ms
2023-10-01T10:00:09Z INFO method=GET path=/api/items/99         status=200 response_time=135ms
2023-10-01T10:00:10Z INFO method=GET path=/api/items            status=200 response_time=105ms
EOF

RUN chmod 644 /home/user/logs/webapp.log

RUN chmod 755 /home/user