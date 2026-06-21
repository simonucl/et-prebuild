# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial workspace expected by the autograder
RUN mkdir -p /home/user/projects/customer_churn/raw_data

RUN cat > /home/user/projects/customer_churn/raw_data/customers_2021.csv <<'EOF'
id,name,age,subscription
1,Alice,30,Basic
2,Bob,25,Premium
3,Charlie,35,Basic
2,Bob,25,Premium

EOF

RUN cat > /home/user/projects/customer_churn/raw_data/customers_2022.csv <<'EOF'
id,name,age,subscription
4,David,40,Premium
5,Eva,28,Basic
4,David,40,Premium
EOF

# Ensure non-root user can create directories & files
RUN chmod -R a+rX /home/user && chmod -R a+w /home/user/projects/customer_churn

# From %environment
RUN chmod 755 /home/user

ENV PATH="/root/.local/bin:${PATH}"
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8