FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/cloud_costs && \
    chmod 755 /home/user/cloud_costs

RUN cat >/home/user/cloud_costs/costs.csv <<'EOF'
service,date,cost
EC2,2023-09-01,10.50
EC2,2023-09-15,20.00
EC2,2023-08-20,5.00
RDS,2023-09-05,30.00
RDS,2023-09-20,40.00
S3,2023-09-10,50.11
S3,2023-09-11,52.11
EOF

RUN chmod 644 /home/user/cloud_costs/costs.csv

CMD sh -c "echo 'FinOps cost summarization container ready.' && echo 'Work in /home/user/cloud_costs.'"