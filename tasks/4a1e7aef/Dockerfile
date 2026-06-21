FROM ubuntu:22.04

# Labels
LABEL Author="backup-task-setup"
LABEL Description="Environment prepared for the backup-report exercise."

# Basic tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the verifier
RUN pip3 install --no-cache-dir "pytest>=7,<8"

# Prepare the filesystem expected by the tests
RUN mkdir -p /home/user/backups/logs

# 2023-08-01
RUN cat <<'EOF' > /home/user/backups/logs/backup_status_2023-08-01.log
host db1: SUCCESS (duration: 122s)
host db2: FAILED (error: timeout)
host db3: SUCCESS (duration: 130s)
EOF

# 2023-08-02
RUN cat <<'EOF' > /home/user/backups/logs/backup_status_2023-08-02.log
host db1: FAILED (error: disk full)
host db2: FAILED (error: timeout)
host db3: SUCCESS (duration: 128s)
EOF

# 2023-08-03
RUN cat <<'EOF' > /home/user/backups/logs/backup_status_2023-08-03.log
host db1: SUCCESS (duration: 120s)
host db2: SUCCESS (duration: 121s)
host db3: SUCCESS (duration: 125s)
EOF

# 2023-08-04
RUN cat <<'EOF' > /home/user/backups/logs/backup_status_2023-08-04.log
host db1: FAILED (error: network)
host db2: SUCCESS (duration: 118s)
host db3: FAILED (error: disk full)
EOF

# 2023-08-05
RUN cat <<'EOF' > /home/user/backups/logs/backup_status_2023-08-05.log
host db1: SUCCESS (duration: 119s)
host db2: SUCCESS (duration: 117s)
host db3: SUCCESS (duration: 124s)
EOF

# 2023-08-06
RUN cat <<'EOF' > /home/user/backups/logs/backup_status_2023-08-06.log
host db1: FAILED (error: timeout)
host db2: FAILED (error: disk full)
host db3: SUCCESS (duration: 123s)
EOF

# 2023-08-07
RUN cat <<'EOF' > /home/user/backups/logs/backup_status_2023-08-07.log
host db1: SUCCESS (duration: 118s)
host db2: SUCCESS (duration: 116s)
host db3: FAILED (error: network)
EOF

# Ensure everything is world-readable so the non-root agent can work
RUN chmod -R a+rX /home/user

# Set working directory
WORKDIR /home/user

# Default command
CMD ["echo", "Container for backup-report exercise. No default action."]