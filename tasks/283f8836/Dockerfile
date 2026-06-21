FROM ubuntu:22.04

# %post
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# %environment
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:/usr/bin:${PATH}"

# %labels
LABEL Author="monitoring-task-preparer"
LABEL Description="Base image for the monitoring scripting exercise—pytest installed, clean initial state."
LABEL Version="v1.0"