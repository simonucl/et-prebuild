# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update package list and install Python + pip
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare the initial filesystem state expected by the exercise
# ------------------------------------------------------------------

# Create required directories
RUN mkdir -p /home/user/projects/data_cleaning/raw_datasets && \
    mkdir -p /home/user/archive

# Populate CSV files with the specified contents
RUN cat > /home/user/projects/data_cleaning/raw_datasets/sales_q1.csv <<'EOF'
id,amount
1,100
EOF

RUN cat > /home/user/projects/data_cleaning/raw_datasets/sales_q2.csv <<'EOF'
id,amount
2,200
EOF

RUN cat > /home/user/projects/data_cleaning/raw_datasets/customers.csv <<'EOF'
id,name
1,Alice
2,Bob
EOF

# Ensure everything is writable by the non-root runtime user
RUN chmod -R a+rwX /home/user && \
    chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8