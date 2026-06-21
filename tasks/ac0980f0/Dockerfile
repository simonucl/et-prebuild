# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help:
# This container image sets up the initial state required for the “active_services.csv”
# exercise. It pre-populates /home/user/services/registry.txt and installs pytest so
# that the automated test-suite can verify the pristine state before the learner
# executes any commands.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/services

RUN cat > /home/user/services/registry.txt <<'EOF'
webapp	8080	up
auth	9090	up
payments	7070	down
monitor	8181	up
search	9200	down
cache	6379	up
EOF

RUN chmod -R a+rwX /home/user/services && chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

LABEL Author="Container Exercise Autogen"
LABEL Description="Environment for the micro-services registry transformation task"