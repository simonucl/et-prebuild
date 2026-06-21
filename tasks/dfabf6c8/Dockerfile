FROM ubuntu:22.04

# Help: This container sets up the initial filesystem state for the
# observability-dashboard version-bump task and provides pytest for
# verification.

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial project state
RUN mkdir -p /home/user/observability-dashboard

# VERSION file (single line + LF)
RUN cat > /home/user/observability-dashboard/VERSION <<'EOF'
1.4.2
EOF

# CHANGELOG.md with the initial 1.4.2 section
RUN cat > /home/user/observability-dashboard/CHANGELOG.md <<'EOF'
## [1.4.2] - 2023-04-27
### Fixed
– Corrected alert rule syntax in latency dashboard

EOF

# Make sure the agent (non-root at runtime) can modify everything
RUN chmod 0777 /home/user/observability-dashboard && \
    chmod 0666 /home/user/observability-dashboard/VERSION /home/user/observability-dashboard/CHANGELOG.md && \
    chmod 755 /home/user

LABEL Author="observability-task-builder"
LABEL Description="Initial state for Grafana dashboard version-bump exercise."