FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create required directory and input file
RUN mkdir -p /home/user/performance

RUN cat <<'EOF' > /home/user/performance/running_containers.txt
redis
nginx
metrics_collector
auth_service
EOF

# Adjust permissions
RUN chmod 755 /home/user && \
    chmod 0777 /home/user/performance && \
    chmod 0666 /home/user/performance/running_containers.txt

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

CMD echo "Container for the running-containers counting task. No default action."