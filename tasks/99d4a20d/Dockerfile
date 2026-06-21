# Converted from Apptainer definition
FROM ubuntu:22.04

# System packages & Python testing tools
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates \
        tzdata && \
    pip3 install --no-cache-dir pytest

# Create user account
RUN set -eux && \
    groupadd -g 1000 user && \
    useradd -m -d /home/user -s /bin/bash -u 1000 -g user user

# Populate initial experiments directory tree
RUN set -eux && \
    base=/home/user/experiments && \
    mkdir -p "$base"/exp01/checkpoints && \
    mkdir -p "$base"/exp01/logs && \
    mkdir -p "$base"/exp02/checkpoints && \
    mkdir -p "$base"/exp03/checkpoints && \
    printf 'dummy checkpoint 1\n'  > "$base/exp01/checkpoints/model_epoch_1.ckpt" && \
    printf 'dummy checkpoint 2\n'  > "$base/exp01/checkpoints/model_epoch_2.ckpt" && \
    printf 'dummy checkpoint 10\n' > "$base/exp02/checkpoints/model_epoch_10.ckpt" && \
    printf 'best checkpoint data\n' > "$base/exp03/checkpoints/best.ckpt" && \
    echo '(content irrelevant)' > "$base/exp01/logs/train.log" && \
    chown -R 1000:1000 /home/user

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Apply chmod for /home/user from %environment
RUN chmod 755 /home/user

# Environment variables from %environment
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Labels
LABEL Author="your_name_here"
LABEL Description="Environment for checkpoint-archiving task; contains initial experiment tree and pytest"

# Equivalent to %runscript
CMD ["/bin/bash"]