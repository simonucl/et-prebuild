FROM ubuntu:22.04

# Update package index and install essential tools
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        make \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for container-side testing
RUN pip3 install --no-cache-dir pytest

# Provision the expected writable home directory for the student
RUN mkdir -p /home/user
RUN chmod 0777 /home/user

# Apply label section's chmod command
RUN chmod 755 /home/user

LABEL Author="Task Preparation Bot"
LABEL Description="Ubuntu 22.04 base with GNU Make and pytest, prepared for the compliance_audit task."