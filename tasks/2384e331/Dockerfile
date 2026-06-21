FROM ubuntu:22.04

# Help / metadata
LABEL Author="Apptainer Task Generator"
LABEL Description="Container providing initial log file and environment for release-manager task"

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Post section
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/project

RUN cat > /home/user/project/release-2024-04-15.log <<'EOF'
2024-04-15T08:00:01Z INFO  app-01 Starting deployment
2024-04-15T08:00:05Z ERROR app-01 Failed to fetch artifact
2024-04-15T08:00:10Z WARN  app-02 Slow response from repository
2024-04-15T08:00:12Z ERROR app-02 Missing environment variable
2024-04-15T08:00:15Z INFO  app-03 Deployment completed
2024-04-15T08:00:18Z ERROR app-03 Timeout contacting service
2024-04-15T08:00:20Z ERROR app-02 Port already in use
2024-04-15T08:00:25Z INFO  app-01 Rollback initiated
EOF

RUN chmod 0644 /home/user/project/release-2024-04-15.log && \
    chmod -R a+rX /home/user && \
    chmod 755 /home/user