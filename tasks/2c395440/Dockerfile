FROM ubuntu:22.04

# Labels
LABEL Author="SystemDiagnosticsContainerSetup"
LABEL Description="Base image for system diagnostics assignment with pytest installed."

# Update package index and install required packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        procps \
        iproute2 && \
    # Install pytest for the test harness
    pip3 install --no-cache-dir pytest && \
    # Create writable home directory for the student
    mkdir -p /home/user && \
    # Make sure any unprivileged container user can write here
    chmod 0777 /home/user && \
    # Clean up apt caches to keep the image lean
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"
ENV HOME="/home/user"

WORKDIR /home/user

CMD ["/bin/bash", "-l"]