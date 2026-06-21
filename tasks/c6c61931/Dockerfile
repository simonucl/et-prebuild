# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python, pip, pytest, and clean up
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create initial log directory structure and files
RUN mkdir -p /home/user/logs && \
    echo "Log for 2023-12-30" > /home/user/logs/app-2023-12-30.log && \
    echo "Log for 2023-12-31" > /home/user/logs/app-2023-12-31.log && \
    ln -sf app-2023-12-30.log /home/user/logs/latest.log && \
    chmod -R a+rwx /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
ENV HOME="/home/user"

CMD ["/bin/bash"]