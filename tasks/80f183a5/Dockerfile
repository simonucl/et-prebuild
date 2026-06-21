# Converted from Apptainer definition file
FROM ubuntu:22.04

# Post section
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        iputils-ping && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && \
    printf '8.8.8.8\n1.1.1.1\n192.0.2.1\n' > /home/user/ip_list.txt && \
    chmod 644 /home/user/ip_list.txt && \
    chmod 777 /home/user

# Environment section
RUN chmod 755 /home/user
ENV PYTHONIOENCODING=UTF-8