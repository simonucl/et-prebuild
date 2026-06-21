FROM ubuntu:22.04

RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales \
        tzdata \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN sed -i 's/^# *en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data && \
    mkdir -p /home/user/task_logs && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/data && \
    chmod 0777 /home/user/task_logs

RUN cat > /home/user/data/raw_transactions.csv <<'EOF'
id,product,price_usd,utc_time
1,Book,12.99,2022-03-13T06:30:00Z
2,Pen,1.50,2022-11-06T05:15:00Z
3,Notebook,4.20,2022-12-01T16:00:00Z
EOF

RUN chmod 0666 /home/user/data/raw_transactions.csv && \
    chmod 755 /home/user

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

LABEL Author="Apptainer build script for transactions-cleaning task"
LABEL Description="Sets up initial directories, data file, and installs pytest for grading."