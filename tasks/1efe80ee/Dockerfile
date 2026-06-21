FROM ubuntu:22.04

# Update package lists and install essentials
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        procps

# Install pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Create non-root user `user` with home directory /home/user
RUN set -eux && \
    if ! id -u user > /dev/null 2>&1; then \
        useradd -m -s /bin/bash -u 1000 user; \
    fi

# Prepare writable workspace for the exercises
RUN mkdir -p /home/user/projects && \
    chown -R user:user /home/user/projects

# Clean up APT caches to keep the image small
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Environment settings
RUN chmod 755 /home/user
ENV PATH=/usr/local/bin:/usr/bin:/bin
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Run script equivalent
CMD ["bash", "-c", "exec \"$@\"", "--"]