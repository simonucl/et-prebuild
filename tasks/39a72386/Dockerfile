FROM ubuntu:22.04

# Help / labels from %labels section
LABEL Author="exercise-preparer"
LABEL Description="Base image for Schedule Periodic Connectivity-Check with a User Cron Job task. Installs cron, ping, and pytest."

ENV DEBIAN_FRONTEND=noninteractive

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        cron \
        iputils-ping \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*