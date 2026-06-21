# Author: csv-disk-usage-prep
# Description: Environment for the CSV disk-usage summary task with initial data and pytest installed.

FROM ubuntu:22.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN useradd -m -u 1000 user

RUN mkdir -p /home/user/data/csv && \
    cd /home/user/data/csv && \
    truncate -s 1250 customers.csv && \
    truncate -s 2750 orders.csv && \
    truncate -s 500 returns.csv && \
    chmod 0644 customers.csv orders.csv returns.csv && \
    chmod 0755 /home/user /home/user/data /home/user/data/csv

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

CMD echo "This container is prepared for the 'CSV disk-usage summary' task." && \
    echo "Switch to the working directory and begin your analysis as needed."