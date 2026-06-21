FROM ubuntu:22.04

# Update package index and install required system packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        time \
        ca-certificates \
        --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Ensure a writable home directory for the non-root runtime user
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Provide a convenient `python` alias if it's missing
RUN if [ ! -e /usr/local/bin/python ] && [ -x /usr/bin/python3 ]; then \
        ln -s /usr/bin/python3 /usr/local/bin/python; \
    fi

# Set environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin
ENV HOME=/home/user

WORKDIR /home/user

CMD ["/bin/bash"]