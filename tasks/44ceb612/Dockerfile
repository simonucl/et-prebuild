# Converted from Apptainer definition file
FROM ubuntu:22.04

# Labels
LABEL maintainer="Container Prep Bot"

# Install packages, pytest, and create /home/user
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        openssh-client \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 1777 /home/user

# Environment settings
ENV PATH="/home/user/.local/bin:${PATH}"

RUN chmod 755 /home/user

# Default runscript behavior
CMD ["bash"]