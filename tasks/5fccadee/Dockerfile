# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update package index and install Python + pip
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create the only directory that must exist before the student starts
RUN mkdir -p /home/user/artifacts

# Make sure the student (a non-root user) can freely work in /home/user
RUN chmod -R 777 /home/user

# Set permissions as specified in the environment section
RUN chmod 755 /home/user

# Add the typical pip user-install location to PATH
ENV PATH="/home/user/.local/bin:${PATH}"

# %runscript equivalent: execute passed commands
CMD ["bash"]