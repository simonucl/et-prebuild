FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the required directory structure
RUN mkdir -p /home/user/test_data

# Populate test_results.csv with the exact content specified
RUN cat > /home/user/test_data/test_results.csv <<'EOF'
TC_ID,Status
TC001,PASS
TC002,FAIL
TC003,PASS
TC004,FAIL
TC005,SKIP
TC006,FAIL
TC007,PASS
TC008,SKIP
TC009,PASS
TC010,PASS
EOF

# Set sensible permissions (readable by any unprivileged user)
RUN chmod 755 /home/user && \
    chmod 755 /home/user/test_data && \
    chmod 644 /home/user/test_data/test_results.csv

# Ensure Python output is unbuffered for clarity during grading
ENV PYTHONUNBUFFERED=1