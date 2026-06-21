FROM ubuntu:22.04

# Refresh package index and install system dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        iputils-ping \
        dnsutils \
        ca-certificates && \
    # Install pytest so the auto-grader can run its checks
    pip3 install --no-cache-dir pytest && \
    # Create the unprivileged user expected by the grader
    useradd --create-home --shell /bin/bash user && \
    # Prepare (empty) directory for future artefacts; do NOT create the file
    mkdir -p /home/user/incidents && \
    chown -R user:user /home/user/incidents && \
    # Clean up APT caches to keep image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH=/home/user/.local/bin:$PATH

# Set permissions on home directory
RUN chmod 755 /home/user

# Default entrypoint: just execute whatever the caller supplied
ENTRYPOINT ["/bin/bash", "-c", "exec \"$@\"", "--"]