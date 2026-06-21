FROM ubuntu:22.04

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Ensure user-level Python binaries are on the PATH
ENV PATH="${PATH}:/home/user/.local/bin"
ENV HOME=/home/user

RUN set -eux && \
    # Update package index and install required software
    apt-get update && \
    apt-get install -y --no-install-recommends \
        cron \
        iputils-ping \
        python3-pip && \
    # Create a non-root user called "user" with home directory /home/user
    if ! id -u user >/dev/null 2>&1; then \
        # Ensure group "user" exists (GID 1000 is conventional for the
        # first non-root account; adjust only if already taken).
        if ! getent group 1000 >/dev/null 2>&1; then \
            groupadd -g 1000 user; \
        fi; \
        useradd -m -u 1000 -g 1000 -s /bin/bash user; \
    fi && \
    chown -R 1000:1000 /home/user && \
    # Ensure cron spool directory has correct permissions so the
    # unprivileged user can later install a crontab.
    mkdir -p /var/spool/cron/crontabs && \
    chmod 1730 /var/spool/cron/crontabs && \
    # Python testing framework
    pip3 install --no-cache-dir pytest && \
    # Clean up apt cache to keep the image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

WORKDIR /home/user

# Default entrypoint: drop into a shell
CMD ["/bin/bash"]