# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# From %help or %labels section
# Author: symlink-cleanup-task-builder

ENV HOME=/home/user

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/projects/datasets/raw && \
    mkdir -p /home/user/projects/datasets/links

RUN printf "id,value\n1,100\n" > /home/user/projects/datasets/raw/sales_2020.csv
RUN printf "id,value\n1,200\n" > /home/user/projects/datasets/raw/sales_2021.csv
RUN printf "id,value\n1,300\n" > /home/user/projects/datasets/raw/customers_2020.csv

RUN ln -s ../raw/sales_2019.csv /home/user/projects/datasets/links/old_sales && \
    ln -s ../raw/customers_2020.csv /home/user/projects/datasets/links/cust_link

RUN chmod -R a+rwX /home/user