FROM ubuntu:22.04

# Labels
LABEL Author="SRE-Firewall-Task"
LABEL Description="Base image for firewall staging assignment with pytest pre-installed."

# Update package lists and install Python & pip
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    # Install pytest for the automated grader
    pip3 install --no-cache-dir pytest && \
    # Ensure the working directory for the student exists and is writable
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    # Minimal clean-up to keep image size small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Set working directory
WORKDIR /home/user