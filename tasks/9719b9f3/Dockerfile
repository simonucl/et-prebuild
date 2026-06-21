# Converted from Apptainer: Bootstrap localimage ./ubuntu_22.04.sif
FROM ubuntu:22.04

# post section
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    ln -sf /usr/bin/python3 /usr/local/bin/python || true

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/projects && \
    chmod -R a+rwx /home/user

# environment section
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# replicate chmod from environment (cannot execute in ENV)
RUN chmod 755 /home/user

# runscript equivalent
CMD ["bash"]