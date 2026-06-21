FROM ubuntu:22.04

# Basic tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state
RUN mkdir -p /home/user/builds/logs

# Log: 2024-06-01
RUN cat >/home/user/builds/logs/build_2024-06-01.log <<'EOF'
[2024-06-01 08:00:01] INFO Build started
[2024-06-01 08:00:05] WARN Deprecated API used
[2024-06-01 08:00:10] INFO Compiling module A
[2024-06-01 08:00:20] ERROR Failed to compile module A: missing header
[2024-06-01 08:00:30] INFO Retrying
[2024-06-01 08:00:40] INFO Compiled module A
[2024-06-01 08:01:00] INFO Build finished
EOF

# Log: 2024-06-02
RUN cat >/home/user/builds/logs/build_2024-06-02.log <<'EOF'
[2024-06-02 08:00:01] INFO Build started
[2024-06-02 08:00:05] INFO Loading cache
[2024-06-02 08:00:06] WARN Cache miss for module B
[2024-06-02 08:00:08] INFO Compiling module B
[2024-06-02 08:00:18] INFO Compiled module B
[2024-06-02 08:00:20] INFO Build finished
EOF

# Log: 2024-06-03
RUN cat >/home/user/builds/logs/build_2024-06-03.log <<'EOF'
[2024-06-03 08:00:01] INFO Build started
[2024-06-03 08:00:03] INFO Loading cache
[2024-06-03 08:00:05] INFO Compiling module C
[2024-06-03 08:00:15] ERROR Failed to compile module C: syntax error
[2024-06-03 08:00:25] ERROR Failed to compile module C: unresolved reference
[2024-06-03 08:00:40] WARN Low disk space
[2024-06-03 08:01:00] INFO Aborting build
EOF

# Permissions
RUN chmod -R a+r /home/user/builds/logs && \
    mkdir -p /home/user/builds/reports && \
    chmod -R a+rwx /home/user/builds/reports && \
    chmod 755 /home/user

# Environment variables
ENV PYTHONUNBUFFERED=1

# Labels
LABEL Author="build-engineer"
LABEL Description="Initial state for the build-logs exercise with pytest pre-installed."