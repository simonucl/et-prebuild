# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="automation-bot" \
      Description="Environment for text-processing automation task"

# Ensure required packages are present and install pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        gawk \
        sed \
        grep \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

# Prepare filesystem layout expected by the automated tests
RUN mkdir -p /home/user && \
    chmod 0755 /home/user && \
    mkdir -p /home/user/automation_logs && \
    chmod 0777 /home/user/automation_logs

# Populate system_report.txt with the exact seven lines (LF endings)
RUN cat > /home/user/automation_logs/system_report.txt <<'EOF'
2023-09-14 10:00:01 [INFO] System boot
2023-09-14 10:01:15 [WARN] Disk space low
2023-09-14 10:05:42 [ERROR] Failed to start service A
2023-09-14 10:10:30 [INFO] Service B started
2023-09-14 10:15:00 [WARN] High memory usage
2023-09-14 10:20:20 [ERROR] Unhandled exception
2023-09-14 10:25:55 [INFO] Health check passed
EOF

# Set correct permissions (world-readable)
RUN chmod 0644 /home/user/automation_logs/system_report.txt

# Environment setup
RUN chmod 0755 /home/user
ENV LC_ALL=C \
    LANG=C

# Default command (equivalent to %runscript)
CMD ["/bin/bash"]