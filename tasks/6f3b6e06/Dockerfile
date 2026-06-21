FROM ubuntu:22.04

# Basic OS tooling
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        procps

# Python tooling (pytest for the grading suite)
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# Create the dedicated non-root account expected by the tests
# If UID/GID 1000 happen to be taken, ignore the error.
RUN groupadd -g 1000 user 2>/dev/null || true && \
    useradd -u 1000 -g 1000 -d /home/user -s /bin/bash user 2>/dev/null || true

# Ensure the home directory exists and is writable by everyone
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Make sure the task-specific directory does NOT exist
RUN rm -rf /home/user/documentation/process_mgmt || true

# Clean up to keep the image lean
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH="/home/user/.local/bin:${PATH}"

# Set permissions on home directory at runtime and define entrypoint
ENTRYPOINT ["/bin/bash", "-c", "chmod 755 /home/user && exec \"$@\"", "--"]