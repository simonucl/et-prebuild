FROM ubuntu:22.04

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Update package index and install Python + pip
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    # Install pytest for the test harness
    pip3 install --no-cache-dir pytest && \
    # Create the /home/user directory hierarchy
    mkdir -p /home/user/documents && \
    # Create the policy file with EXACT contents `abc` (no newline)
    printf 'abc' > /home/user/documents/policy.txt && \
    # Ensure sane permissions (non-root users need read access)
    chmod 644 /home/user/documents/policy.txt && \
    chmod 755 /home/user && \
    chmod 755 /home/user/documents && \
    # Do NOT create /home/user/audit: the learner must do that.
    # Clean up apt caches to keep the image small
    rm -rf /var/lib/apt/lists/*

# Labels
LABEL Author="Compliance Training Build"
LABEL Description="Container with initial state for auditable checksum task"

# Default command
CMD ["/bin/bash"]