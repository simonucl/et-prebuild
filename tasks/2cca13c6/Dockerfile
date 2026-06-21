FROM ubuntu:22.04

# Author: OpenAI_Assistant
# Description: Initial state for the compression task – Ubuntu 22.04 with pytest installed

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/project/utils && \
    printf 'print("Hello from main")\n' > /home/user/project/main.py && \
    printf '# Project Sample\nA tiny project used for compression-task testing.\n' > /home/user/project/README.md && \
    printf 'def helper():\n    return "helping"\n' > /home/user/project/utils/helper.py && \
    chmod 0777 /home/user && \
    chmod -R a+rX,u+w /home/user/project

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV PYTHONUNBUFFERED=1