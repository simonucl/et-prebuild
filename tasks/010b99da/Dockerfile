FROM ubuntu:22.04

# Author: ChatGPT
# Description: Environment for quick-check services task with pytest installed
# Help:
# This image contains:
#   * pytest (pre-installed for automated grading)
#   * A pre-built docker-compose.yml at
#     /home/user/projects/metrics/docker-compose.yml
# The student’s task is to generate defined_services.log as specified.

ENV PATH="/usr/local/bin:$PATH"

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/projects/metrics

RUN cat <<'EOF' >/home/user/projects/metrics/docker-compose.yml
version: '3'
services:
  prometheus:
    image: prom/prometheus:latest
  grafana:
    image: grafana/grafana:latest
EOF

RUN chmod 755 /home/user /home/user/projects /home/user/projects/metrics && \
    chmod 644 /home/user/projects/metrics/docker-compose.yml && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*