# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from %labels
LABEL Author="Apptainer Setup Script"
LABEL Description="Container with initial state for quarterly CSV staging-area task."

# Basic tooling and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state for the “quarterly CSV” exercise
RUN set -eux && \
    mkdir -p /home/user

# Create directory hierarchy
RUN set -eux && \
    BASE_DIR=/home/user/data && \
    ORIG_DIR=${BASE_DIR}/original && \
    CURR_DIR=${BASE_DIR}/current && \
    mkdir -p "${ORIG_DIR}" "${CURR_DIR}"

# Populate ORIGINAL_DIR with the required CSV files
RUN set -eux && \
    BASE_DIR=/home/user/data && \
    ORIG_DIR=${BASE_DIR}/original && \
    cat > "${ORIG_DIR}/inventory_2023_Q1.csv" <<'EOF'
month,units,value
Jan,45,720
EOF

RUN set -eux && \
    BASE_DIR=/home/user/data && \
    ORIG_DIR=${BASE_DIR}/original && \
    cat > "${ORIG_DIR}/marketing_2023_Q1.csv" <<'EOF'
channel,impressions,spend
Social,12000,350
EOF

RUN set -eux && \
    BASE_DIR=/home/user/data && \
    ORIG_DIR=${BASE_DIR}/original && \
    cat > "${ORIG_DIR}/sales_2023_Q1.csv" <<'EOF'
month,units,revenue
Jan,100,1200
Feb,130,1500
EOF

RUN set -eux && \
    BASE_DIR=/home/user/data && \
    ORIG_DIR=${BASE_DIR}/original && \
    cat > "${ORIG_DIR}/sales_2022_Q4.csv" <<'EOF'
month,units,revenue
Dec,90,1100
EOF

# Create the single outdated symlink inside CURRENT_DIR
RUN set -eux && \
    ln -s ../original/sales_2022_Q4.csv /home/user/data/current/sales_latest.csv

# Make everything under /home/user writable so the unprivileged runtime user can modify the staging area.
RUN set -eux && \
    chmod -R a+rwX /home/user

# Environment variables from %environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Ensure permissions as specified in %environment
RUN chmod 755 /home/user

# Help text from %help (converted to comments)
# Container with initial state for quarterly CSV staging-area task.