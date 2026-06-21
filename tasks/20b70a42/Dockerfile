FROM ubuntu:22.04

# Make APT non-interactive
ENV DEBIAN_FRONTEND=noninteractive

# Update package index and install required software
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        libnss-myhostname \
        ca-certificates && \
    # Install pytest for the grading harness
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    # Guarantee that the system's own short hostname can be resolved
    if ! grep -q "myhostname" /etc/nsswitch.conf; then \
        sed -i 's/^\(hosts:.*files\)/\1 myhostname/' /etc/nsswitch.conf; \
    fi && \
    # Create the "user" account referenced in the assignment
    if ! id -u user >/dev/null 2>&1; then \
        useradd -m -d /home/user -s /bin/bash user; \
    fi && \
    chown -R user:user /home/user && \
    # Clean up APT caches to keep the image lean
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set permissions on home directory and configure PATH
RUN chmod 755 /home/user

# Ensure that Python user-installed executables are on PATH
ENV PATH=/usr/local/bin:$PATH