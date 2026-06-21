# Help: This image sets up the initial environment for the Capacity Planner task.
# Includes:
# - /home/user/capacity_planner with pre-populated files
# - Python 3 with pytest installed

FROM ubuntu:22.04

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/capacity_planner

RUN cat > /home/user/capacity_planner/usage.csv << 'EOF'
service,port,avg_cpu,avg_mem_MB,avg_network_Mbps
http,80,25,512,120
https,443,30,600,150
ssh,22,5,100,5
postgres,5432,10,800,30
redis,6379,8,200,20
prometheus,9090,15,300,40
EOF

RUN cat > /home/user/capacity_planner/baseline_firewall.rules << 'EOF'
-A INPUT -p tcp --dport 22 -j ACCEPT
-A INPUT -p tcp --dport 80 -j ACCEPT
-A INPUT -p tcp --dport 443 -j ACCEPT
-A INPUT -j DROP
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/capacity_planner && \
    chmod 644 /home/user/capacity_planner/usage.csv && \
    chmod 644 /home/user/capacity_planner/baseline_firewall.rules && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

CMD echo "Container for the Capacity Planner task." && \
    echo "Run 'pytest' inside the container to execute the test suite."