FROM ubuntu:22.04

# Maintainer: Apptainer Task Preparer
# Description: Base image for “training_pipeline” exercise – clean initial state with pytest installed.

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-venv \
        procps \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 777 /home/user

# Apply permissions similar to %environment step
RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:$PATH
ENV PYTHONIOENCODING=utf-8

CMD ["/bin/sh", "-c", "echo 'This container sets up the environment for the training_pipeline exercise.' && echo 'Open a shell in the container and follow the task instructions.'"]