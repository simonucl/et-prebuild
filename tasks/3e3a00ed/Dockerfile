FROM ubuntu:22.04

# Help text
# This container includes curl, pytest, and the staged mock JSON payload
# at /home/user/mock_backup_api.json required for the exercise.

LABEL Author="Apptainer Task Prep"
LABEL Description="Container for the exercise 'Retrieve local backup status via curl and archive it'"

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 1777 /home/user

RUN cat > /home/user/mock_backup_api.json <<'EOF'
{
  "backup_id": "2024-06-15T08:30:00Z",
  "status": "completed",
  "duration_seconds": 125,
  "size_bytes": 10485760
}
EOF

RUN chmod 0644 /home/user/mock_backup_api.json && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH="$PATH:/usr/local/bin"