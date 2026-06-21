FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /home/user/incidents

RUN cat >/home/user/incidents/failed_attempts.csv <<'EOF'
SessionID,IP
1001,192.0.2.10
1002,203.0.113.55
1003,198.51.100.30
1004,203.0.113.77
1005,198.51.100.88
EOF

RUN cat >/home/user/incidents/successful_attempts.csv <<'EOF'
SessionID,IP
1001,198.51.100.23
1002,198.51.100.24
1003,203.0.113.60
1004,192.0.2.44
1005,203.0.113.90
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/incidents && \
    chmod 644 /home/user/incidents/*.csv

ENV PATH=/usr/local/bin:$PATH
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

CMD echo "Container for incident response exercise.  Use it as instructed."