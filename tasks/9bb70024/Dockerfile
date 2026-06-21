FROM ubuntu:22.04

# Help:
# This container sets up the initial state for the “FinOps CSV processing” task.
# It includes:
#   - /home/user/cloud_usage with the two required source CSV files.
#   - pytest pre-installed for automated grading.

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user

RUN mkdir -p /home/user/cloud_usage

RUN cat > /home/user/cloud_usage/raw_usage.csv <<'EOF'
Service,ResourceID,UsageHours,CostUSD,Region
Compute,i-031,120,48.00,us-east-1
Storage,vol-22,720,36.00,us-east-1
Database,db-67,100,120.00,eu-west-1
Compute,i-099,50,20.00,us-east-1
Analytics,athena-1,30,15.00,us-west-2
EOF

RUN cat > /home/user/cloud_usage/pricing_adjustments.csv <<'EOF'
Service,DiscountPercent
Compute,10
Storage,5
Database,15
Analytics,20
EOF

RUN chown -R user:user /home/user && \
    chmod 755 /home/user && \
    chmod 755 /home/user/cloud_usage && \
    chmod 644 /home/user/cloud_usage/*.csv

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

CMD ["/bin/bash"]