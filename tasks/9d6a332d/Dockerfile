FROM ubuntu:22.04

# Help:
# This container provides the baseline filesystem layout for the
# Grafana dashboard symlink exercise and includes pytest for grading.

LABEL Author="ExampleTaskBuilder"
LABEL Purpose="Observability symlink exercise – baseline image with pytest installed"

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/observability/dashboards/archive/2023 && \
    touch /home/user/observability/dashboards/archive/2023/performance_dashboard.json && \
    chmod -R a+rwx /home/user

RUN chmod 755 /home/user

ENV PYTHONUNBUFFERED=1