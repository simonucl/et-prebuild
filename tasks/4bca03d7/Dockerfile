# Author: ChatGPT – Apptainer setup for diagnostic artefacts task
FROM ubuntu:22.04

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/logs

RUN cat > /home/user/logs/webapp1.log <<'EOF'
[2023-11-04 09:15:23] INFO User login id=23
[2023-11-04 09:16:00] WARN Session delay
[2023-11-04 09:17:10] ERROR ERR101 Failed query
[2023-11-04 09:19:30] INFO Data saved
[2023-11-04 09:20:05] ERROR ERR102 Timeout calling API
EOF

RUN cat > /home/user/logs/webapp2.log <<'EOF'
[2023-11-04 09:12:00] INFO Service started
[2023-11-04 09:13:34] ERROR ERR201 Missing config
[2023-11-04 09:14:00] WARN Cache cold
[2023-11-04 09:15:45] ERROR ERR201 Missing config
[2023-11-04 09:18:50] INFO Healthcheck OK
[2023-11-04 09:19:59] ERROR ERR202 Disk full
EOF

RUN cat > /home/user/logs/dbservice.log <<'EOF'
[2023-11-04 09:10:10] INFO Connection pool created
[2023-11-04 09:11:12] ERROR ERR301 Connection refused
[2023-11-04 09:14:50] WARN Slow query detected
[2023-11-04 09:16:30] ERROR ERR301 Connection refused
[2023-11-04 09:18:00] ERROR ERR302 Deadlock found
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/logs && \
    chmod 644 /home/user/logs/*.log