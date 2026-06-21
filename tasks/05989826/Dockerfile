FROM ubuntu:22.04

# Install required software
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        openssh-client \
        ca-certificates && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create user and set up home directory
RUN if ! id -u user >/dev/null 2>&1 ; then \
        useradd -m -u 1000 -d /home/user -s /bin/bash user ; \
    fi && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    chown -R 1000:1000 /home/user || true

# Set environment variables
ENV LC_ALL=C
ENV LANG=C
ENV PATH=/usr/local/bin:/usr/bin:/bin

WORKDIR /home/user

# Default entry: present an interactive shell
CMD ["/bin/bash"]