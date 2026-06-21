FROM ubuntu:22.04

# Base utilities & Python tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        ca-certificates \
        --no-install-recommends && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directory structure
RUN mkdir -p /home/user && \
    chmod 0777 /home/user && \
    install -d -m 0755 /home/user/serviceA/logs && \
    install -d -m 0755 /home/user/serviceB/logs

# Populate serviceA.log
RUN cat > /home/user/serviceA/logs/serviceA.log <<'EOF'
2024-04-10T10:00:00Z INFO correlation_id=abc123 Start request
2024-04-10T10:00:01Z INFO correlation_id=abc123 End request
2024-04-10T10:00:02Z INFO correlation_id=def456 Start request
2024-04-10T10:00:03Z INFO correlation_id=ghi789 Start request
2024-04-10T10:00:04Z INFO correlation_id=def456 End request
EOF

# Populate serviceB.log
RUN cat > /home/user/serviceB/logs/serviceB.log <<'EOF'
2024-04-10T10:00:00Z INFO correlation_id=abc123 Processing request
2024-04-10T10:00:01Z INFO correlation_id=abc123 Done
2024-04-10T10:00:04Z INFO correlation_id=def456 Processing request
2024-04-10T10:00:05Z INFO correlation_id=def456 Done
2024-04-10T10:00:06Z INFO correlation_id=zzz999 Unknown request
EOF

# Correct permissions and clean up
RUN chmod 0644 /home/user/serviceA/logs/serviceA.log && \
    chmod 0644 /home/user/serviceB/logs/serviceB.log && \
    rm -rf /home/user/debug && \
    chmod 755 /home/user

ENV PYTHONUNBUFFERED=1

LABEL Author="Apptainer Task Prepper"
LABEL Description="Container with initial state for correlation_id debugging exercise."
LABEL Version="1.0"