FROM ubuntu:22.04

# Update apt metadata and install Python + pip (minimal footprint)
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip python3-setuptools ca-certificates && \
    # Install pytest for the grader
    pip3 install --no-cache-dir pytest && \
    # Create an unprivileged user "user" with home /home/user
    # (the agent will work under this account)
    useradd -m -s /bin/bash user && \
    # Ensure the home directory is accessible to the unprivileged user
    chmod 755 /home/user && \
    # Clean up apt cache to keep the image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure Python is on PATH for any user
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Default action: just drop into the requested command or a shell
ENTRYPOINT []
CMD ["/bin/bash"]