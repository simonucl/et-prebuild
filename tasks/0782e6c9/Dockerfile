FROM ubuntu:22.04

# ------------------------------------------------------------------
# Basic tools + pytest
# ------------------------------------------------------------------
RUN apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# ------------------------------------------------------------------
# Create directory hierarchy expected by the tests
# ------------------------------------------------------------------
RUN mkdir -p /home/user && \
    mkdir -p /home/user/documents && \
    touch /home/user/documents/finance_Q1_2024.csv && \
    touch /home/user/documents/finance_Q2_2024.csv && \
    chmod 0644 /home/user/documents/finance_Q1_2024.csv && \
    chmod 0644 /home/user/documents/finance_Q2_2024.csv

RUN mkdir -p /home/user/reference
RUN cat <<'EOF' > /home/user/reference/hashes.sha256
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  finance_Q1_2024.csv
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  finance_Q2_2024.csv
EOF

RUN chmod 0644 /home/user/reference/hashes.sha256

RUN mkdir -p /home/user/audit && \
    chmod 0755 /home/user/audit

# ------------------------------------------------------------------
# Permissions
# ------------------------------------------------------------------
RUN chown -R 1000:1000 /home/user/audit && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/documents && \
    chmod 0755 /home/user/reference

# ------------------------------------------------------------------
# Environment
# ------------------------------------------------------------------
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# ------------------------------------------------------------------
# Labels
# ------------------------------------------------------------------
LABEL Author="checksum-audit-task"
LABEL Description="Base image prepared for the checksum audit trail exercise."

# ------------------------------------------------------------------
# Help (as comments)
# ------------------------------------------------------------------
# This container supplies the initial file system state required for the
# “checksum audit trail” task and includes pytest for automated testing.