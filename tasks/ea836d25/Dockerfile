FROM ubuntu:22.04

# Labels
LABEL Author="DevSecOps-Container-Setup"
LABEL Description="Base image for benchmarking /bin/true against a 1000 ms policy. Pytest pre-installed."

# Update package lists and install Python tooling
RUN apt-get update -y && \
    apt-get install -y python3-pip && \
    # Install pytest for the automated test-runner
    pip3 install --no-cache-dir pytest && \
    # Ensure the working directory for the student exists and is writable
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    # House-keeping
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV LC_ALL=C.UTF-8

WORKDIR /home/user