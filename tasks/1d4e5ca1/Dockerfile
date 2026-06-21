FROM ubuntu:22.04

# Install Python and pytest
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state for the "configs" assignment

# 1. Directory layout
RUN mkdir -p /home/user/projects/configs/available && \
    mkdir -p /home/user/projects/configs/enabled

# 2. Initial regular files
RUN echo -e "app configuration\n" > /home/user/projects/configs/available/app.conf && \
    echo -e "db configuration\n" > /home/user/projects/configs/available/db.conf

# 3. Broken symlink (must stay dangling)
RUN ln -s ../available/old.conf /home/user/projects/configs/enabled/old.conf

# 4. Make directories world-writable so the unprivileged agent can modify them
RUN chmod -R 0777 /home/user/projects

# Environment variables
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Default command
CMD ["/bin/bash"]