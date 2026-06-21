FROM ubuntu:22.04

# Labels
LABEL Author="OpenAI-ChatGPT"
LABEL Description="Apptainer image for the load-average logging one-liner task."

# Post installation
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create default non-root user and its home if they do not already exist
RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -u 1000 user; \
    fi && \
    mkdir -p /home/user && \
    chown -R 1000:1000 /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PATH=/home/user/.local/bin:$PATH

# Set working directory
WORKDIR /home/user

# Default command
CMD ["/bin/bash"]