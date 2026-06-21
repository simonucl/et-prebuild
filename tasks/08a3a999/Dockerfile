FROM ubuntu:22.04

# Help section not provided, so none added

ENV PATH="/usr/local/bin:/usr/bin:/bin"

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/source_data

RUN cat > /home/user/source_data/servers.csv <<'EOF'
id,hostname,status
1,web-01,up
2,db-01,up
3,cache-01,down
EOF

RUN cat > /home/user/source_data/events.csv <<'EOF'
id,server_id,timestamp,description
101,1,2023-01-12 10:15:00,Deployment
102,3,2023-01-12 10:16:00,Cache restart
103,3,2023-01-12 11:00:00,Cache down
104,3,2023-01-12 11:05:00,Cache still down
105,2,2023-01-12 11:10:00,DB maintenance
106,1,2023-01-12 12:00:00,Deployment complete
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/source_data && \
    chmod 644 /home/user/source_data/*.csv

CMD ["bash", "-c", "exec \"$@\""]