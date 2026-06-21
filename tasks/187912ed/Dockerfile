FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create required directory structure
RUN mkdir -p /home/user/observability/templates

# Create baseline template file
RUN cat <<'EOF' > /home/user/observability/templates/metrics_base.json
{
  "id": null,
  "title": "Base Metrics Dashboard",
  "uid": "base-metrics",
  "tags": [
    "base"
  ],
  "refresh": "10s",
  "panels": []
}
EOF

# Set permissions
RUN chmod 0755 /home/user && \
    chmod -R 0755 /home/user/observability && \
    chmod 0644 /home/user/observability/templates/metrics_base.json

# Environment settings
ENV PYTHONUNBUFFERED=1