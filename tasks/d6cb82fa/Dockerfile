FROM ubuntu:22.04

# Update package index and install Python tooling
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    # Install pytest for the grading harness
    pip3 install --no-cache-dir pytest && \
    # Ensure `python` command is available
    ln -s /usr/bin/python3 /usr/local/bin/python || true && \
    # Create a writable home directory for the unprivileged runtime user.
    # The sticky bit (1777) lets any user write here while protecting others' files.
    mkdir -p /home/user && \
    chmod 1777 /home/user && \
    # Clean up apt cache to keep the image slim
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Minimal environment so Python and pip are on the PATH
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV HOME=/home/user

WORKDIR /home/user

# Labels
LABEL Author="Container build script for translation-sync exercise"

# Default action: start an interactive shell
CMD ["/bin/bash"]