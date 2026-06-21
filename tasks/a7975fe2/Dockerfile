# syntax=docker/dockerfile:1
# Converted from Apptainer definition file
FROM ubuntu:22.04

# Basic Python tooling
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip python3-setuptools ca-certificates && \
    pip3 install --no-cache-dir pytest

# Prepare filesystem
RUN mkdir -p /home/user/datasets/raw

RUN printf 'a' > /home/user/datasets/raw/customers.csv
RUN printf 'x' > /home/user/datasets/raw/products.csv
RUN printf 'b' > /home/user/datasets/raw/transactions.csv

RUN cat > /home/user/datasets/reference_md5.txt <<'EOF'
0cc175b9c0f1b6a831c399e269772661  customers.csv
4a8a08f09d37b73795649038408b5f33  products.csv
92eb5ffee6ae2fec3ad71c777531578f  transactions.csv
EOF

# Permissions
RUN chmod -R a+rwX /home/user

# Environment
ENV PYTHONUNBUFFERED=1

# Additional environment commands from %environment
RUN chmod 755 /home/user

# Labels
LABEL Author="automated build for checksum-audit task"