FROM ubuntu:22.04

# Labels
LABEL Author="observability-task-generator"
LABEL Description="Container for Prometheus curl metrics validation kata"

# Environment (none needed)

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -s /bin/bash user; \
    fi

RUN mkdir -p /home/user/observability/metrics

RUN cat <<'EOF' > /home/user/observability/metrics/exporter_stats.txt
up 1
scrape_duration_seconds 0.005
scrape_samples_post_metric_relabeling 15
EOF

RUN chown -R user:user /home/user && \
    chmod 755 /home/user && \
    chmod -R 755 /home/user/observability && \
    chmod 644 /home/user/observability/metrics/exporter_stats.txt