FROM ubuntu:22.04

# Update package lists and install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip curl && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the test harness
RUN pip3 install --no-cache-dir pytest

# Create directory structure for the exercise
RUN mkdir -p /home/user/simple_api && \
    chmod 0755 /home/user /home/user/simple_api

# Create the users.json file
RUN cat <<'EOF' >/home/user/simple_api/users.json
{"users":[{"id":1,"name":"Alice"},{"id":2,"name":"Bob"},{"id":3,"name":"Charlie"}]}
EOF

# Create the status.json file
RUN cat <<'EOF' >/home/user/simple_api/status.json
{"status":"ok","uptime_seconds":1234}
EOF

# Ensure world-readable permissions
RUN chmod 0644 /home/user/simple_api/*.json

# Set environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Set permissions on /home/user
RUN chmod 755 /home/user