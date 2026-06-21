FROM ubuntu:22.04

# Basic tooling
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial exercise state under /home/user
RUN mkdir -p /home/user/data && \
    mkdir -p /home/user/output && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/data && \
    chmod 0755 /home/user/output

# Populate the sample CSV file
RUN cat > /home/user/data/quarterly_sales.csv <<'EOF'
region,quarter,profit
north,1,23500
south,1,19800
east,1,17500
west,1,16000
north,2,24000
south,2,21000
east,2,18000
west,2,16500
EOF

RUN chmod 0644 /home/user/data/quarterly_sales.csv

# Clean up APT caches to keep the image small
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/user

CMD ["/bin/bash"]