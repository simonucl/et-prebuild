# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python tooling and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create workspace
RUN mkdir -p /home/user/finops

# cost-alerts.yaml (pristine version)
RUN cat <<'EOF' > /home/user/finops/cost-alerts.yaml
alerts:
  - name: daily-spend
    threshold: 500
    channels:
      - slack
      - email
  - name: monthly-spend
    threshold: 15000
    channels:
      - slack
EOF

# budget.toml (pristine version)
RUN cat <<'EOF' > /home/user/finops/budget.toml
[budget]
monthly_limit = 20000
daily_limit  = 700

[metadata]
owner        = "finops-team"
last_updated = "2023-01-15"
EOF

# Permissions
RUN chmod 777 /home/user/finops && \
    chmod 666 /home/user/finops/cost-alerts.yaml /home/user/finops/budget.toml && \
    chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

LABEL Author="ChatGPT (FinOps setup)"
LABEL Description="Base container for FinOps cost-control configuration editing exercise"