FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare the initial workspace under /home/user/builds
RUN mkdir -p /home/user/builds && \
    cd /home/user/builds && \
    # Create the three build directories
    mkdir -p build_v1.0.0 && \
    mkdir -p build_v1.1.0 && \
    mkdir -p build_v1.2.0 && \
    # (Optional) placeholder files so the dirs are non-empty
    touch build_v1.0.0/placeholder.txt && \
    touch build_v1.1.0/placeholder.txt && \
    touch build_v1.2.0/placeholder.txt && \
    # Create the "latest" symlink pointing to build_v1.1.0
    ln -sfn build_v1.1.0 latest && \
    # Ensure the learner (non-root) can modify the contents
    chmod -R 777 /home/user/builds

RUN chmod 755 /home/user

# Author: Build-and-Release Exercise Container
# Description: Sets up initial state with outdated "latest" symlink for learners to fix.

CMD echo "Container for symlink-update exercise. Launch a shell with:" && \
    echo "  docker exec -it <container> /bin/bash"