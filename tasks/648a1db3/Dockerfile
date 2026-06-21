FROM ubuntu:22.04

# Install Python & pip
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the project directory structure
RUN mkdir -p /home/user/project/src

# Create the initial main.py file with the required contents
RUN cat >/home/user/project/src/main.py <<'EOF'
#!/usr/bin/env python3
print("Hello from main!")
EOF

# Make the script executable and set permissions
RUN chmod +x /home/user/project/src/main.py && \
    chmod -R a+rwx /home/user

# Clean up apt caches to keep the image small
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Set working directory
WORKDIR /home/user

CMD ["echo", "Container for the symlink-task is ready."]