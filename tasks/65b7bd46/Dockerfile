# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install Python, pip, and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Create directory structure
# ------------------------------------------------------------------
RUN mkdir -p /home/user/data

# ------------------------------------------------------------------
# Populate CSV files
# ------------------------------------------------------------------
RUN cat > /home/user/data/sales_q1.csv <<'EOF'
date,product,units_sold,unit_price
2023-01-05,Widget,10,25.00
2023-02-10,Gadget,5,15.00
2023-03-15,Widget,20,25.00
2023-03-18,Doodad,7,12.50
EOF

RUN cat > /home/user/data/sales_q2.csv <<'EOF'
date,product,units_sold,unit_price
2023-04-02,Gadget,8,15.00
2023-04-10,Widget,15,25.00
2023-05-12,Doodad,10,12.50
2023-06-22,Widget,5,25.00
EOF

# ------------------------------------------------------------------
# Set permissions
# ------------------------------------------------------------------
RUN chmod 755 /home/user && \
    chmod 755 /home/user/data && \
    chmod 644 /home/user/data/sales_q1.csv /home/user/data/sales_q2.csv

# ------------------------------------------------------------------
# Environment variables
# ------------------------------------------------------------------
ENV PATH=/usr/local/bin:$PATH

# ------------------------------------------------------------------
# Help / run information (from %runscript)
# ------------------------------------------------------------------
# This container provides the initial workspace for the task.
# Required CSV data is located in /home/user/data.

CMD ["/bin/bash"]