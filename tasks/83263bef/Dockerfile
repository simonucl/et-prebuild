FROM ubuntu:22.04

# Update package list and install Python + pip
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata && \
    # Upgrade pip and install pytest for the grading framework
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    # Ensure the workspace directory expected by the assignment exists
    mkdir -p /home/user && \
    # Make it writable for any non-root user that will run inside the container
    chmod 0777 /home/user && \
    # Clean up apt caches to keep the image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

WORKDIR /home/user

# Default action when the container is executed without arguments
ENTRYPOINT []
CMD ["/bin/bash"]