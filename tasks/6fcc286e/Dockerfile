# syntax=docker/dockerfile:1
FROM ubuntu:22.04

#--------------------------------------------------
# Environment
#--------------------------------------------------
ENV DEBIAN_FRONTEND=noninteractive

#--------------------------------------------------
# Base OS packages
#--------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        openssl \
        ca-certificates \
        tini && \
    rm -rf /var/lib/apt/lists/*

#--------------------------------------------------
# Python tooling for the grader
#--------------------------------------------------
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

#--------------------------------------------------
# Prepare initial filesystem state for the exercise
#--------------------------------------------------
# Create user home and exercise root (but NOT the certs directory)
RUN mkdir -p /home/user/observability

# Ensure the unprivileged runtime user can write later
RUN chmod 0777 /home/user && \
    chmod 0777 /home/user/observability

# Provide a baseline Grafana configuration that lacks the required HTTPS block
RUN cat >/home/user/observability/grafana.ini <<'EOF'
###############################################
# Baseline Grafana configuration (HTTP only)  #
###############################################

[paths]
data = /var/lib/grafana
logs = /var/log/grafana
plugins = /var/lib/grafana/plugins

#-------------------------------------------------
# NOTE: The mandatory HTTPS [server] block that
# the student must add is intentionally absent.
#-------------------------------------------------
EOF

# Make the file writable for the student/agent
RUN chmod 0666 /home/user/observability/grafana.ini

#--------------------------------------------------
# Permissions adjustment from labels section
#--------------------------------------------------
RUN chmod 0755 /home/user

#--------------------------------------------------
# Labels
#--------------------------------------------------
LABEL Author="Apptainer Exercise Generator" \
      Description="Base container for Grafana HTTPS enablement task"

#--------------------------------------------------
# Help
#--------------------------------------------------
# This container provides the starting environment for the
# “Enable HTTPS for a local Grafana instance” hands-on task.
# The required directories and an initial Grafana configuration
# are present, while the certificate artefacts the student must
# create are deliberately absent. pytest is installed for grading.

#--------------------------------------------------
# Runtime behavior
#--------------------------------------------------
CMD echo "Container for Grafana HTTPS enablement exercise." && \
    echo "No entrypoint action defined."