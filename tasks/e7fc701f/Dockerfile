FROM ubuntu:22.04

# Labels
LABEL Author="example"
LABEL Description="Container for cloud-migration symlink task with initial legacy files and pytest installed."

# Set environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Update package lists and install Python + pytest
RUN set -e && \
    apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare the initial legacy configuration layout expected by tests
# Create the legacy directory tree and populate it with files.
RUN mkdir -p /home/user/old_configs

# Create the required *.conf files with exact contents (including
# the single trailing newline each file must have).
RUN printf 'APP_ENV=production\n'   > /home/user/old_configs/app.conf && \
    printf 'AUTH_METHOD=oauth2\n'   > /home/user/old_configs/auth.conf && \
    printf 'CACHE_SIZE=256\n'       > /home/user/old_configs/cache.conf && \
    printf 'DB_HOST=localhost\n'    > /home/user/old_configs/db.conf

# Set appropriate permissions so the unprivileged runtime user can read/write.
RUN chmod 755 /home/user && \
    chmod 755 /home/user/old_configs && \
    chmod 644 /home/user/old_configs/*.conf

# Clean up apt caches to keep the image small.
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*