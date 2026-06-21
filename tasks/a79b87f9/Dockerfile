FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set up initial directory structure and log file
RUN mkdir -p /home/user/ci_cd/logs

# Create the initial build.log with exact required content and LF endings
RUN cat >/home/user/ci_cd/logs/build.log <<'EOF'
2023-07-01 12:00:00 INFO Build started
2023-07-01 12:00:01 INFO Running tests...
2023-07-01 12:00:02 FAIL TestUserLogin failed with AssertionError
2023-07-01 12:00:03 ERROR Deployment aborted
2023-07-01 12:00:04 WARNING Disk space low
2023-07-01 12:00:05 FAIL TestPaymentProcessing failed with NullPointerException
2023-07-01 12:00:06 INFO Build finished
EOF

# Ensure directories are writable by the runtime (non-root) user
RUN chmod -R 0777 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH