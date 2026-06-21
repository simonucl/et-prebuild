FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install --no-cache-dir pytest

ENV USER_HOME=/home/user

# Create directory tree for the dashboards
RUN mkdir -p "${USER_HOME}/projects/obs-dashboards/dashboards"

# Populate the two JSON dashboard definition files
RUN cat > "${USER_HOME}/projects/obs-dashboards/dashboards/cpu.json" <<'EOF'
{"dashboard":"cpu","version":1}
EOF

RUN cat > "${USER_HOME}/projects/obs-dashboards/dashboards/memory.json" <<'EOF'
{"dashboard":"memory","version":1}
EOF

# Create auxiliary directories where the student will write output
RUN mkdir -p "${USER_HOME}/backup_logs" && \
    mkdir -p "${USER_HOME}/backups"

# Ensure the future-write locations are writable by the unprivileged user
RUN chmod 0777 "${USER_HOME}/backup_logs" && \
    chmod 0777 "${USER_HOME}/backups"

# Read-only areas only need world-read/execute
RUN chmod -R a+rX "${USER_HOME}/projects"

# Set permissions on home directory
RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8