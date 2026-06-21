# Converted from Apptainer definition file

FROM ubuntu:22.04

# %post commands
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 0777 /home/user

RUN rm -rf /home/user/docs || true

# %environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN chmod 755 /home/user

# %labels
LABEL Author="Apptainer Task Setup"
LABEL Description="Environment for cron-file exercise with pytest pre-installed."