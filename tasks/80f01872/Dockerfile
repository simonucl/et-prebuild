FROM ubuntu:22.04

# Help
# Container prepared for the SQLite/CSV migration exercise.
# Preloaded with ground-truth CSV files in /home/user/data/raw
# and pytest installed for automated pre-task checks.

ENV PYTHONIOENCODING=utf-8

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/data/raw

RUN cat <<'EOF' >/home/user/data/raw/customers.csv
id,name,email
1,Alice Smith,alice@example.com
2,Bob Jones,bob@example.com
3,Charlie Chen,charlie@example.com
4,Diana Prince,diana@example.com
5,Evan Davis,evan@example.com
EOF

RUN cat <<'EOF' >/home/user/data/raw/orders.csv
id,customer_id,product,quantity
1001,1,Keyboard,2
1002,1,Mouse,1
1003,2,Laptop,1
1004,3,Monitor,2
1005,3,USB Cable,5
1006,4,Headset,1
1007,4,Mouse Pad,3
1008,5,Webcam,1
EOF

RUN mkdir -p /home/user/work

RUN chmod -R 0777 /home/user && chmod 755 /home/user