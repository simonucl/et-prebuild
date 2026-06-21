FROM ubuntu:22.04

# Install required software: Python, pip, pytest, and GNU make
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        make \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial directory layout and seed files for the exercise
RUN set -e && \
    BASE="/home/user/support_tickets" && \
    mkdir -p "${BASE}/data" "${BASE}/scripts"

# tickets.csv
RUN BASE="/home/user/support_tickets" && \
    cat > "${BASE}/data/tickets.csv" <<'EOF'
id,client,issue
101,Acme Corp,Printer not responding
102,Globex Inc,VPN disconnecting
103,Initech,Email bounce back
EOF

# Stub resolver script
RUN BASE="/home/user/support_tickets" && \
    cat > "${BASE}/scripts/resolve_ticket.sh" <<'EOF'
#!/usr/bin/env bash
# simple stub used by tests
echo "Ticket $1 resolved"
EOF

RUN chmod 0755 /home/user/support_tickets/scripts/resolve_ticket.sh

# Ensure subsequent, non-root users can add/edit files
RUN chmod -R a+rwX /home/user/support_tickets

# Set environment variables
ENV PATH="/home/user/.local/bin:${PATH}"

# Ensure home permissions
RUN chmod 755 /home/user

# Default runscript equivalent
CMD ["bash"]