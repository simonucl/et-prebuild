FROM ubuntu:22.04

# Install Python and pytest
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-wheel && \
    pip install --no-cache-dir pytest

# Create a non-root user `user`
RUN useradd -m -u 1000 -s /bin/bash user

# Set up initial directory and CSV file
RUN install -d -m 755 /home/user/tickets

RUN cat > /home/user/tickets/tickets.csv <<'EOF'
TicketID,User,Issue,Status,Priority
TCK-1001,alice,Cannot login,Open,High
TCK-1002,bob,Printer offline,In Progress,Medium
TCK-1003,charlie,VPN issue,Resolved,Low
TCK-1004,dana,Email bounce,Open,Medium
TCK-1005,ed,Password reset,Resolved,Low
EOF

RUN chmod 644 /home/user/tickets/tickets.csv

# Ensure ownership belongs to the non-root user
RUN chown -R user:user /home/user

# Clean up APT caches to keep the image small
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Set permissions on home directory at runtime
RUN chmod 755 /home/user

# Help:
# This container provides the initial environment for the ticket-processing task.
# It contains:
#   • A non-root user named "user" (UID 1000) with home directory /home/user
#   • The CSV register at /home/user/tickets/tickets.csv
#   • pytest installed for automated grading