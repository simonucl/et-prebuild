FROM ubuntu:22.04

# Labels
LABEL Author="db-firewall-task"
LABEL Description="Environment for the firewall rule single-command task"

# Update apt cache and install Python and pytest
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the working directory
RUN mkdir -p /home/user

# Create baseline firewall configuration
RUN cat > /home/user/firewall.conf <<'EOF'
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]

# Allow SSH
-A INPUT -p tcp --dport 22 -j ACCEPT

# DB RULES

COMMIT
EOF

# Make sure the file is writable by the unprivileged user who will run the task
RUN chmod 666 /home/user/firewall.conf

# Clean up apt artifacts to keep the image small
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ENV PYTHONIOENCODING="utf-8"

WORKDIR /home/user

CMD ["/bin/bash", "-l"]