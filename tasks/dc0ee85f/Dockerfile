FROM ubuntu:22.04

# Labels
LABEL Maintainer="cpu-hog-prep"
LABEL Description="Environment for the CPU-hog performance-snapshot exercise"

# Basic tools and Python environment
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip procps ca-certificates && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# Prepare working directory
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Create helper script
RUN cat >/home/user/cpu_hog.sh <<'EOF'
#!/usr/bin/env bash
# Very small infinite loop to eat CPU
while true; do :; done
EOF

RUN chmod 0755 /home/user/cpu_hog.sh

# Ensure the perf_logs directory does NOT exist in the pristine image
RUN rm -rf /home/user/perf_logs

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

WORKDIR /home/user