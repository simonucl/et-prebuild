FROM ubuntu:22.04

# Labels
LABEL Author="ChatGPT"
LABEL Description="Starting container for the daily revenue report assignment"

# Install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        cron \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest (for the grader)
RUN pip3 install --no-cache-dir pytest

# Prepare directory structure for the assignment
RUN mkdir -p /home/user/data/raw_sales && \
    mkdir -p /home/user/data/summaries && \
    mkdir -p /home/user/scripts && \
    mkdir -p /home/user/logs

# Create the three raw CSV input files with exact contents
RUN cat > /home/user/data/raw_sales/sales_2023-03-01.csv <<'CSV1'
date,product,units,unit_price
2023-03-01,Widget,10,25.50
2023-03-01,Gadget,5,40.00
CSV1

RUN cat > /home/user/data/raw_sales/sales_2023-03-02.csv <<'CSV2'
date,product,units,unit_price
2023-03-02,Widget,8,25.50
2023-03-02,Thingamajig,3,60.00
CSV2

RUN cat > /home/user/data/raw_sales/sales_2023-03-03.csv <<'CSV3'
date,product,units,unit_price
2023-03-03,Gadget,7,40.00
2023-03-03,Thingamajig,2,60.00
CSV3

# Set safe permissions: directories 755, files 644
RUN find /home/user -type d -exec chmod 755 {} + && \
    find /home/user -type f -exec chmod 644 {} +

# Environment setup
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Set working directory
WORKDIR /home/user