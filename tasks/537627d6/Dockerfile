FROM ubuntu:22.04

# Labels
LABEL Author="k8s-operator-task-preparer"
LABEL Description="Base image with Python and pytest installed; provides a writable /home/user starting point for the exercise."

# Install Python and pip
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest for the grading harness
RUN pip3 install --no-cache-dir pytest

# Create a writable home directory for the student/agent
RUN mkdir -p /home/user && \
    chmod 777 /home/user

# Set working directory
WORKDIR /home/user

# Set entrypoint to handle the runscript behavior
ENTRYPOINT ["/bin/sh", "-c", "chmod 755 /home/user && exec \"$@\"", "--"]