FROM ubuntu:22.04

# Basic tools + pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip coreutils && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directory skeleton
RUN mkdir -p /home/user/datasets/raw/projectA /home/user/datasets/raw/projectB

# Helper to create files of exact size
RUN make_file () { dd if=/dev/zero of="$1" bs=1 count="$2" status=none; }; \
    RAW_ROOT="/home/user/datasets/raw" && \
    make_file "${RAW_ROOT}/projectA/img1.png"      1500000 && \
    make_file "${RAW_ROOT}/projectA/img2.png"      200000 && \
    make_file "${RAW_ROOT}/projectA/old1.jpg"      800000 && \
    make_file "${RAW_ROOT}/projectA/note.txt"      100 && \
    make_file "${RAW_ROOT}/projectB/big_graph.png" 2500000 && \
    make_file "${RAW_ROOT}/projectB/recent.jpg"    600000 && \
    make_file "${RAW_ROOT}/projectB/tiny.dat"      300000 && \
    make_file "${RAW_ROOT}/orphan.jpg"             700000 && \
    make_file "${RAW_ROOT}/readme.md"              4000

# Set modification times
RUN RAW_ROOT="/home/user/datasets/raw" && \
    touch -m -d @1625097600 "${RAW_ROOT}/projectA/img1.png" && \
    touch -m -d @1625184000 "${RAW_ROOT}/projectA/img2.png" && \
    touch -m -d @1622505600 "${RAW_ROOT}/projectA/old1.jpg" && \
    touch -m -d @1625270400 "${RAW_ROOT}/projectA/note.txt" && \
    touch -m -d @1625366400 "${RAW_ROOT}/projectB/big_graph.png" && \
    touch -m -d @1627843200 "${RAW_ROOT}/projectB/recent.jpg" && \
    touch -m -d @1625452800 "${RAW_ROOT}/projectB/tiny.dat" && \
    touch -m -d @1622592000 "${RAW_ROOT}/orphan.jpg" && \
    touch -m -d @1625539200 "${RAW_ROOT}/readme.md"

# Permissions for learners
RUN chmod -R 0777 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONIOENCODING=UTF-8