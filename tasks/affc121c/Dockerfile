FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Autograder Setup"
LABEL Description="Environment for Grafana dashboard batch-operations exercise"

# Help section as comments
# This container provides the initial filesystem state and required tooling
# (pytest, GNU core utilities) for the "Grafana dashboard batch-operations"
# exercise.

# Post section
RUN set -e && \
    echo "Updating package index and installing Python + pip..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        curl \
        git \
        locales && \
    echo "Installing pytest..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Configuring locale (UTF-8)…" && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 && \
    echo "Creating initial directory structure and dashboard files..." && \
    mkdir -p /home/user/dashboards && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/dashboards

# Create the three JSON dashboard files with exact contents
RUN cat > /home/user/dashboards/app_error.json <<'EOF'
{"dashboard":"app_error"}
EOF

RUN cat > /home/user/dashboards/latency_overview.json <<'EOF'
{"dashboard":"latency_overview"}
EOF

RUN cat > /home/user/dashboards/system_health.json <<'EOF'
{"dashboard":"system_health"}
EOF

# Ensure a single trailing newline on each file and make them world-writable
RUN for f in /home/user/dashboards/*.json; do \
        sed -i -e '$a\' "$f"; \
        chmod 0666 "$f"; \
    done

# Environment variables
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Set working directory
WORKDIR /home/user