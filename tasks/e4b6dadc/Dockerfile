FROM ubuntu:22.04

# Install required system packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        make \
        tar \
        gzip \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading infrastructure
RUN pip3 install --no-cache-dir pytest

# Prepare the workspace directory expected by the assignment
RUN mkdir -p /home/user/artifact-project

# Ensure the runtime (non-root) user can freely write to these paths
RUN chmod 0777 /home/user && \
    chmod 0777 /home/user/artifact-project

# Labels
LABEL Author="artifact-project-container"