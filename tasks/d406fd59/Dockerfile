FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer setup for logtool challenge"
LABEL Description="Initial container state for the logtool file-editing exercise."

# Basic tooling
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create initial project structure and seed files
RUN mkdir -p /home/user/logtool/config && \
    mkdir -p /home/user/logtool/output

# settings.yaml (initial state expected by the tests)
RUN cat > /home/user/logtool/config/settings.yaml <<'EOF'
# LogTool configuration
alert_threshold: 90
pattern_detection: false
log_paths:
  - /var/log/syslog
  - /var/log/auth.log
EOF

# filters.toml (initial state expected by the tests)
RUN cat > /home/user/logtool/config/filters.toml <<'EOF'
# Default filter rules
[[rules]]
name = "ignore_health_checks"
pattern = "healthcheck"
action = "drop"
EOF

# Ensure non-root users can work with the repo
RUN chmod -R a+rwX /home/user

# Environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH