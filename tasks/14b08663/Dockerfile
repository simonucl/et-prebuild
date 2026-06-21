FROM ubuntu:22.04

# Help text
# This container provides the initial state required for the log-analysis task:
#   - /home/user/logs/server.log is pre-populated with sample data.
#   - pytest is installed for automated grading.
# The /home/user/analysis directory is intentionally absent; student code
# should create it and produce the required artefacts there.

ENV PYTHONUNBUFFERED=1

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -qq && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/logs && \
    chmod 0777 /home/user

RUN cat <<'EOF' > /home/user/logs/server.log
2023-11-01T12:00:00Z | INFO | API | 10.0.0.1 | Request completed in 150ms
2023-11-01T12:00:01Z | WARN | AUTH | 10.0.0.2 | Password attempt failed 100ms
2023-11-01T12:00:02Z | ERROR | API | 10.0.0.1 | DB connection timeout after 300ms
2023-11-01T12:00:03Z | INFO | FRONTEND | 192.168.1.1 | Page rendered in 80ms
2023-11-01T12:00:04Z | ERROR | AUTH | 10.0.0.3 | Unauthorized access 200ms
2023-11-01T12:00:05Z | INFO | API | 10.0.0.1 | Request completed in 110ms
2023-11-01T12:00:06Z | WARN | FRONTEND | 192.168.1.1 | Slow image load 250ms
2023-11-01T12:00:07Z | ERROR | FRONTEND | 192.168.1.1 | JS exception 90ms
2023-11-01T12:00:08Z | INFO | AUTH | 10.0.0.2 | Login successful 120ms
2023-11-01T12:00:09Z | INFO | API | 10.0.0.4 | Request completed in 140ms
2023-11-01T12:00:10Z | ERROR | API | 10.0.0.4 | Timeout after 400ms
2023-11-01T12:00:11Z | INFO | FRONTEND | 192.168.1.1 | Page rendered in 70ms
2023-11-01T12:00:12Z | WARN | API | 10.0.0.1 | High latency 310ms
2023-11-01T12:00:13Z | INFO | AUTH | 10.0.0.3 | Logout complete 90ms
2023-11-01T12:00:14Z | ERROR | AUTH | 10.0.0.2 | Invalid token 150ms
EOF

RUN chmod 0644 /home/user/logs/server.log && \
    chmod 0755 /home/user/logs && \
    chmod 755 /home/user

CMD echo "Container built for log-analysis task. Open a shell to use." >&2 && exec "$@"