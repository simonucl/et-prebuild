FROM ubuntu:22.04

# Labels
LABEL Author="example"
LABEL Description="Base image for Provisioning Utility exercise – includes pytest and a clean /home/user workspace."

# Post installation
RUN set -e && \
    echo "Updating APT and installing Python tooling..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates \
        git \
        bash && \
    echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating non-root user 'user' with home directory /home/user..." && \
    useradd -m -s /bin/bash user && \
    chown -R user:user /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Set proper permissions for home directory
RUN chmod 755 /home/user

# Help information as comments
# This container image provides a clean Ubuntu 22.04 environment with:
#   • A non-root user 'user' (home: /home/user)
#   • Python 3, pip and pytest pre-installed
#
# The workspace under /home/user is empty except for the directory itself,
# fulfilling the initial-state requirements of the automated grader.

# Default command (equivalent to runscript)
CMD echo "This container is prepared for the Provisioning Utility exercise." && \
    echo "Switch to the 'user' account to begin work, e.g.:" && \
    echo "    su - user" && \
    echo "Happy hacking!"