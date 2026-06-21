# Converted from Apptainer definition file

FROM ubuntu:22.04

# Basic tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading suite
RUN pip3 install --no-cache-dir pytest

# Create non-root user “user” with home directory /home/user
RUN useradd -m -s /bin/bash user

# Prepare initial filesystem state for the exercise
RUN mkdir -p /home/user/backups/2024-05-01 && \
    mkdir -p /home/user/backups/2024-06-01 && \
    ln -s /home/user/backups/2024-05-01 /home/user/backup_latest && \
    chown -R user:user /home/user && \
    chmod -R a+rwx /home/user

# From %environment
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Default command (from %runscript)
CMD ["/bin/bash"]