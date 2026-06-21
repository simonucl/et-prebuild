FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

# Create /home/user/logs/ with the correct permissions
RUN mkdir -p /home/user/logs && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/logs

# Populate /home/user/logs/webserver.log with the exact contents
RUN cat >/home/user/logs/webserver.log <<'EOF'
2024-04-12T10:14:01Z server1.example.com status=UP   response_ms=101
2024-04-12T10:15:32Z server1.example.com status=DOWN response_ms=0
2024-04-12T10:16:45Z server2.example.com status=UP   response_ms=95
2024-04-12T10:17:02Z server2.example.com status=DOWN response_ms=0
2024-04-12T10:18:01Z server1.example.com status=UP   response_ms=103
2024-04-12T10:19:20Z server1.example.com status=DOWN response_ms=0
2024-04-12T10:20:45Z server2.example.com status=UP   response_ms=96
2024-04-12T10:21:11Z server3.example.com status=DOWN response_ms=0
EOF

RUN chmod 0644 /home/user/logs/webserver.log

# Ensure /home/user/reports/ does NOT exist yet
RUN rm -rf /home/user/reports