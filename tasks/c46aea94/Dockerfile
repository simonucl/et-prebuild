# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python tooling for the test harness
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state expected by the exercise
RUN mkdir -p /home/user/logs

# Generate log files with exact byte counts
RUN yes line | head -n 100 > /home/user/logs/access.log && \
    yes line | head -n 50  > /home/user/logs/error.log && \
    yes line | head -n 200 > /home/user/logs/app.log

# Ensure permissions
RUN chmod 777 /home/user/logs && \
    chmod 644 /home/user/logs/*.log && \
    chmod 755 /home/user

# Default run behavior
CMD ["bash"]