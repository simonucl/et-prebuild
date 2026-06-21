FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer build script"
LABEL Description="Initial container for the hostname look-ups QA exercise"

# Environment variables
ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create directory for seed data
RUN mkdir -p /home/user/qa_env

# Create the test_hosts file
RUN cat > /home/user/qa_env/test_hosts <<'EOF'
10.10.0.5    api.dev.local api
10.10.0.6    db.dev.local db
10.10.0.7    cache.dev.local cache

# An extra test entry that should be ignored by the agent
# 10.10.0.8    logging.dev.local log
EOF

# Set permissions
RUN chmod 755 /home/user/qa_env && \
    chmod 644 /home/user/qa_env/test_hosts

# Clean up APT caches to keep the image lean
RUN rm -rf /var/lib/apt/lists/*