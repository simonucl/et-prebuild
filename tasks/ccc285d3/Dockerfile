FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="${PATH}:/home/user/.local/bin"

# Update package lists and install Python + pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    # Install pytest for the exercise test-suite
    pip3 install --no-cache-dir pytest && \
    # Ensure the required home directory exists and is writable
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    # Clean up apt caches to keep the image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/user

# Default command
CMD ["echo", "Docker container ready for the migration baseline task."]