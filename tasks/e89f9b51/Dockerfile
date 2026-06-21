FROM ubuntu:22.04

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

# Prepare the pre-populated workspace expected by the grader
RUN mkdir -p /home/user/test_env/app1 && \
    mkdir -p /home/user/test_env/app2 && \
    mkdir -p /home/user/test_env/logs/archived

# app1 files
RUN truncate -s 1200  /home/user/test_env/app1/config.yaml && \
    truncate -s 20480 /home/user/test_env/app1/data.bin && \
    truncate -s 600   /home/user/test_env/app1/readme.txt

# app2 files
RUN truncate -s 900   /home/user/test_env/app2/config.ini && \
    truncate -s 51200 /home/user/test_env/app2/core.dump && \
    truncate -s 1500  /home/user/test_env/app2/script.sh

# logs files
RUN truncate -s 30720 /home/user/test_env/logs/app1.log && \
    truncate -s 25600 /home/user/test_env/logs/app2.log && \
    truncate -s 10240 /home/user/test_env/logs/archived/old.log

# Ensure the student (non-root) user has full access
RUN chmod -R a+rwx /home/user

ENV LC_ALL=C
ENV LANG=C