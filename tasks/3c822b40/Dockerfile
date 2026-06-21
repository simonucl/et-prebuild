FROM ubuntu:22.04

# Labels
LABEL Author="ReleaseManagerPrep"
LABEL Description="Base image for deployment-cron exercise. Provides Python, pytest and cron; ensures /home/user is writable."

# Ensure non-interactive apt operations
ENV DEBIAN_FRONTEND=noninteractive

# Install packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        cron \
        ca-certificates \
        build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install pytest for the student's tests
RUN python3 -m pip install --upgrade pip setuptools && \
    python3 -m pip install pytest

# Prepare writable workspace for the student
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
ENV EDITOR="vi"

# Set working directory
WORKDIR /home/user

# Default action: start an interactive shell
CMD ["/bin/bash"]