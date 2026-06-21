# Author: Observability-Setup
# Description: Container with initial logs for observability assignment

FROM ubuntu:22.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        ca-certificates \
        gnupg \
        curl && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/logs

RUN cat <<'EOF' > /home/user/logs/log_serverA.log
2023-10-23T08:00:00Z serverA /api/auth 200 120
2023-10-23T08:00:01Z serverA /api/items 500 34
2023-10-23T08:00:02Z serverA /api/items 200 56
2023-10-23T08:00:03Z serverA /api/cart 502 89
2023-10-23T08:00:04Z serverA /api/cart 200 90
2023-10-23T08:00:05Z serverA /api/cart 200 95
2023-10-23T08:00:06Z serverA /api/auth 503 45
2023-10-23T08:00:07Z serverA /api/auth 200 110
2023-10-23T08:00:08Z serverA /api/items 200 60
2023-10-23T08:00:09Z serverA /api/items 504 40
EOF

RUN cat <<'EOF' > /home/user/logs/log_serverB.log
2023-10-23T08:00:00Z serverB /api/auth 200 100
2023-10-23T08:00:01Z serverB /api/items 200 70
2023-10-23T08:00:02Z serverB /api/items 500 30
2023-10-23T08:00:03Z serverB /api/cart 200 85
2023-10-23T08:00:04Z serverB /api/cart 504 90
2023-10-23T08:00:05Z serverB /api/cart 200 80
2023-10-23T08:00:06Z serverB /api/auth 502 55
2023-10-23T08:00:07Z serverB /api/auth 200 95
2023-10-23T08:00:08Z serverB /api/items 200 65
2023-10-23T08:00:09Z serverB /api/items 200 68
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/logs && \
    chmod 644 /home/user/logs/log_serverA.log /home/user/logs/log_serverB.log