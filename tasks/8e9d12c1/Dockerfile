# Derived from localimage ./ubuntu_22.04.sif
FROM ubuntu:22.04

RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/backups/daily

RUN cat <<'EOF' > /home/user/backups/manifest.size
56 users.bak
59 inventory.bak
80 orders.bak
EOF

RUN cat <<'EOF' > /home/user/backups/daily/users.bak
USERS BACKUP 2023-01-01
ID,NAME
1,John Doe
2,Jane Smith
EOF

RUN cat <<'EOF' > /home/user/backups/daily/inventory.bak
INVENTORY BACKUP 2023-01-01
SKU,COUNT
ABC123,100
XYZ789,50
EOF

RUN cat <<'EOF' > /home/user/backups/daily/orders.bak
ORDERS BACKUP 2023-01-01
ORDER_ID,USER_ID,SKU,AMOUNT
1001,1,ABC123,2
1002,2,XYZ789,1
EOF

RUN chmod -R a+rwX /home/user && chmod 755 /home/user