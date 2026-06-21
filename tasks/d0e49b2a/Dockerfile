FROM ubuntu:22.04

# Labels
LABEL Author="release-manager-task"
LABEL Description="Container with initial deployment configuration files and pytest pre-installed for grading."

# Environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Install Python and pip
RUN set -e && \
    echo "Updating package index and installing Python tooling..." && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    echo "Installing pytest for the grading suite..." && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create deployment configuration directory
RUN mkdir -p /home/user/deployment_configs && \
    chmod 755 /home/user/deployment_configs

# Create service_alpha.conf
RUN cat > /home/user/deployment_configs/service_alpha.conf <<'EOF'
ServiceName: AlphaAPI
Version: 1.3.7
Environment: staging
Status: READY
EOF

# Create service_beta.conf
RUN cat > /home/user/deployment_configs/service_beta.conf <<'EOF'
ServiceName: BetaWorker
Version: 3.2.4
Environment: production
Status: LIVE
EOF

# Create service_gamma.conf
RUN cat > /home/user/deployment_configs/service_gamma.conf <<'EOF'
ServiceName: GammaDB
Version: 0.9.12
Environment: staging
Status: READY
EOF

# Create service_delta.conf
RUN cat > /home/user/deployment_configs/service_delta.conf <<'EOF'
ServiceName: DeltaUI
Version: 2.1.0
Environment: staging
Status: IN_TEST
EOF

# Set permissions on config files
RUN chmod 644 /home/user/deployment_configs/*.conf