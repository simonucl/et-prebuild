FROM ubuntu:22.04

# Update package index and install Python tooling
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-wheel && \
    # Install pytest for the validation suites
    pip3 install --no-cache-dir pytest && \
    # Create the non-privileged user expected by the grading scripts
    useradd -m -s /bin/bash user && \
    # Ensure ownership of the home directory
    chown -R user:user /home/user && \
    # Clean up APT caches to keep the image lean
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set permissions on home directory
RUN chmod 755 /home/user

# Make sure user-level Python binaries (if any) are found first
ENV PATH="/home/user/.local/bin:${PATH}"

# Default entrypoint simply execs its arguments
ENTRYPOINT []
CMD ["/bin/bash"]