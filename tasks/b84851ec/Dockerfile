# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# %post
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/etl/input

RUN cat <<'CSV' > /home/user/etl/input/sales_data.csv
order_id,customer_id,date,product,quantity,unit_price
1001,501,2020-11-10,Laptop,2,799.99
1002,502,2021-01-05,Mouse,5,25.50
1003,503,2021-03-16,Keyboard,3,45.00
1004,504,2020-07-23,Monitor,1,189.99
1005,505,2021-12-30,Laptop,1,749.99
CSV

RUN chmod -R a+rX /home/user && \
    chmod -R a+w /home/user/etl && \
    chmod 755 /home/user

# %environment
ENV PATH="/usr/local/bin:${PATH}"

# %labels
LABEL Author="container-builder"
LABEL Description="Workspace for miniature ETL shell exercise; pytest pre-installed."

CMD echo "ETL exercise container. Start your work in /home/user." && /bin/bash