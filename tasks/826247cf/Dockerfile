FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer-Task-Builder"
LABEL Description="Base image for the DNS snapshot logging exercise (pytest included)"

# Update package index and install Python tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-venv \
        ca-certificates \
        tzdata \
        git && \
    # Create the regular (non-root) working user expected by the tasks
    useradd -m -s /bin/bash user && \
    chown -R user:user /home/user && \
    # Install pytest for the assessment framework
    pip3 install --no-cache-dir pytest && \
    # Clean up APT cache to reduce image size
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Basic runtime environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV HOME=/home/user

# Set permissions on home directory
RUN chmod 755 /home/user

# By default just drop into a shell
CMD ["/bin/bash"]