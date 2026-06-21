# Maintainer: Apptainer Task Setup
# Description: Environment for query-tuning playground task with initial sample SQL files.
# Help:
# This container provides the starting environment for the “query-tuning playground” task.
# It includes:
# • /home/user/sample_queries/orders.sql
# • /home/user/sample_queries/inventory.sql
# and has pytest pre-installed for the automated validation suite.
# All work should be done under /home/user as described in the task instructions.

FROM ubuntu:22.04

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN set -eux && \
    mkdir -p /home/user/sample_queries && \
    chmod 755 /home/user && \
    chmod 755 /home/user/sample_queries

RUN set -eux && \
    printf "SELECT * FROM orders WHERE order_date > '2023-01-01';\n" > /home/user/sample_queries/orders.sql && \
    printf "SELECT * FROM inventory WHERE quantity < 10;\n" > /home/user/sample_queries/inventory.sql && \
    chmod 644 /home/user/sample_queries/orders.sql && \
    chmod 644 /home/user/sample_queries/inventory.sql

RUN set -eux && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*