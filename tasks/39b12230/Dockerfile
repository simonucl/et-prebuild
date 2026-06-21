FROM ubuntu:22.04

# Ensure basic tooling is available
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        openssh-client && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment setup
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# Default action: open an interactive shell
CMD ["/bin/bash", "-l"]