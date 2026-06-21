FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare initial project structure and seed files for the learner
# ------------------------------------------------------------------
RUN mkdir -p /home/user/projects/observability/grafana

# dashboard.yaml (original 7-line file)
RUN cat > /home/user/projects/observability/grafana/dashboard.yaml <<'EOF'
title: "Service Overview"
panels:
  - id: 1
    title: "CPU Usage"
    datasource: "Prometheus"
    targets:
      - expr: "rate(node_cpu_seconds_total[5m])"
EOF

# alerting.toml (alerting disabled)
RUN cat > /home/user/projects/observability/alerting.toml <<'EOF'
[alerting]
enabled = false
EOF

# Ensure the student (non-root) can freely modify everything under /home/user
RUN chmod -R a+rwX /home/user && \
    chmod 755 /home/user

# Labels
LABEL Author="observability-task-setup"

# Help: This container sets up the initial state for the observability editing task
# and includes pytest for automated evaluation.