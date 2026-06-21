FROM ubuntu:22.04

# Labels
LABEL Maintainer="microservice-container-prep"
LABEL Description="Base developer container for microservice SSH-key exercise"

# Post installation
RUN set -e && \
    echo "Updating package index and installing dependencies..." && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        openssh-client \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata \
        locales \
        git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Python tooling
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# Create dedicated non-privileged user "user" with home /home/user
RUN if ! getent group 1000 >/dev/null 2>&1; then \
        groupadd -g 1000 user || true; \
    fi && \
    if ! id -u 1000 >/dev/null 2>&1; then \
        useradd -u 1000 -g 1000 -m -d /home/user -s /bin/bash user || true; \
    fi && \
    mkdir -p /home/user && \
    chown -R 1000:1000 /home/user && \
    chmod 755 /home/user

# Ensure locale is usable
RUN sed -i 's/^# *\(en_US.UTF-8 UTF-8\)/\1/' /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=en_US.UTF-8

# Environment variables
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin

# Set working directory
WORKDIR /home/user

# Default user
USER user

# Default command
CMD ["/bin/bash", "-l"]

# Help information (as comments):
# This container provides the base environment for the "microservice
# administration SSH-key" exercise.  It contains:
#   • OpenSSH client utilities (ssh-keygen)  
#   • Python 3 with pytest pre-installed  
#   • A non-privileged user account "user" with home directory /home/user  
#
# The filesystem is intentionally left **clean**: no .ssh or log files
# related to the exercise are present.  Students are expected to carry out
# the provisioning steps after launching the container.