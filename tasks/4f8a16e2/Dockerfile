FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Preparer"
LABEL Description="Base image with pytest installed and writable /home/user, ready for the student to generate datasets and metadata."

# Update package lists and install Python + pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    # Install pytest for the forthcoming test-suite
    pip3 install --no-cache-dir pytest && \
    # Create the required /home/user directory and make it writable
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    # Clean up APT caches to keep the image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Set working directory
WORKDIR /home/user