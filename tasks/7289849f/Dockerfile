FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest

# Prepare the filesystem layout expected by the exercise & tests
# 1. Create the home hierarchy for the (non-root) agent
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# 2. Create the "remote host" tree with its three reference log files
RUN mkdir -p /home/user/remote_host/var/logs

# app1.log (81 bytes)
RUN cat > /home/user/remote_host/var/logs/app1.log <<'EOF'
2023-05-01 12:00:00 INFO App1 started
2023-05-01 12:05:00 ERROR Something failed
EOF

# app2.log (40 bytes)
RUN cat > /home/user/remote_host/var/logs/app2.log <<'EOF'
2023-05-01 13:00:00 INFO App2 heartbeat
EOF

# sys.log (43 bytes) - note the double space after "May"
RUN cat > /home/user/remote_host/var/logs/sys.log <<'EOF'
May  1 14:00:00 host kernel: Boot complete
EOF

# 3. Ensure world-readable files and executable directories
RUN chmod 0755 /home/user/remote_host /home/user/remote_host/var /home/user/remote_host/var/logs && \
    chmod 0644 /home/user/remote_host/var/logs/*.log

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

WORKDIR /home/user

# Default entry: drop into a shell
CMD ["/bin/bash"]