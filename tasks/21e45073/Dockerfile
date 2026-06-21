FROM ubuntu:22.04

# Install Python and pytest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare directory structure
RUN mkdir -p /home/user/logs

# Create the egress_traffic.csv file
RUN cat << 'EOF' > /home/user/logs/egress_traffic.csv
timestamp,src_ip,dst_ip,bytes_out
2024-05-01T10:00:00Z,10.0.0.5,34.102.120.1,2048
2024-05-01T10:01:00Z,10.0.0.5,44.12.31.5,10240
2024-05-01T10:02:00Z,10.0.0.20,34.102.120.1,4096
2024-05-01T10:03:00Z,10.0.0.20,172.217.3.110,5120
2024-05-01T10:04:00Z,10.0.0.7,44.12.31.5,8192
2024-05-01T10:05:00Z,10.0.0.7,34.102.120.1,1024
2024-05-01T10:06:00Z,10.0.0.7,172.217.3.110,10000
2024-05-01T10:07:00Z,10.0.0.5,34.102.120.1,3072
2024-05-01T10:08:00Z,10.0.0.20,44.12.31.5,2048
2024-05-01T10:09:00Z,10.0.0.5,34.102.120.1,5120
EOF

# Set permissions
RUN chmod 644 /home/user/logs/egress_traffic.csv && \
    chmod 755 /home/user && \
    chmod 755 /home/user/logs

# Ensure finops output directory is not present
RUN if [ -d /home/user/finops_firewall ]; then rm -rf /home/user/finops_firewall; fi

LABEL Author="OpenAI ChatGPT"
LABEL Description="Ubuntu 22.04 container for FinOps egress analysis task with pytest pre-installed."