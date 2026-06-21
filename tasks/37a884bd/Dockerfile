FROM ubuntu:22.04

# Labels
LABEL Author="SRE_Task_Setup"
LABEL Description="Docker container for API health-log parsing task with pytest pre-installed."

# Set environment variables
ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/logs

# Create log file with heredoc
RUN cat > /home/user/logs/service_status.log <<'EOF'
2023-05-01T00:00:01Z UP 48ms
2023-05-01T00:05:01Z DOWN
2023-05-01T00:10:01Z UP 45ms
2023-05-01T01:15:22Z UP 46ms
2023-05-01T01:20:22Z DOWN
2023-05-01T02:30:31Z UP 47ms
2023-05-01T03:30:31Z UP 44ms
2023-05-01T03:35:31Z DOWN
2023-05-01T04:00:00Z UP 41ms
2023-05-01T04:30:00Z UP 42ms
EOF

# Ensure readable permissions
RUN chmod 644 /home/user/logs/service_status.log && \
    chmod 755 /home/user && \
    chmod 755 /home/user/logs

# Clean up APT caches
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*