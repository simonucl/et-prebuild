FROM ubuntu:22.04

# Install Python 3, pip, and pytest for the autograder
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Base user directory
RUN mkdir -p /home/user

# 1. Incident logs for 2024-06-15
RUN mkdir -p /home/user/incidents/2024-06-15

RUN cat > /home/user/incidents/2024-06-15/app.log <<'EOF'
2024-06-15 00:00:01 INFO  Starting application bootstrap
2024-06-15 00:00:07 ERROR Failed to connect to database
EOF

RUN cat > /home/user/incidents/2024-06-15/sys.log <<'EOF'
Jun 15 00:00:02 kernel: memory allocator initialised
Jun 15 00:00:08 kernel: stack trace follows
EOF

RUN cat > /home/user/incidents/2024-06-15/readme.txt <<'EOF'
These logs were captured automatically by the incident response tooling.
They may contain sensitive information – handle with care.
EOF

# 2. Destination directory for the archive the learner will create
RUN mkdir -p /home/user/archives && \
    chmod 0777 /home/user/archives

# Ensure all directories are world-readable so tests can access them
RUN chmod -R a+rX /home/user

# Set up the default command
CMD echo "Container built for the 2024-06-15 incident archiving exercise." && \
    echo "Use this environment to complete the task as described."