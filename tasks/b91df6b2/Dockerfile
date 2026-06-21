FROM ubuntu:22.04

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    echo "Updating package index and installing dependencies..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        time \
        parallel \
        jq \
        ca-certificates && \
    echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating baseline directory structure and files..." && \
    mkdir -p /home/user && \
    mkdir -p /home/user/policy_tests/scripts

# Create compute.sh with executable workload
RUN cat >/home/user/policy_tests/scripts/compute.sh <<'EOF'
#!/usr/bin/env bash
# Very small CPU-bound workload (~0.5-1s)
for i in $(seq 1 150000); do
  : $((i * i))
done
EOF

RUN chmod 755 /home/user/policy_tests/scripts/compute.sh

# Create policy.conf with required thresholds
RUN cat >/home/user/policy_tests/policy.conf <<'EOF'
MAX_RUNTIME_MS=1500
MAX_MEMORY_KB=300000
EOF

RUN chmod 644 /home/user/policy_tests/policy.conf

# Ensure write permissions for future artefacts
RUN chmod -R a+rwx /home/user/policy_tests

# Clean up apt caches to reduce image size
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/user

# Default command
CMD echo "Container for Policy-as-Code Performance Benchmark." && \
    echo "Everything is prepared under /home/user/policy_tests." && \
    echo "Invoke your benchmark scripts from the host environment."