FROM ubuntu:22.04

# Labels
LABEL Author="infrastructure-task-setup"
LABEL Description="Baseline image for infra Makefile bootstrapping exercise"

# Update apt metadata and install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        make \
        ca-certificates \
        git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest for the upcoming test suites
RUN pip3 install --no-cache-dir pytest

# Create the non-root working user
RUN useradd -m -s /bin/bash user

# Prepare empty repository directory that the student will work in
RUN mkdir -p /home/user/infra && \
    chown -R user:user /home/user && \
    chmod 755 /home/user

# Basic locale / path settings
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PATH=/home/user/.local/bin:$PATH

# Help information (as comments):
# This container supplies a pristine environment for the "Makefile bootstrap"
# assignment.  It includes:
#   • Python 3 with pytest
#   • An empty repository directory at /home/user/infra
# Students should create the required Makefile and automation_setup.log files
# inside that directory using the non-root 'user' account.

CMD echo "Container for infrastructure Makefile exercise." && \
    echo "Switch to the 'user' account with:   su - user" && \
    echo "Repository directory: /home/user/infra"