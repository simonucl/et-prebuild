FROM ubuntu:22.04

# Install Python tooling
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Create filesystem state
RUN mkdir -p /home/user && chmod 0777 /home/user
RUN mkdir -p /home/user/app/logs

RUN cat <<'EOF' > /home/user/app/VERSION
v2.5.1-beta
EOF

RUN cat <<'EOF' > /home/user/app/logs/app01.log
2023-04-01T12:00:00Z INFO Application started
2023-04-01T12:00:05Z ERROR Failed to read config
2023-04-01T12:00:06Z INFO Retrying
EOF

RUN cat <<'EOF' > /home/user/app/logs/app02.log
2023-04-01T12:05:00Z INFO Task begin
2023-04-01T12:05:10Z INFO Task complete
EOF

RUN cat <<'EOF' > /home/user/app/logs/app03.log
2023-04-01T12:10:00Z DEBUG Verbose output
2023-04-01T12:10:01Z ERROR Connection lost
2023-04-01T12:10:02Z DEBUG Reconnecting
2023-04-01T12:10:03Z INFO Connection re-established
EOF

RUN chmod -R a+rX /home/user/app && \
    chmod 0644 /home/user/app/VERSION /home/user/app/logs/*.log

RUN chmod 755 /home/user

CMD echo "Container for Support Diagnostics task. No default runtime action."