FROM ubuntu:22.04

# Help information
# Container for capacity-planning task. Open a shell with:
#     docker exec <container> /bin/bash
# or run your commands directly with:
#     docker exec <container> <command>

RUN set -e && \
    echo "Updating package lists and installing system packages..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-venv \
        build-essential && \
    echo "Installing Python packages (pytest and useful libs)..." && \
    pip3 install --no-cache-dir pytest psutil && \
    echo "Creating default home directory for the learner..." && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Set working directory
WORKDIR /home/user

CMD ["/bin/bash"]