# Converted from Apptainer definition
FROM ubuntu:22.04

# Install Python and pytest
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create required directory structure
RUN mkdir -p /home/user/qa_logs

# Create sample log file via heredoc
RUN cat > /home/user/qa_logs/application.log <<'EOF'
2024-06-01 10:00:00 [INFO] Starting application
2024-06-01 10:00:01 [DEBUG] Initializing modules
2024-06-01 10:00:02 [WARN] Deprecated API used
2024-06-01 10:00:03 [INFO] Module A ready
2024-06-01 10:00:04 [ERROR] Null pointer exception
2024-06-01 10:00:05 [WARN] Low disk space
2024-06-01 10:00:06 [DEBUG] Cache cleared
2024-06-01 10:00:07 [ERROR] Out of memory
2024-06-01 10:00:08 [INFO] Shutdown requested
2024-06-01 10:00:09 [WARN] Configuration file missing
EOF

# Permissions
RUN chmod 777 /home/user/qa_logs && \
    chmod 644 /home/user/qa_logs/application.log

# Create user (UID/GID 1000)
RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -d /home/user -s /bin/bash -u 1000 user; \
    fi && \
    chown -R user:user /home/user

# Environment variables and permissions
ENV PATH=/usr/local/bin:/usr/bin:/bin

RUN chmod 755 /home/user

# Labels
LABEL author="container-builder"
LABEL description="Environment for QA log-triage exercise with pytest pre-installed"