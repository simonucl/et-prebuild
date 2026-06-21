FROM ubuntu:22.04

# Help text
# This container image provides the initial filesystem and tooling
# (Python + pytest) required for the “single compound command” release
# management task.

# Labels
LABEL Author="Apptainer Task Setup"
LABEL Description="Environment for release-manager compound-command exercise."

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/release && \
    printf 'APP_NAME=webapp\nAPP_ENV=production\nAPP_VERSION=1.4.2' > /home/user/release/.env && \
    chmod 777 /home/user/release && \
    chmod 666 /home/user/release/.env

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Default command equivalent to Apptainer %runscript
CMD ["/bin/bash"]