FROM ubuntu:22.04

LABEL Maintainer="Apptainer prep for network_lab exercise"
LABEL Description="Base image with pytest installed and a writable /home/user directory; no exercise artefacts created."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /home/user && \
    chmod 0777 /home/user

RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:${PATH}"

CMD echo "Container for the network_lab exercise.  Invoke your commands or tests as needed."