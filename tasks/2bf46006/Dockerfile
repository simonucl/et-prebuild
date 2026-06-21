FROM ubuntu:22.04

# Install Python + pip and build tools
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading framework
RUN pip3 install --no-cache-dir pytest

# Prepare the required initial filesystem layout for the assignment
# Create /home/user and the release directories
RUN mkdir -p /home/user/releases/2024-01-26 && \
    mkdir -p /home/user/releases/2024-01-20 && \
    mkdir -p /home/user/release

# Ensure the student (non-root runtime user) can write inside
# /home/user/release so they may create the symlink.
RUN chmod 0777 /home/user/release

# Keep the release directories themselves world-readable but not writable.
RUN chmod 0755 /home/user/releases && \
    chmod 0755 /home/user/releases/2024-01-26 && \
    chmod 0755 /home/user/releases/2024-01-20

# Set permissions on /home/user
RUN chmod 755 /home/user

# Make sure python and pip are on PATH
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Set working directory
WORKDIR /home/user

# Default command
CMD ["echo", "Container for symlink assignment. Run the provided tests with pytest."]