FROM ubuntu:22.04

# Apptainer %post
RUN set -eux \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --no-cache-dir pytest \
    && mkdir -p /home/user \
    && chmod 0777 /home/user

# Apptainer %environment (environment variables only)
ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1

# %runscript equivalent (Docker default entrypoint behavior executes commands directly)
ENTRYPOINT []