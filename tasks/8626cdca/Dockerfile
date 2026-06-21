FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create an unprivileged user
RUN useradd -m -s /bin/bash user

# Prepare initial filesystem state
RUN mkdir -p /home/user/app

# Create the initial .env file with the required content
RUN printf 'APP_DB_USER=olduser\nAPP_DB_PASS=oldpass123\n' > /home/user/app/.env

# Set correct permissions (world-readable, writable by owner)
RUN chmod 0644 /home/user/app/.env

# Ensure ownership belongs to the unprivileged user
RUN chown -R user:user /home/user

# Set permissions on home directory
RUN chmod 755 /home/user

# Set the user
USER user

# Set working directory
WORKDIR /home/user

# Default command: drop to a shell
CMD ["/bin/bash"]