FROM ubuntu:22.04

# Maintainer: FinOps Task Container
# Container pre-configured with cloud usage CSV files for the FinOps reporting task.
# Pytest is installed so that automated grading can run inside the container.

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/cloud_logs

RUN cat > /home/user/cloud_logs/usage_jan.csv <<'EOF'
date,service,resource,cost
2023-01-05,Compute,vm-1,10.50
2023-01-10,Storage,s3-bucket-1,2.75
2023-01-15,Compute,vm-2,7.25
EOF

RUN cat > /home/user/cloud_logs/usage_feb.csv <<'EOF'
date,service,resource,cost
2023-02-03,Compute,vm-1,9.00
2023-02-08,Storage,s3-bucket-1,2.75
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/cloud_logs && \
    chmod 644 /home/user/cloud_logs/usage_jan.csv /home/user/cloud_logs/usage_feb.csv

LABEL Maintainer="FinOps Task Container"