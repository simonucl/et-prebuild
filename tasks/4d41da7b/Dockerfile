FROM ubuntu:22.04

# Help / labels
LABEL Author="YourName"
LABEL Description="Environment for the project_utils/secure_scripts permissions task. Pytest pre-checks installed."

# Update package lists and install Python + pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates \
        build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Create group and user with UID/GID 1000 if they don't exist
RUN if ! getent group 1000 >/dev/null; then groupadd -g 1000 user; fi

RUN if ! id -u 1000 >/dev/null 2>&1; then useradd -m -u 1000 -g 1000 -s /bin/bash user; fi

# Ensure the home directory exists and correct permissions
RUN mkdir -p /home/user && \
    chown -R 1000:1000 /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/home/user/.local/bin:${PATH}"

# Default runscript equivalent
CMD ["bash"]