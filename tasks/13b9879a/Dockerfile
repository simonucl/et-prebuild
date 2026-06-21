FROM ubuntu:22.04

# Help:
# This image sets up the environment for the incident-response log filtering task.
# Provides:
#   - /home/user/logs/system.log with exact required contents
#   - Correct permissions for creating new logs
#   - pytest installed for automated grading

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -u 1000 user && \
    mkdir -p /home/user/logs && \
    chmod 0755 /home/user/logs

RUN cat > /home/user/logs/system.log <<'EOF'
[2023-05-15 10:03:17] [INFO] System booting
[2023-05-15 10:05:42] [ERROR] Failed to mount /dev/sda1
[2023-05-15 10:07:03] [WARNING] Low disk space
[2023-05-15 10:12:55] [ERROR] Network unreachable
[2023-05-15 10:15:00] [INFO] User login: alice
EOF

RUN chmod 0644 /home/user/logs/system.log && \
    chown -R user:user /home/user && \
    chmod 755 /home/user

ENV PATH="/home/user/.local/bin:${PATH}"

# Run script equivalent
CMD echo "Container for log-processing task. Run your commands inside an interactive shell." && exec /bin/bash