# From local image reference; converted to base Ubuntu 22.04
FROM ubuntu:22.04

# Install Python tooling and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/data

# Q1 data
RUN cat <<'EOF' > /home/user/data/raw_sales_2023_Q1.csv
product,quantity,price
Laptop,10,1200
Phone,25,800
Tablet,14,600
EOF

# Q2 data
RUN cat <<'EOF' > /home/user/data/raw_sales_2023_Q2.csv
product,quantity,price
Laptop,8,1150
Phone,30,780
Headphones,40,150
EOF

# Permissions
RUN chmod -R 0755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Mirroring the environment chmod (executed at runtime in Apptainer)
ENV HOME=/home/user

# Runscript equivalent
CMD echo "Apptainer container for the sales aggregation exercise."