FROM ubuntu:22.04

# Labels
LABEL Author="mock_api_task_maintainer"
LABEL Description="Environment for the mock-API curl exercise, with pytest installed."

# Help information (as comments)
# This container supplies the minimal runtime environment (Python, curl, pytest)
# required for learners to complete the "mock-API" exercise. No task artefacts
# are pre-created so that the workspace starts in a clean state.

# Update apt indexes and install required packages
RUN set -e && \
    echo "Updating apt indexes and installing required packages ..." && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl \
        procps \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest via pip
RUN echo "Installing pytest via pip ..." && \
    pip3 install --no-cache-dir --upgrade pip setuptools && \
    pip3 install --no-cache-dir pytest

# Create a writable skeleton home directory for the exercise
RUN echo "Creating a writable skeleton home directory for the exercise ..." && \
    mkdir -p /home/user && \
    chmod 0777 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

WORKDIR /home/user