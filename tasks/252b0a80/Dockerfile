FROM ubuntu:22.04

# Install Python, pip, and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        --no-install-recommends && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare filesystem
RUN mkdir -p /home/user && chmod 0777 /home/user
RUN mkdir -p /home/user/data && chmod 0755 /home/user/data

RUN cat > /home/user/data/sales.csv << 'EOF'
order_id,region,amount
1,North,1200
2,South,850
3,East,990
4,West,640
5,North,1330
6,South,720
7,East,560
8,West,410
9,North,1500
EOF

RUN chmod 0644 /home/user/data/sales.csv
RUN rm -f /home/user/process_log.txt

LABEL Author="example"
LABEL Version="v1.0"
LABEL Description="Base image for Unix process-management assignment."

ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8