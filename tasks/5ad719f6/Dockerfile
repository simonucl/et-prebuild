# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install Python tooling required for the assessment environment
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Create reference input data (initial state before the student works)
# ------------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user/data/raw && \
    mkdir -p /home/user/config

# 1) Raw customer CSV -------------------------------------------------
RUN cat > /home/user/data/raw/customers.csv << 'EOF'
customer_id,full_name,email,age,country,phone
1,John Doe,jdoe@example.com,29,USA,555-1234
2,Jane Smith,,34,Canada,555-2345
3,,third@example.com,27,USA,
4,Bob Lee,blee@example.com,,USA,555-4567
5,Alice Wong,awong@example.com,31,,555-5678
EOF

# 2) Cleaning INI configuration --------------------------------------
RUN cat > /home/user/config/cleaning.ini << 'EOF'
[keep]
list = customer_id,full_name,email,age,country

[rename]
customer_id = id
full_name   = name
email       = email_address

[drop]
policy = any
EOF

# ------------------------------------------------------------------
# Ensure files are readable by the unprivileged user inside the container
# ------------------------------------------------------------------
RUN chmod 644 /home/user/data/raw/customers.csv && \
    chmod 644 /home/user/config/cleaning.ini && \
    chmod 755 /home/user

# ------------------------------------------------------------------
# Apptainer %runscript equivalent (documentation only)
# ------------------------------------------------------------------
# Apptainer container for the customer list cleaning task.
# No default action. Refer to task instructions.