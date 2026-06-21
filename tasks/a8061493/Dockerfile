# syntax=docker/dockerfile:1
FROM ubuntu:22.04

LABEL Author="cloud-cost-init"
LABEL Version="1.0"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN set -e && \
    PROJECT_DIR=/home/user/projects/cloud-cost-optimizer && \
    CFG_DIR=${PROJECT_DIR}/config && \
    LOG_DIR=${PROJECT_DIR}/logs && \
    mkdir -p "${CFG_DIR}" && \
    mkdir -p "${LOG_DIR}"

RUN cat > /home/user/projects/cloud-cost-optimizer/config/thresholds.yml <<'EOF'
aws:
  monthly_budget: 7000
  alert_at_percent: 90
azure:
  monthly_budget: 5000
  alert_at_percent: 90
gcp:
  monthly_budget: 4000
  alert_at_percent: 90
EOF

RUN cat > /home/user/projects/cloud-cost-optimizer/config/alerts.toml <<'EOF'
[email]
recipients = ["finops@example.com","cloudteam@example.com"]
EOF

RUN chmod -R a+rwX /home/user/projects && \
    chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# Help section was provided in the source Apptainer file