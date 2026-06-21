FROM ubuntu:22.04

# Labels
LABEL Author="YourName"
LABEL Description="Container for hostname logging task; provides clean initial state and pytest"

# Post installation commands
RUN set -e && \
    # Update package lists and install Python and pip
    apt-get update && \
    apt-get install -y python3 python3-pip && \
    # Install pytest for the grading framework
    pip3 install --no-cache-dir pytest && \
    # Ensure the expected home directory exists and is write-accessible
    mkdir -p /home/user && \
    # Make it writable for any unprivileged UID that will run inside the container
    chmod 0777 /home/user && \
    # Clean up apt caches to keep image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Set working directory
WORKDIR /home/user

# Default action: start an interactive shell
CMD ["/bin/bash"]