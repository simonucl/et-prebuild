FROM ubuntu:22.04

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/logs && \
    chmod 755 /home/user && \
    chmod 755 /home/user/logs

RUN cat > /home/user/logs/system_events.csv << 'EOF'
timestamp,event,user,code
2023-03-10 12:01:05,LOGIN_SUCCESS,alice,200
2023-03-10 12:05:00,LOGIN_FAILURE,bob,403
2023-03-10 12:10:15,FILE_UPLOAD,charlie,201
2023-03-10 12:12:47,LOGIN_SUCCESS,dave,200
2023-03-10 12:15:30,FILE_DELETE,alice,204
EOF

RUN chmod 644 /home/user/logs/system_events.csv

ENV LC_ALL=C
ENV LANG=C