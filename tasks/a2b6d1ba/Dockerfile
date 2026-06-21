FROM ubuntu:22.04

# Help text (from %help, if any existed)

ENV PYTHONPATH="/usr/local/lib/python3.10/dist-packages:${PYTHONPATH}"

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/compliance/logs/2024-02-01 && \
    mkdir -p /home/user/compliance/logs/2024-02-02 && \
    echo "SECURITY LOG 2024-02-01" > /home/user/compliance/logs/2024-02-01/security.log && \
    echo "SECURITY LOG 2024-02-02" > /home/user/compliance/logs/2024-02-02/security.log && \
    chmod 777 /home/user/compliance && \
    chmod 777 /home/user/compliance/logs && \
    chmod 755 /home/user/compliance/logs/2024-02-01 && \
    chmod 755 /home/user/compliance/logs/2024-02-02 && \
    chmod 644 /home/user/compliance/logs/2024-02-01/security.log && \
    chmod 644 /home/user/compliance/logs/2024-02-02/security.log