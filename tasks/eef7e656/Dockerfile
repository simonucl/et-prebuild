FROM ubuntu:22.04

# Labels
LABEL Maintainer="task-prep"
LABEL Description="Initial filesystem and tooling for syslog log-filter exercise"

# Refresh apt and install Python tooling
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates

# Install pytest so the grader can run its suites
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# Create the required directory structure
RUN mkdir -p /home/user/logs && \
    chmod 0777 /home/user/logs

# Populate syslog_sample.log with the exact fixture lines
RUN cat > /home/user/logs/syslog_sample.log <<'EOF'
2023-08-25 10:02:15 server1 sshd[1234]: INFO User root logged in
2023-08-25 10:03:10 server1 sshd[1234]: WARN Failed password attempt for user dev
2023-08-25 10:05:42 server1 app[5678]: ERROR Could not connect to database [code=DBCONN01]
2023-08-25 10:06:00 server1 kernel: INFO CPU temperature normal
2023-08-25 10:07:18 server1 app[5678]: ERROR Timeout while reading socket [code=SOCKTIME02]
2023-08-25 10:08:22 server1 app[5678]: WARN Deprecated API usage detected
2023-08-25 10:09:30 server1 backup[9012]: INFO Backup completed successfully
EOF

# Set correct permissions and clean up any artefact files
RUN chmod 0644 /home/user/logs/syslog_sample.log && \
    chmod 755 /home/user && \
    rm -f /home/user/logs/filtered_syslog.log /home/user/logs/summary.log || true

# Environment variables
ENV PATH="${HOME}/.local/bin:${PATH}"

WORKDIR /home/user

# Default command
CMD ["/bin/bash"]