FROM ubuntu:22.04

# Update package lists and install Python + pip
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Create the log directory hierarchy
RUN mkdir -p /home/user/logs

# Populate the single-day uptime log
RUN cat << 'EOF' > /home/user/logs/site-01-2023-10-05.log
2023-10-05T13:00:00Z site-01 OK response_time=120ms
2023-10-05T13:05:00Z site-01 ERROR connection_timeout
2023-10-05T13:10:00Z site-01 OK response_time=118ms
2023-10-05T13:15:00Z site-01 WARNING high_latency response_time=350ms
2023-10-05T13:20:00Z site-01 OK response_time=119ms
2023-10-05T13:25:00Z site-01 CRITICAL host_unreachable
2023-10-05T13:30:00Z site-01 OK response_time=117ms
EOF

# Ensure write permissions
RUN chmod -R 0777 /home/user && chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
ENV PYTHONUNBUFFERED=1