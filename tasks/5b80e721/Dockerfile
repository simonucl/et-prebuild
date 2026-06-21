# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install system packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Prepare writable home directory for the unprivileged user that will run inside the container
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Provide an empty baseline .bashrc without the required export lines
RUN if [ ! -f /home/user/.bashrc ]; then \
        printf '# Initial user bashrc\n' > /home/user/.bashrc; \
    fi && \
    chmod 0666 /home/user/.bashrc

# Apply final permissions as specified in labels section
RUN chmod 755 /home/user

LABEL Author="task-prep"

CMD ["/bin/bash"]