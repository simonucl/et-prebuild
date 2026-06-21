FROM ubuntu:22.04

# Labels
LABEL Author="Acme-Payments Task Setup"
LABEL Description="Container image pre-configured for the Acme-Payments firewall exercise."
LABEL Maintainer="example@example.com"

# Update apt cache and install Python + pip
RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest for the forthcoming test suites
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state for the "Acme-Payments" exercise
# 1. Writable firewall directory
RUN mkdir -p /home/user/firewall && \
    chmod 0777 /home/user/firewall

# 2. Base rules file (read-only to the learner)
RUN cat > /home/user/firewall/base.rules <<'EOF'
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
-A INPUT -i lo -j ACCEPT
COMMIT
EOF

RUN chmod 0644 /home/user/firewall/base.rules

# 3. Writable release log directory
RUN mkdir -p /home/user/release_logs && \
    chmod 0777 /home/user/release_logs

# Set permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Default command
CMD ["/bin/bash", "-l"]