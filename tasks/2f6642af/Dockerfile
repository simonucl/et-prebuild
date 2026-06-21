FROM ubuntu:22.04

# Help / labels from %labels
LABEL Author="backup-task-setup"
LABEL Description="Initial state for deterministic backup task – includes production_data and pytest."

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        gzip \
        tar \
        coreutils && \
    pip3 install --no-cache-dir pytest

RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 user

RUN install -d -o user -g user /home/user/production_data

RUN cat << 'EOF' > /home/user/production_data/customers.csv
id,name,email
1,Alice,alice@example.com
2,Bob,bob@example.com
3,Charlie,charlie@example.com
EOF

RUN cat << 'EOF' > /home/user/production_data/orders.csv
order_id,customer_id,product,quantity
1001,1,Keyboard,2
1002,2,Mouse,1
1003,3,Monitor,1
EOF

RUN cat << 'EOF' > /home/user/production_data/README.md
# Production Data
This directory contains the CSV exports used by the sales team.
EOF

RUN chown -R user:user /home/user/production_data && \
    chmod 644 /home/user/production_data/*

RUN chmod 755 /home/user