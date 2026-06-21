FROM ubuntu:22.04

# Labels
LABEL Author="Container Setup Automation"
LABEL Description="Base image for the ping-health uptime summary task."

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure /home/user exists and is writable by whoever runs the container
RUN mkdir -p /home/user && \
    chmod 777 /home/user

# Create the logs directory with the exact permissions the tests expect
RUN mkdir -p /home/user/logs && \
    chmod 755 /home/user/logs

# Populate the ping_results.log file with the ground-truth data
RUN cat > /home/user/logs/ping_results.log <<'EOF'
2024-08-12 10:00 server1.example.com UP
2024-08-12 10:00 server2.example.com DOWN
2024-08-12 10:01 server3.example.com UP
2024-08-12 10:02 server1.example.com UP
2024-08-12 10:03 server2.example.com UP
2024-08-12 10:04 server3.example.com DOWN
2024-08-12 10:05 server1.example.com UP
2024-08-12 10:06 server3.example.com UP
2024-08-12 10:07 server1.example.com UP
2024-08-12 10:08 server2.example.com DOWN
EOF

RUN chmod 644 /home/user/logs/ping_results.log

# NOTE: Intentionally DO NOT create /home/user/summary — the student
# is expected to generate it during the exercise.

# Help information (as comment):
# This container image provides the initial state (log files, directories,
# and required Python tooling) for the uptime summary coding challenge.