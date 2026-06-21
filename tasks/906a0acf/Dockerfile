FROM ubuntu:22.04

# Labels
LABEL Author="build-script"
LABEL Description="Environment for log-processing DevOps task with pytest pre-installed."

# Update APT and install Python/pip
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        gzip \
        ca-certificates && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# Prepare directory tree
RUN mkdir -p /home/user/app/logs/archived && \
    mkdir -p /home/user/app/debug && \
    chmod 0777 /home/user/app/debug

# Create uncompressed *.log files
RUN cat > /home/user/app/logs/service-a_2024-03-25.log << 'EOF'
2024-03-25 10:02:15 INFO  Starting service
2024-03-25 10:15:02 ERROR Connection timeout
2024-03-25 10:18:47 WARN  Retrying
2024-03-25 11:07:11 ERROR Failed to reconnect
EOF

RUN cat > /home/user/app/logs/service-b_2024-03-24.log << 'EOF'
2024-03-24 09:45:00 INFO  Scheduled task
2024-03-24 09:46:21 INFO  Task running
2024-03-24 09:47:33 ERROR Task failed
EOF

RUN cat > /home/user/app/logs/service-a_2024-03-14.log << 'EOF'
2024-03-14 13:01:09 INFO  Old record
2024-03-14 13:05:17 WARN  Still fine
2024-03-14 13:06:45 ERROR Historical issue
EOF

# Create auxiliary files
RUN echo "This directory stores application log files." > /home/user/app/logs/readme.txt

RUN echo "Archived log – not relevant for current diagnostics." | \
    gzip -c > /home/user/app/logs/archived/archived_2024-03-20.log.gz

# Final permissions
RUN chmod -R a+r /home/user && \
    find /home/user -type d -exec chmod a+x {} + && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

WORKDIR /home/user

CMD ["bash", "-l"]