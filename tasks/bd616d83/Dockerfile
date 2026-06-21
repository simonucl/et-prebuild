# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Base utilities and Python tooling
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        coreutils && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create required directory structure
RUN mkdir -p /home/user/raw_logs && \
    mkdir -p /home/user/reports

# Populate source log files
RUN cat > /home/user/raw_logs/active_connections.tsv <<'EOF'
HOSTNAME	IP	PORT	STATE	PID
web01	10.0.0.1	80	ESTABLISHED	2345
db01	10.0.0.2	5432	ESTABLISHED	5432
cache01	10.0.0.3	6379	LISTEN	3333
EOF

RUN cat > /home/user/raw_logs/cpu_load.tsv <<'EOF'
HOSTNAME	1min	5min	15min
web01	0.10	0.12	0.15
db01	0.55	0.53	0.50
cache01	0.20	0.25	0.30
EOF

# Permissions setup
RUN chmod -R a+rwx /home/user && chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Help section
# Container for the “connection load summary” exercise.
# Pre-populated with:
#   /home/user/raw_logs/active_connections.tsv
#   /home/user/raw_logs/cpu_load.tsv
# The /home/user/reports directory is empty (writable) for learner output.
# Pytest is installed for automated grading tests.