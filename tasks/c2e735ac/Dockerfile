FROM ubuntu:22.04

# Basic development tools
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        locales && \
    # Ensure UTF-8 locale is available
    sed -i 's/^# *\(en_US.UTF-8 UTF-8\)/\1/' /etc/locale.gen && \
    locale-gen && \
    # Install pytest for the grader
    pip3 install --no-cache-dir pytest && \
    # Prepare the expected home directory for the unprivileged user.
    # Give wide permissions so whichever UID runs inside the container
    # can create sub-directories and files.
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    # Clean up apt caches to keep the image small
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Default entrypoint drops to a shell so the agent can interact.
CMD ["/bin/bash"]