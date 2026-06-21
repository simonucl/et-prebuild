# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from %labels
LABEL Author="MLOps Task Setup"
LABEL Description="Container for latest-metrics logging exercise with pytest pre-installed."

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state expected by the assignment/tests
RUN set -e && \
    mkdir -p /home/user/experiments/exp_v1

# Populate metrics.csv with the required historical data
RUN cat > /home/user/experiments/exp_v1/metrics.csv <<'EOF'
epoch,loss,accuracy
1,0.678,0.75
2,0.432,0.82
3,0.321,0.86
EOF

# Ensure permissions allow the (non-root) runtime user to create / overwrite files
RUN chmod -R a+rwx /home/user/experiments

# Make sure the target log file does NOT exist yet
RUN rm -f /home/user/experiments/exp_v1/latest_metrics.log

# Ensure home directory permissions
RUN mkdir -p /home/user && chmod 755 /home/user

# Environment variables from %environment
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8