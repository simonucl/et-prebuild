FROM ubuntu:22.04

# Help:
# This container provides the initial filesystem state and tools
# required for the “cloud migration” awk/sed summarization task.
# Key locations:
#   /home/user/cloud_migration/logs/*.log – Input data for the exercise

LABEL Author="example-builder"
LABEL Description="Environment for cloud-migration log summarization exercise"

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 python3-pip \
        ca-certificates gnupg dirmngr && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    install -d -m 0755 /home/user/cloud_migration/logs

RUN cat > /home/user/cloud_migration/logs/2023-10-01.log <<'EOF'
2023-10-01T12:00:00Z serviceA MIGRATE START
2023-10-01T12:05:00Z serviceA MIGRATE SUCCESS
2023-10-01T13:00:00Z serviceB MIGRATE START
2023-10-01T13:03:00Z serviceB MIGRATE FAIL Error: Disk quota exceeded
2023-10-01T14:00:00Z serviceC MIGRATE START
2023-10-01T14:04:00Z serviceC MIGRATE SUCCESS
EOF

RUN cat > /home/user/cloud_migration/logs/2023-10-02.log <<'EOF'
2023-10-02T09:00:00Z serviceA MIGRATE START
2023-10-02T09:04:30Z serviceA MIGRATE SUCCESS
2023-10-02T10:00:10Z serviceB MIGRATE START
2023-10-02T10:05:00Z serviceB MIGRATE FAIL Error: Network unreachable
2023-10-02T11:00:00Z serviceC MIGRATE START
2023-10-02T11:05:40Z serviceC MIGRATE SUCCESS
EOF

RUN cat > /home/user/cloud_migration/logs/2023-10-03.log <<'EOF'
2023-10-03T15:00:00Z serviceA MIGRATE START
2023-10-03T15:07:00Z serviceA MIGRATE SUCCESS
2023-10-03T16:00:00Z serviceB MIGRATE START
2023-10-03T16:09:15Z serviceB MIGRATE SUCCESS
2023-10-03T17:00:00Z serviceC MIGRATE START
2023-10-03T17:08:50Z serviceC MIGRATE FAIL Error: Timeout contacting datastore
EOF

RUN chmod 0644 /home/user/cloud_migration/logs/*.log
RUN chmod 755 /home/user