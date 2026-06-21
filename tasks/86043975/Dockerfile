FROM ubuntu:22.04

# Help text from %help
# This container provides the initial filesystem state for the
# virtual-environment creation exercise.
# • python3 and pytest are installed
# • /home/user/web_project exists (empty except for VCS files the student may add)
# • No virtual-environment artefacts or confirmation file exist

LABEL description="chmod 755 /home/user"
LABEL author="Container Setup Script for Virtual-Env Exercise"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/web_project && \
    chmod -R 777 /home/user

ENV HOME=/home/user