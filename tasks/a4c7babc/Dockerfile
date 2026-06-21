FROM ubuntu:22.04

# Labels
LABEL Author="chatbot"
LABEL Description="Base image for FinOps virtual-env exercise. Provides Python, pip, venv tooling and pytest for grading."

# Post installation
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        ca-certificates \
        build-essential && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 755 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Set working directory
WORKDIR /home/user

# Default command
CMD ["sh", "-c", "echo 'Container for FinOps exercise.' && echo \"Run 'pytest' to execute the validation tests.\""]