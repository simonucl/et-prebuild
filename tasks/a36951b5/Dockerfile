# Author: backup-task-preparer
# Description: Ubuntu 22.04 container with initial state for the database backup assignment.

FROM ubuntu:22.04

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN id -u user >/dev/null 2>&1 || useradd -m -u 1000 -U -s /bin/bash user

RUN mkdir -p /home/user/db_dumps && \
    mkdir -p /home/user/backups

RUN printf 'CREATE TABLE customers(id INT, name TEXT);\n'  > /home/user/db_dumps/customers.sql && \
    printf 'CREATE TABLE orders(id INT,  total NUMERIC);\n' > /home/user/db_dumps/orders.sql && \
    printf 'CREATE TABLE products(id INT, price NUMERIC);\n' > /home/user/db_dumps/products.sql

RUN chown -R user:user /home/user && \
    chmod 755 /home/user && \
    chmod 755 /home/user/db_dumps && \
    chmod 755 /home/user/backups