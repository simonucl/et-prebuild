FROM ubuntu:22.04

# %post
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        openssh-client \
        jq \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user

# %environment
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin

RUN chmod 755 /home/user

# %help (as comments)
# Author: devsecops-container-builder
# Description: Base image for the SSH-key-as-code exercise – contains openssh-client, jq, and pytest.

# %runscript equivalent
CMD echo "This container is intended for automated testing of the SSH-key-as-code exercise."