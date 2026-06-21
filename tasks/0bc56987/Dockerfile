FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y git python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/etl-pipeline && \
    cd /home/user/etl-pipeline && \
    git config --global init.defaultBranch main && \
    git config --global user.email "builder@example.com" && \
    git config --global user.name "Builder" && \
    git init && \
    printf 'ETL Pipeline\n\n' > README.md && \
    git add README.md && \
    git commit -m "Initial commit" && \
    chmod -R a+rwX /home/user/etl-pipeline

RUN chmod 755 /home/user

LABEL Author="CI Setup"