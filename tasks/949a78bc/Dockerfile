FROM ubuntu:22.04

# Update package index and install Python tooling
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip python3-setuptools && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the automated checker
RUN pip3 install --no-cache-dir pytest

# Prepare writable home directory for the non-root agent
RUN mkdir -p /home/user && chmod 777 /home/user

# Provide an initial .bashrc without the management block
RUN if [ ! -f /home/user/.bashrc ]; then \
        printf '# ~/.bashrc\n' > /home/user/.bashrc; \
    fi && \
    chmod 666 /home/user/.bashrc

# Converted from %labels (kept as comments because labels were not valid key-value pairs)
# chmod 755 /home/user
# Author env-management-task container