FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Setup"
LABEL Description="Base image for process-health tuning exercise"

# Basic utilities and Python tooling
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        procps \
        jq && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user `user`
RUN useradd -m -s /bin/bash user

# Prepare initial dashboard directory and file
RUN install -d -m 755 /home/user/dashboards

RUN cat > /home/user/dashboards/app_server_dashboard.json <<'EOF'
{
  "dashboard": "App Server Metrics",
  "panels": [
    {
      "id": 1,
      "metric": "cpu_usage",
      "threshold": 75
    },
    {
      "id": 2,
      "metric": "memory_usage",
      "threshold": 80
    }
  ]
}
EOF

RUN chmod 644 /home/user/dashboards/app_server_dashboard.json && \
    chown -R user:user /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/home/user/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH}"

# Set working directory
WORKDIR /home/user

# Default action: drop into a shell
CMD ["/bin/bash"]