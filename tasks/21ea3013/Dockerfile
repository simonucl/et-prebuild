FROM ubuntu:22.04

# Author: LoopbackPingExercise
# Description: Base image for the loopback ping logging exercise (with pytest and ping installed).

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        iputils-ping \
        python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

LABEL Author="LoopbackPingExercise"
LABEL Description="Base image for the loopback ping logging exercise (with pytest and ping installed)."

CMD echo "Container for the loopback ping logging exercise." && \
    echo "Invoke a shell or run your commands as needed."