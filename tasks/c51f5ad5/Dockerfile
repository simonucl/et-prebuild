# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help and metadata
# Author example@example.com
# Description "Environment for filesystem-cleaning exercise with pytest installed."
LABEL Author="example@example.com" \
      Description="Environment for filesystem-cleaning exercise with pytest installed."

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN chmod 755 /home/user || true

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN set -e && \
    mkdir -p /home/user/workspace && \
    RAW_ROOT="/home/user/workspace/raw_data" && \
    mkdir -p "${RAW_ROOT}"

RUN set -e && \
    RAW_ROOT="/home/user/workspace/raw_data" && \
    cd "${RAW_ROOT}" && \
    echo "id,name,value" > customer_data_2020.csv && \
    echo "backup of customer_data_2020.csv" > customer_data_2020.csv.bak && \
    echo "id,product,price" > product_data_2021.csv && \
    echo "temporary notes" > old_notes.txt~ && \
    echo "quarterly,sales,data" > sales_Q4_2021.csv && \
    echo "# Project README" > README.md && \
    mkdir -p logs && \
    echo "2023-01-01 user login" > logs/usage.log && \
    echo "2023-01-01 error: something broke" > logs/error.log~ && \
    echo "2023-01-01 debug info" > logs/debug.log~ && \
    mkdir -p archive/old/empty_dir && \
    mkdir -p archive/zip && \
    echo "legacy,data,goes,here" > archive/old/legacy_data.csv.bak && \
    echo "placeholder text" > archive/old/placeholder.txt~ && \
    mkdir -p duplicates && \
    echo "Some notes about duplicates" > duplicates/duplicates_readme.txt

RUN chmod -R a+rwX /home/user/workspace