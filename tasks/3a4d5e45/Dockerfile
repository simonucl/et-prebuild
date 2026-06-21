FROM ubuntu:22.04

# Author SecurityEngineerAI
# Description: Container for credential-rotation task – initial state and pytest preinstalled
# Help:
# This Apptainer image provides the starting environment for the
# credential-rotation exercise.

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/credentials && \
    chmod 755 /home/user && \
    chmod 777 /home/user/credentials

RUN printf "OLD KEY 2023\n" > /home/user/credentials/api_key_2023.pem && \
    printf "NEW KEY 2024\n" > /home/user/credentials/api_key_2024.pem && \
    chmod 644 /home/user/credentials/api_key_2023.pem /home/user/credentials/api_key_2024.pem && \
    ln -s /home/user/credentials/api_key_2023.pem /home/user/credentials/api_key_current.pem

LABEL Author="SecurityEngineerAI"
LABEL Description="Container for credential-rotation task – initial state and pytest preinstalled"