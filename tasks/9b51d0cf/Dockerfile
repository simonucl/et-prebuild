FROM ubuntu:22.04

# Author benchmark-preparation
# Description "Environment with reference data and tools for sort benchmark task"

RUN set -e && \
    echo "Updating package lists and installing required packages ..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        time python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "Creating unprivileged user 'user' ..." && \
    useradd -m -u 1000 -s /bin/bash user

RUN echo "Installing pytest for the agent ..." && \
    pip3 install --no-cache-dir pytest

RUN echo "Preparing benchmark directories and reference data ..." && \
    BENCH_DIR="/home/user/benchmarks" && \
    DATA_DIR="/home/user/benchmark_data" && \
    mkdir -p "${BENCH_DIR}" "${DATA_DIR}"

RUN cat <<'EOF' > /home/user/benchmark_data/small.txt
357
91
782
14
601
274
439
208
901
58
66
132
475
820
7
510
334
699
244
123
EOF

RUN seq 1 1000 > /home/user/benchmark_data/large.txt

RUN echo "Fixing permissions so that the unprivileged user owns the data ..." && \
    chown -R 1000:1000 /home/user && \
    chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH}"

CMD echo "Container for sort benchmark task. Switch to user with: su - user"