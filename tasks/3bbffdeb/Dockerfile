# Converted from Apptainer definition file
FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure user exists
RUN if ! id -u user >/dev/null 2>&1; then useradd -m -d /home/user -s /bin/bash user; fi

# Set permissions for home directories
RUN chmod 755 /home && chmod 755 /home/user

# Create dataset directory
RUN mkdir -p /home/user/data && chmod 755 /home/user/data

# Create CSV file via heredoc
RUN cat >/home/user/data/sales.csv <<'EOF'
Date,Region,Product,Quantity,Price,Revenue
2023-01-01,North,Widget,10,2.50,25.00
2023-01-02,South,Gadget,5,5.00,25.00
2023-01-03,East,Widget,7,2.50,17.50
2023-01-04,West,Doohickey,2,12.00,24.00
2023-01-05,North,Gadget,1,5.00,5.00
EOF

# Set CSV permissions
RUN chmod 644 /home/user/data/sales.csv

# Environment variables
ENV LC_ALL=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1