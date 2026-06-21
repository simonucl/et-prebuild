# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ---------------------------------------------------------------------
# Update package list and install Python 3, pip and pytest
# ---------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# ---------------------------------------------------------------------
# Create a regular user 'user' with UID 1000
# ---------------------------------------------------------------------
RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user

# ---------------------------------------------------------------------
# Set up the raw dataset directory and populate the CSV file
# ---------------------------------------------------------------------
RUN mkdir -p /home/user/datasets/raw

RUN cat <<'EOF' > /home/user/datasets/raw/sales_2023.csv
OrderID,Date,Product,Quantity,UnitPrice,CustomerEmail
1001,01/03/2023,Widget A,4,25.50,alice@example.com
1002,02/15/2023,Widget B,,30.00,bob@example.com
1003,03/22/2023,Widget C,2,,"charlie@example.com"
1004,04/10/2023,Widget A,1,25.50,dana@example.com
1005,05/18/2023,Widget D,3,40.00,erin@example.com
1006,06/30/2023,Widget B,5,30.00,frank@example.com
1007,07/12/2023,Widget A,2,25.50,grace@example.com
1008,08/25/2023,Widget E,7,55.00,harry@example.com
EOF

# ---------------------------------------------------------------------
# Ensure ownership and permissions
# ---------------------------------------------------------------------
RUN chown -R 1000:1000 /home/user && \
    chmod -R a+rwX /home/user

# ---------------------------------------------------------------------
# Clean up apt caches
# ---------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------
# Environment setup
# ---------------------------------------------------------------------
RUN chmod 755 /home/user
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# ---------------------------------------------------------------------
# Default command (equivalent to Apptainer runscript)
# ---------------------------------------------------------------------
CMD echo "Apptainer container for the sales-data cleaning exercise."