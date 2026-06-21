FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    # Prepare a writable home directory for the exercises
    mkdir -p /home/user && \
    chmod 1777 /home/user && \
    # Ensure the alerts path does NOT pre-exist (clean slate for the exercise)
    rm -rf /home/user/alerts && \
    # Clean up apt cache to keep the image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Set working directory
WORKDIR /home/user

# Default command
CMD ["echo", "This container is ready for the alert-file exercise."]