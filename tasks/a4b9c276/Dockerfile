FROM ubuntu:22.04

# Install Python, pip, and other dependencies
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the forthcoming automated checks
RUN pip3 install --no-cache-dir pytest

# Pre-task file system scaffolding expected by the grader
# 1. Ensure the generic home directory exists
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# 2. Provide a default .bashrc that *does not* yet source the dotenv file
RUN if [ -f /etc/skel/.bashrc ]; then \
        cp /etc/skel/.bashrc /home/user/.bashrc; \
    else \
        echo '# ~/.bashrc – default initial content for test container' > /home/user/.bashrc && \
        echo '# (Intentionally left minimal; will be extended by the backup-automation task.)' >> /home/user/.bashrc; \
    fi && \
    chmod 0666 /home/user/.bashrc

# Set environment - note: chmod in %environment is not standard, 
# we handle permissions in the build steps above
ENV HOME=/home/user

WORKDIR /home/user

# Default command provides a shell for convenience
CMD ["/bin/bash"]

# Help:
# This container supplies a minimal Ubuntu 22.04 environment with pytest
# installed and a predefined /home/user/.bashrc file that does *not* yet
# source any dotenv file.  It establishes the initial conditions required
# for the PostgreSQL-backup automation task's automated grading.