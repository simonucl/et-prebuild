FROM ubuntu:22.04

# Labels
LABEL Author="FinOps-Exercise"
LABEL Description="Container for Investigate Expensive Running Cloud Instances via Curl task"

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Install system packages and pytest
RUN set -e \
 && apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      python3 \
      python3-pip \
      curl \
      jq \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && pip3 install --no-cache-dir pytest

# Create mock API directory and add fixture
RUN mkdir -p /home/user/mock_api

RUN cat <<'EOF' > /home/user/mock_api/costs.json
{
  "instances": [
    { "id": "i-07bd", "state": "running",  "hourly_cost": 0.12 },
    { "id": "i-18ef", "state": "running",  "hourly_cost": 0.45 },
    { "id": "i-21aa", "state": "stopped",  "hourly_cost": 0.37 },
    { "id": "i-3cb2", "state": "running",  "hourly_cost": 0.31 },
    { "id": "i-4ddc", "state": "running",  "hourly_cost": 0.29 }
  ]
}
EOF

# Fix permissions
RUN chmod 755 /home/user \
 && chmod 755 /home/user/mock_api \
 && chmod 644 /home/user/mock_api/costs.json