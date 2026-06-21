FROM ubuntu:22.04

# %help and metadata
LABEL Author="Apptainer Task Preparer"
LABEL Description="Base image for UK time-zone logging task with pytest pre-installed."

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# Package installation, pytest, home directory setup, cleanup
RUN set -e && \
    apt-get -y update && \
    apt-get -y install --no-install-recommends \
        python3 \
        python3-pip \
        tzdata \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 755 /home/user && \
    rm -f /home/user/uk-time.log && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*