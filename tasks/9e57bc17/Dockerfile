FROM ubuntu:22.04

# Install Python tooling and pytest
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial task files
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

RUN cat >/home/user/server_access.log <<'EOF'
server1
server2
server1
server3
server2
server2
server1
server4
server3
EOF

RUN chmod 0644 /home/user/server_access.log

# Apply final permissions as in %environment
RUN chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# Labels
LABEL Author="Generated for coding task – access-log rotation setup"