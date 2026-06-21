FROM ubuntu:22.04

# Labels
LABEL Author="network-exercise-setup"
LABEL Description="Container with initial ICMP-reachability logs and pytest installed for learner task."

# Update APT and install Python & pytest
RUN set -e && \
    echo "Updating APT and installing Python & pytest..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest

# Create initial directory structure
RUN echo "Creating initial directory structure and log files..." && \
    mkdir -p /home/user/network/logs && \
    chmod 0777 /home/user/network && \
    chmod 0755 /home/user/network/logs

# Create ping_results_2023-08-15.log
RUN cat >/home/user/network/logs/ping_results_2023-08-15.log <<'EOF'
2023-08-15 09:00:01 Host: 192.168.1.1 Status: alive time=0.23ms
2023-08-15 09:00:04 Host: 192.168.1.2 Status: unreachable
2023-08-15 09:15:10 Host: 192.168.1.3 Status: alive time=0.30ms
2023-08-15 09:30:55 Host: 192.168.1.2 Status: unreachable
2023-08-15 10:00:40 Host: 192.168.1.4 Status: alive time=0.28ms
EOF

# Create ping_results_2023-08-16.log
RUN cat >/home/user/network/logs/ping_results_2023-08-16.log <<'EOF'
2023-08-16 09:00:01 Host: 192.168.1.1 Status: alive time=0.25ms
2023-08-16 09:05:14 Host: 192.168.1.5 Status: unreachable
2023-08-16 09:15:10 Host: 192.168.1.3 Status: alive time=0.29ms
2023-08-16 09:35:22 Host: 192.168.1.5 Status: unreachable
2023-08-16 09:50:33 Host: 192.168.1.6 Status: alive time=0.31ms
2023-08-16 10:05:45 Host: 192.168.1.2 Status: unreachable
EOF

# Set permissions on log files
RUN chmod 0644 /home/user/network/logs/ping_results_2023-08-15.log && \
    chmod 0644 /home/user/network/logs/ping_results_2023-08-16.log && \
    chmod 755 /home/user && \
    echo "Initial environment ready."

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH