FROM ubuntu:22.04

# Author ping-summary-task
# Description "Base image for ping summary exercise with pytest and initial CSV pre-populated."
# This Apptainer image provides the starting state for the “ping summary” programming task.
# It contains:
#   • /home/user/net_tests/ping_results.csv
#   • pytest installed for automated grading
# The directory /home/user/net_tests is writable by an unprivileged user so the agent can create ping_summary.json and action.log.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip jq ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    mkdir -p /home/user/net_tests

RUN cat > /home/user/net_tests/ping_results.csv <<'EOF'
host,status,latency_ms
8.8.8.8,success,23
1.1.1.1,success,19
192.0.2.1,failed,
example.com,success,45
EOF

RUN chmod 0777 /home/user/net_tests && \
    chmod 0644 /home/user/net_tests/ping_results.csv && \
    chown -R 1000:1000 /home/user || true

RUN chmod 755 /home/user

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

LABEL Author="ping-summary-task" \
      Description="Base image for ping summary exercise with pytest and initial CSV pre-populated."