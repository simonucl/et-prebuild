FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Setup"
LABEL Description="Base image for IoT edge-computing SQLite exercise with pytest installed."

# Update APT index and install required system packages
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates \
        tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Ensure that /home/user exists (the grader expects this path)
RUN mkdir -p /home/user && \
    chmod 0755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Set working directory
WORKDIR /home/user

# Default command
CMD ["/bin/bash", "-c", "echo 'This container is prepared for the IoT edge SQLite exercise.' && echo 'Use the shell to begin working.' && /bin/bash"]