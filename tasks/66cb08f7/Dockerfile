# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update package lists and install Python tooling required for both
# creating virtual environments and running pytest.
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading harness.
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Prepare the writable workspace for the student.
RUN mkdir -p /home/user && \
    chmod 777 /home/user

# Ensure correct default permissions on the home directory.
RUN chmod 755 /home/user

# Ensure user-installed Python packages are discoverable.
ENV PATH="/home/user/.local/bin:${PATH}"

# Container built for the virtual-environment assignment.