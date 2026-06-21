FROM ubuntu:22.04

# Update package lists and install Python + pip
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        bash && \
    pip3 install --no-cache-dir pytest

# Prepare a non-root user environment at /home/user
# Create the user if it does not already exist
RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -d /home/user -s /bin/bash user; \
    fi

# Ensure the home directory exists with correct ownership and permissions
RUN mkdir -p /home/user && \
    chown -R user:user /home/user && \
    chmod 755 /home/user

# Provide a minimal, clean ~/.bashrc
RUN echo "# .bashrc prepared for task – initially empty of custom PostgreSQL settings" > /home/user/.bashrc && \
    chown user:user /home/user/.bashrc && \
    chmod 644 /home/user/.bashrc

# Clean up apt caches to keep the image small
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Default action: open a shell as the non-root 'user'
CMD ["su", "-", "user"]