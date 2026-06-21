FROM ubuntu:22.04

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -qq && \
    apt-get install -y --no-install-recommends python3 python3-pip tar gzip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/finops/raw_cost_data

RUN cat > /home/user/finops/raw_cost_data/january.csv <<'EOF'
Date,Cost
Compute,23.45
Storage,12.00
EOF

RUN cat > /home/user/finops/raw_cost_data/february.csv <<'EOF'
Date,Cost
Compute,25.10
Storage,11.50
EOF

RUN chmod 755 /home /home/user || true && \
    chmod -R 755 /home/user/finops

# Author FinOps Backup Exercise