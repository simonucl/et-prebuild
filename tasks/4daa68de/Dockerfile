FROM ubuntu:22.04

# Help section (none provided in source)

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    if ! id -u user >/dev/null 2>&1; then useradd -m -d /home/user -s /bin/bash user; fi && \
    mkdir -p /home/user/data

RUN cat << 'EOF' > /home/user/data/sales_q1.csv
id,value
1,100
2,200
3,300
EOF

RUN cat << 'EOF' > /home/user/data/sales_q2.csv
id,value
1,400
2,500
EOF

RUN cat << 'EOF' > /home/user/data/sales_q3.csv
id,value
1,600
2,700
3,800
4,900
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/data && \
    chmod 644 /home/user/data/sales_q1.csv /home/user/data/sales_q2.csv /home/user/data/sales_q3.csv