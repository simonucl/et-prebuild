FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create required directory hierarchy under /home/user
RUN mkdir -p /home/user/containers/proxy && \
    mkdir -p /home/user/containers/api && \
    mkdir -p /home/user/vuln_db

# Populate container bundle JSON files - proxy
RUN cat > /home/user/containers/proxy/container.json <<'EOF'
{
  "Config": {
    "ExposedPorts": {
      "80/tcp": {},
      "443/tcp": {},
      "8080/tcp": {}
    }
  }
}
EOF

# Populate container bundle JSON files - api
RUN cat > /home/user/containers/api/container.json <<'EOF'
{
  "Config": {
    "ExposedPorts": {
      "3000/tcp": {},
      "22/tcp": {}
    }
  }
}
EOF

# Populate vulnerability CSV
RUN cat > /home/user/vuln_db/vuln_ports.csv <<'EOF'
Port,Service,Severity
22,OpenSSH,Medium
80,HTTP,Low
443,HTTPS,Low
3000,NodeJS-Dev-Server,Critical
8080,JBoss,Critical
EOF

# Set permissions
RUN chmod 644 /home/user/containers/proxy/container.json && \
    chmod 644 /home/user/containers/api/container.json && \
    chmod 644 /home/user/vuln_db/vuln_ports.csv && \
    chmod 0777 /home/user

# Labels
LABEL Author="Automated Build"
LABEL Description="Environment for container-based vulnerability correlation task"