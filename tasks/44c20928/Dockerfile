FROM ubuntu:22.04

# %post
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata && \
    pip3 install --no-cache-dir pytest

RUN BASE=/home/user/storage && \
    mkdir -p ${BASE}/archive && \
    mkdir -p ${BASE}/incoming/project1 && \
    mkdir -p ${BASE}/incoming/project2 && \
    mkdir -p ${BASE}/incoming/emptydir && \
    truncate -s 56        ${BASE}/incoming/project1/keep.txt && \
    truncate -s 1572864   ${BASE}/incoming/project1/large.bak && \
    truncate -s 42        ${BASE}/incoming/project1/old.txt && \
    truncate -s 73        ${BASE}/incoming/project2/archive.txt && \
    truncate -s 1310720   ${BASE}/incoming/project2/temp2.bak && \
    touch -d "3 days ago"  ${BASE}/incoming/project1/keep.txt && \
    touch -d "2 days ago"  ${BASE}/incoming/project1/large.bak && \
    touch -d "15 days ago" ${BASE}/incoming/project1/old.txt && \
    touch -d "12 days ago" ${BASE}/incoming/project2/archive.txt && \
    touch -d "1 day ago"   ${BASE}/incoming/project2/temp2.bak && \
    chmod -R 777 /home/user

RUN chmod 755 /home/user

# %environment
ENV LC_ALL=C
ENV LANG=C.UTF-8

# %labels
LABEL Author="Container build for spring-cleaning task"
LABEL Description="Provides initial filesystem state and pytest for validation."

# %help
# This image installs pytest and prepares the exact directory
# structure required for the “spring-cleaning” exercise under
# /home/user/storage/.