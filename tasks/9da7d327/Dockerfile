FROM ubuntu:22.04

# Install Python tooling and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state
RUN mkdir -p /home/user/support_ticket/configs && \
    mkdir -p /home/user/support_ticket/report

# Create app1.ini
RUN cat > /home/user/support_ticket/configs/app1.ini <<'EOF'
[AuthService]
enabled=true
port=8080

[DataCollector]
enabled=true
; port intentionally omitted
EOF

# Create app2.ini
RUN cat > /home/user/support_ticket/configs/app2.ini <<'EOF'
[WebPortal]
enabled=true
port=8080

[Metrics]
enabled=false
port=9100
EOF

# Permissions
RUN chmod 0755 /home/user && \
    chmod 0755 /home/user/support_ticket && \
    chmod 0755 /home/user/support_ticket/configs && \
    chmod 0755 /home/user/support_ticket/report && \
    chmod 0644 /home/user/support_ticket/configs/app1.ini && \
    chmod 0644 /home/user/support_ticket/configs/app2.ini

# Environment variables
ENV PYTHONIOENCODING=UTF-8
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Help text (runscript equivalent)
# This container is prepared for the 'service audit' task.
# Enter the shell to start working.

CMD ["/bin/bash"]