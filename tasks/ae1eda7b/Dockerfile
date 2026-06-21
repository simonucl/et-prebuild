# syntax=docker/dockerfile:1
# Author Incident-Frequency Task Builder
# Description Base image for the "Count incident frequency per component" task.
# This image provides:
#   - /home/user/incidents/alerts.log seed log file
#   - pytest for automated grading

FROM ubuntu:22.04

ENV PATH="/usr/local/bin:${PATH}"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/incidents && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/incidents

RUN cat > /home/user/incidents/alerts.log <<'EOF'
2024-05-06T12:01:02Z ERROR auth-service
2024-05-06T12:01:03Z WARN payment-service
2024-05-06T12:01:04Z ERROR auth-service
2024-05-06T12:01:05Z CRITICAL inventory-service
2024-05-06T12:01:06Z ERROR payment-service
2024-05-06T12:01:07Z ERROR auth-service
2024-05-06T12:01:08Z WARN auth-service
2024-05-06T12:01:09Z ERROR shipping-service
2024-05-06T12:01:10Z ERROR payment-service
2024-05-06T12:01:11Z CRITICAL auth-service
EOF

RUN chmod 0644 /home/user/incidents/alerts.log && \
    chmod 755 /home/user