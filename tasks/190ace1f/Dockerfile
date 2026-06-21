FROM ubuntu:22.04

# Help documentation:
# This container provides the starting environment for the
# "capacity-planning report" exercise.
#
# Pre-created items:
#   • /home/user/metrics/cpu.log
#   • /home/user/metrics/memory.log
#
# The /home/user directory is writable so that learners can
# create /home/user/reports/usage_summary.csv as instructed.

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        python3-setuptools && \
    pip3 install --no-cache-dir pytest

# Create the metrics directory
RUN mkdir -p /home/user/metrics

# Create cpu.log file
RUN cat > /home/user/metrics/cpu.log <<'EOF'
2024-06-01T00:00 15
2024-06-01T01:00 17
2024-06-01T02:00 20
EOF

# Create memory.log file
RUN cat > /home/user/metrics/memory.log <<'EOF'
2024-06-01T00:00 45
2024-06-01T01:00 50
2024-06-01T02:00 55
EOF

# Set appropriate permissions
RUN chmod -R a+r /home/user/metrics && \
    chmod 0777 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

WORKDIR /home/user