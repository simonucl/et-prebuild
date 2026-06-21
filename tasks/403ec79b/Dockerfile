FROM ubuntu:22.04

# Labels
LABEL Author="On-call Sysadmin Exercise"
LABEL Description="Container prepared for 'host count' one-liner task"

# Update APT index and install Python + pip
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Create filesystem layout
RUN mkdir -p /home/user/servers && \
    chmod -R a+rwx /home/user

# Create hosts.lst with exact content
RUN cat <<'EOF' > /home/user/servers/hosts.lst
host-a
host-b
host-c
host-d
host-e
host-f
host-g
EOF

# Ensure hosts.lst is writable
RUN chmod a+rw /home/user/servers/hosts.lst

# Environment setup
RUN chmod 755 /home/user
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH