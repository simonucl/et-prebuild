FROM ubuntu:22.04

# Labels
LABEL Author="FinOpsTaskBuilder"
LABEL Description="Container seeded for Prometheus firewall configuration task."

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create /home/user hierarchy
RUN mkdir -p /home/user/config && \
    mkdir -p /home/user/logs

# Set directory permissions (agent will not have root privileges)
RUN chmod 755 /home/user && \
    chmod 755 /home/user/config && \
    chmod 755 /home/user/logs

# Create the baseline firewall.rules file with EXACT content + trailing newline
RUN cat > /home/user/config/firewall.rules <<'EOF'
-A INPUT -p tcp --dport 22 -j ACCEPT
-A INPUT -j DROP
EOF

RUN chmod 644 /home/user/config/firewall.rules

# Intentionally DO NOT create /home/user/logs/firewall_actions.log
# so that initial-state tests confirm its absence.

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Default command
CMD ["bash"]