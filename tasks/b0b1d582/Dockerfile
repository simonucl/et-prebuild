# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install system packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install Python testing framework (pytest) and supervisord
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest supervisor

# Prepare a writable home for the non-root runtime user
RUN mkdir -p /home/user && chmod 0777 /home/user

# Apply environment-time permissions fix
RUN chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Run script equivalent
CMD sh -c "echo 'Container for the \"temperature-sensor\" edge-computing task.' && echo 'Python and pytest are installed. Begin your work in /home/user.'"