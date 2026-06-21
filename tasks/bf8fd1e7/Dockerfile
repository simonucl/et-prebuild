FROM ubuntu:22.04

# Fail fast
RUN set -e && \
    # Update package lists and install Python tooling
    apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    # Install pytest for the automated test harness
    pip3 install --no-cache-dir pytest && \
    # ------------------------------------------------------------------
    # Prepare initial filesystem state expected by the tests
    # ------------------------------------------------------------------
    # Create the user home hierarchy and the utils directory
    mkdir -p /home/user/utils && \
    # Make /home/user/utils writable by any unprivileged user that will
    # execute the tests inside the container.
    chmod 0777 /home/user/utils && \
    # Create /home/user/utils/input.txt containing exactly the 5 bytes "hello"
    printf 'hello' > /home/user/utils/input.txt && \
    # Set sensible permissions: readable by everyone, writable by owner (root)
    chmod 0644 /home/user/utils/input.txt && \
    # Ensure /home/user itself is accessible
    chmod 0755 /home/user && \
    # Clean up APT caches to keep the image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Set working directory
WORKDIR /home/user

# Default command
CMD ["echo", "Container ready. Execute your commands within this environment."]