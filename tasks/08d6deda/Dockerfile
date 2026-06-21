FROM ubuntu:22.04

# Update apt index and install Python and pip
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Apply environment-time permissions that were in %environment
RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin"

CMD /bin/sh -c "echo 'Container for the support_diag assignment.' && echo 'Activate an interactive shell to begin.'"