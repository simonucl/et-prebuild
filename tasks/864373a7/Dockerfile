# Converted from Apptainer definition file
FROM ubuntu:22.04

# 1. Install Python tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

# 2. Create initial repository layout
RUN mkdir -p /home/user/repo/releases && \
    mkdir -p /home/user/repo/stable && \
    echo "dummy binary 4.7.0" > /home/user/repo/releases/binary_4.7.0.bin && \
    echo "dummy binary 4.8.1" > /home/user/repo/releases/binary_4.8.1.bin && \
    chmod 644 /home/user/repo/releases/binary_4.7.0.bin && \
    chmod 644 /home/user/repo/releases/binary_4.8.1.bin && \
    ln -sf ../releases/binary_4.7.0.bin /home/user/repo/stable/binary.bin

# 3. Permissions
RUN chmod -R a+rX /home/user/repo && \
    chmod 777 /home/user/repo && \
    chmod 777 /home/user/repo/stable && \
    chmod 777 /home/user/repo/releases && \
    chmod 755 /home/user

# Environment variables
ENV LC_ALL=C
ENV LANG=C
ENV PYTHONUNBUFFERED=1

# Labels
LABEL Author="task-prep"
LABEL Description="Initial state for the binary-curator exercise (pytest pre-installed)"