FROM ubuntu:22.04

# Update package index and install Python + pip
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        bash && \
    rm -rf /var/lib/apt/lists/*

# Install pytest globally
RUN pip3 install --no-cache-dir pytest

# Create a non-root user `user` with home directory /home/user
RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -s /bin/bash user; \
    fi

# Ensure the user owns its home directory
RUN chown -R user:user /home/user

# Ensure correct permissions
RUN chmod 755 /home/user

ENV PYTHONDONTWRITEBYTECODE=1

# Help section
# Author: Your Name
# Description: Base image with Python and pytest for MLOps benchmark task

LABEL Author="Your Name"
LABEL Description="Base image with Python and pytest for MLOps benchmark task"

CMD ["/bin/bash"]