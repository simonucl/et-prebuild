FROM ubuntu:22.04

# Labels
LABEL Author="process-monitor-prep"
LABEL Description="Base image for the Process Monitor task – provides Python, pytest and a writable /home/user."

# Post installation
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        procps \
        iputils-ping \
        coreutils \
        ca-certificates && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    rm -rf /home/user/process_monitor || true && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Set working directory
WORKDIR /home/user

# Help information (as comments)
# This image supplies:
#   • Python 3
#   • pytest (for the autograder)
#   • Standard POSIX utilities (yes, ps, etc.)
# A writable /home/user is prepared. No task artefacts are present yet.

CMD ["echo", "Process Monitor task container – ready for action."]