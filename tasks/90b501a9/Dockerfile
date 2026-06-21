FROM ubuntu:22.04

# Basic build utilities
RUN apt-get update && apt-get install -y --no-install-recommends python3-pip && pip3 install --no-cache-dir pytest && rm -rf /var/lib/apt/lists/*

# Directory structure
RUN mkdir -p /home/user/monitoring/conf && mkdir -p /home/user/monitoring/logs

# alerts.yaml
RUN cat <<'EOF' > /home/user/monitoring/conf/alerts.yaml
# Managed by monitoring team
alerts:
  - name: disk_space_low
    severity: warning
    expr: (node_filesystem_free_bytes / node_filesystem_size_bytes) < 0.1
    for: 5m
    labels:
      team: ops
    annotations:
      summary: Low disk space on {{ $labels.instance }}
      description: Free disk space is below 10% for more than 5 minutes.
    chmod 755 /home/user


  # --- ADD NEW ALERTS BELOW THIS LINE ---
EOF

# thresholds.toml
RUN cat <<'EOF' > /home/user/monitoring/conf/thresholds.toml
[global]
timezone = "UTC"

# --- ADD ALERT THRESHOLDS BELOW THIS LINE ---
EOF

# Permissions
RUN chown -R 1000:1000 /home/user || true
RUN chmod -R u+rwX,go+rX-w /home/user

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Labels
LABEL Author="highcpu-task-prep"
LABEL Description="Container with baseline monitoring configuration for high_cpu alert exercise"