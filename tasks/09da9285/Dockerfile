FROM ubuntu:22.04

# Labels
LABEL Author="ChatGPT"
LABEL Description="Container for diagnostic bundle exercise – provides initial log and config files and includes pytest for automated grading."

# Post section
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/app_logs

RUN cat > /home/user/app_logs/app.log <<'EOF'
2023-03-01 10:00:00 INFO Service started
2023-03-01 10:05:00 WARN Cache miss
2023-03-01 10:10:00 ERROR Connection timeout
2023-03-01 10:15:00 INFO Retrying...
2023-03-01 10:20:00 INFO Connected
2023-03-01 10:25:00 INFO Health check OK
2023-03-01 10:30:00 WARN Slow response
2023-03-01 10:35:00 INFO Cleanup initiated
2023-03-01 10:40:00 INFO Cleanup finished
2023-03-01 10:45:00 INFO Service running
EOF

RUN cat > /home/user/app_logs/config.ini <<'EOF'
[general]
version = 2.4.7
maintainer = ops-team
EOF

RUN chmod -R a+rX /home/user && chmod a+w /home/user && chmod 755 /home/user

# Environment section
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"