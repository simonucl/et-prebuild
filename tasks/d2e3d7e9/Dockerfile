FROM ubuntu:22.04

# Update package list and install Python plus pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python-is-python3

# Install pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Create the non-root user expected by the exercise
RUN useradd -m -s /bin/bash user

# Prepare the initial INI configuration file
RUN cat > /home/user/db_config.ini <<'EOF'
[general]
max_connections = 100
shared_buffers  = 128MB

[optimizer]
enable_hashjoin  = off
enable_mergejoin = on
enable_indexscan = off

[logging]
log_min_duration_statement = 100ms
EOF

# Ensure correct ownership so the learner (non-root) can modify it
RUN chown user:user /home/user/db_config.ini

# Clean up APT caches to keep the image small
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set permissions and environment variables
RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8